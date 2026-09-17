from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Exam, ExamSchedule, ExamResult
from .serializers import (
    ExamSerializer,
    ExamScheduleSerializer,
    ExamResultSerializer
)
from apps.accounts.permissions import IsAdminOrStaff, IsTeacher, IsOwnerOrAdmin


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related('academic_year').all()
    serializer_class = ExamSerializer
    search_fields = ['name']
    filterset_fields = ['exam_type', 'academic_year', 'is_published']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class ExamScheduleViewSet(viewsets.ModelViewSet):
    queryset = ExamSchedule.objects.select_related('exam', 'subject', 'class_section').all()
    serializer_class = ExamScheduleSerializer
    filterset_fields = ['exam', 'subject', 'class_section', 'exam_date']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff | IsTeacher]
        return [permission() for permission in permission_classes]


class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.select_related('student', 'student__user', 'exam_schedule', 'exam_schedule__subject').all()
    serializer_class = ExamResultSerializer
    filterset_fields = ['student', 'exam_schedule', 'is_pass']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff | IsTeacher]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_student:
            return ExamResult.objects.filter(student__user=user).select_related('student', 'student__user', 'exam_schedule', 'exam_schedule__subject')
        return super().get_queryset()


# Web Template Views
@login_required
def exam_list_view(request):
    exams = Exam.objects.select_related('academic_year').filter(is_published=True) if request.user.is_student else Exam.objects.select_related('academic_year').all()
    return render(request, 'examinations/exam_list.html', {'exams': exams})


@login_required
def result_transcript_view(request, student_id=None):
    user = request.user
    if user.is_student:
        student = getattr(user, 'student_profile', None)
    elif student_id:
        from apps.students.models import StudentProfile
        student = get_object_or_404(StudentProfile, pk=student_id)
    else:
        messages.error(request, "Student ID is required.")
        return redirect('dashboard:index')

    results = ExamResult.objects.filter(student=student).select_related('exam_schedule', 'exam_schedule__subject', 'exam_schedule__exam')
    
    # Calculate overall GPA / Percentage
    total_max = sum([r.exam_schedule.max_marks for r in results])
    total_obtained = sum([r.marks_obtained for r in results])
    overall_pct = round((total_obtained / total_max * 100), 2) if total_max > 0 else 0.0

    return render(request, 'examinations/result_transcript.html', {
        'student': student,
        'results': results,
        'overall_pct': overall_pct,
        'total_obtained': total_obtained,
        'total_max': total_max
    })
