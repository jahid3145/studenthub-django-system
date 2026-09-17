from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer
from apps.accounts.permissions import IsAdminOrStaff, IsTeacher, IsOwnerOrAdmin


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('subject', 'class_section', 'created_by', 'created_by__user').all()
    serializer_class = AssignmentSerializer
    search_fields = ['title', 'description']
    filterset_fields = ['subject', 'class_section']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsTeacher | IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.select_related('assignment', 'student', 'student__user').all()
    serializer_class = AssignmentSubmissionSerializer
    filterset_fields = ['assignment', 'student', 'status']

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsOwnerOrAdmin | IsTeacher]
        else:
            permission_classes = [IsTeacher | IsAdminOrStaff]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_student:
            return AssignmentSubmission.objects.filter(student__user=user)
        return super().get_queryset()


# Web Template Views
@login_required
def assignment_list_view(request):
    assignments = Assignment.objects.select_related('subject', 'class_section', 'created_by', 'created_by__user').all()
    user_submissions = {}

    if request.user.is_student:
        student = getattr(request.user, 'student_profile', None)
        submissions = AssignmentSubmission.objects.filter(student=student) if student else []
        user_submissions = {sub.assignment_id: sub for sub in submissions}

    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments,
        'user_submissions': user_submissions
    })


@login_required
def assignment_detail_view(request, pk):
    assignment = get_object_or_404(Assignment.objects.select_related('subject', 'class_section', 'created_by'), pk=pk)
    submission = None

    if request.user.is_student:
        student = getattr(request.user, 'student_profile', None)
        submission = AssignmentSubmission.objects.filter(assignment=assignment, student=student).first() if student else None

    submissions_list = []
    if request.user.is_teacher or request.user.is_admin_or_staff:
        submissions_list = assignment.submissions.select_related('student', 'student__user').all()

    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment,
        'submission': submission,
        'submissions_list': submissions_list
    })
