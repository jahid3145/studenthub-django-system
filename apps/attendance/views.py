from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q

from .models import AttendanceSession, AttendanceRecord
from .serializers import (
    AttendanceSessionSerializer,
    AttendanceRecordSerializer,
    MarkBatchAttendanceSerializer
)
from apps.academics.models import Subject, ClassSection
from apps.students.models import StudentProfile
from apps.accounts.permissions import IsAdminOrStaff, IsTeacher, IsOwnerOrAdmin


class AttendanceSessionViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSession.objects.select_related('subject', 'class_section', 'marked_by', 'marked_by__user').all()
    serializer_class = AttendanceSessionSerializer
    filterset_fields = ['subject', 'class_section', 'date']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsTeacher | IsAdminOrStaff]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[IsTeacher | IsAdminOrStaff])
    def mark_batch(self, request):
        serializer = MarkBatchAttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "message": "Invalid data.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        subject = get_object_or_404(Subject, pk=data['subject_id'])
        class_section = get_object_or_404(ClassSection, pk=data['class_section_id'])
        teacher_profile = getattr(request.user, 'teacher_profile', None)

        session, created = AttendanceSession.objects.get_or_create(
            subject=subject,
            class_section=class_section,
            date=data['date'],
            defaults={'marked_by': teacher_profile}
        )

        for rec in data['records']:
            student_id = rec.get('student_id')
            status_val = rec.get('status', 'P')
            remarks_val = rec.get('remarks', '')

            try:
                student = StudentProfile.objects.get(pk=student_id)
                AttendanceRecord.objects.update_or_create(
                    session=session,
                    student=student,
                    defaults={'status': status_val, 'remarks': remarks_val}
                )
            except StudentProfile.DoesNotExist:
                continue

        return Response({
            "success": True,
            "message": f"Attendance marked for {len(data['records'])} students.",
            "data": AttendanceSessionSerializer(session).data
        }, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)


class AttendanceRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttendanceRecord.objects.select_related('session', 'student', 'student__user').all()
    serializer_class = AttendanceRecordSerializer
    filterset_fields = ['session', 'student', 'status']

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_student:
            return AttendanceRecord.objects.filter(student__user=user)
        return super().get_queryset()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def student_attendance_summary(request, student_id=None):
    """
    API calculating subject-wise and overall attendance percentage.
    Formula: Attendance % = (Present Classes / Total Sessions) * 100
    Warning if percentage < 75%.
    """
    user = request.user
    if user.is_student:
        student = getattr(user, 'student_profile', None)
    elif student_id:
        student = get_object_or_404(StudentProfile, pk=student_id)
    else:
        return Response({"success": False, "message": "student_id parameter is required."}, status=400)

    if not student:
        return Response({"success": False, "message": "Student profile not found."}, status=404)

    records = AttendanceRecord.objects.filter(student=student)
    total_sessions = records.count()
    present_sessions = records.filter(status__in=['P', 'L']).count()
    overall_percentage = round((present_sessions / total_sessions * 100), 2) if total_sessions > 0 else 0.0

    # Subject wise breakdown
    subject_summary = []
    subject_records = records.values(
        'session__subject__id',
        'session__subject__code',
        'session__subject__name'
    ).annotate(
        total=Count('id'),
        present=Count('id', filter=Q(status__in=['P', 'L']))
    )

    for item in subject_records:
        sub_total = item['total']
        sub_present = item['present']
        sub_pct = round((sub_present / sub_total * 100), 2) if sub_total > 0 else 0.0
        subject_summary.append({
            'subject_id': item['session__subject__id'],
            'subject_code': item['session__subject__code'],
            'subject_name': item['session__subject__name'],
            'total_classes': sub_total,
            'present_classes': sub_present,
            'percentage': sub_pct,
            'is_low_attendance': sub_pct < 75.0
        })

    return Response({
        "success": True,
        "data": {
            "student_id": student.student_id,
            "student_name": student.user.get_full_name(),
            "total_classes": total_sessions,
            "present_classes": present_sessions,
            "overall_percentage": overall_percentage,
            "is_low_attendance_warning": overall_percentage < 75.0,
            "subject_breakdown": subject_summary
        }
    })


# Web Template Views
@login_required
def attendance_dashboard_view(request):
    user = request.user
    if user.is_student:
        student = getattr(user, 'student_profile', None)
        records = AttendanceRecord.objects.filter(student=student) if student else []
        total_sessions = records.count() if student else 0
        present_sessions = records.filter(status__in=['P', 'L']).count() if student else 0
        overall_percentage = round((present_sessions / total_sessions * 100), 2) if total_sessions > 0 else 0.0

        return render(request, 'attendance/student_attendance.html', {
            'records': records,
            'total_sessions': total_sessions,
            'present_sessions': present_sessions,
            'overall_percentage': overall_percentage,
            'is_warning': overall_percentage < 75.0
        })

    classes = ClassSection.objects.all()
    subjects = Subject.objects.all()
    recent_sessions = AttendanceSession.objects.select_related('subject', 'class_section', 'marked_by').all()[:10]

    return render(request, 'attendance/mark_attendance.html', {
        'classes': classes,
        'subjects': subjects,
        'recent_sessions': recent_sessions
    })
