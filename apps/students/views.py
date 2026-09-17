from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import StudentProfile, Enrollment, StudentDocument
from .forms import StudentCreateForm, StudentEditForm
from .serializers import (
    StudentProfileSerializer,
    EnrollmentSerializer,
    StudentDocumentSerializer
)
from apps.accounts.permissions import IsAdminOrStaff, IsTeacher, IsStudent, IsOwnerOrAdmin


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user', 'department', 'course').all()
    serializer_class = StudentProfileSerializer
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    filterset_fields = ['department', 'course', 'current_semester', 'status']

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [IsAdminOrStaff | IsTeacher]
        elif self.action in ['retrieve']:
            permission_classes = [IsOwnerOrAdmin | IsTeacher]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_student:
            return StudentProfile.objects.filter(user=user).select_related('user', 'department', 'course')
        return super().get_queryset()


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'student__user', 'class_section', 'academic_year').all()
    serializer_class = EnrollmentSerializer
    filterset_fields = ['student', 'class_section', 'academic_year', 'semester', 'is_active']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class StudentDocumentViewSet(viewsets.ModelViewSet):
    queryset = StudentDocument.objects.select_related('student', 'student__user').all()
    serializer_class = StudentDocumentSerializer
    filterset_fields = ['student', 'document_type', 'is_verified']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsOwnerOrAdmin | IsTeacher]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_student:
            return StudentDocument.objects.filter(student__user=user)
        return super().get_queryset()


# Web Template Views
@login_required
def student_list_view(request):
    if request.user.is_student:
        student = getattr(request.user, 'student_profile', None)
        if student:
            return redirect('students:student_detail', pk=student.pk)
        messages.error(request, "Student profile not found.")
        return redirect('dashboard:index')
    
    students = StudentProfile.objects.select_related('user', 'department', 'course').all()
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def student_detail_view(request, pk):
    student = get_object_or_404(StudentProfile.objects.select_related('user', 'department', 'course'), pk=pk)

    # Permission check: Student can only view self unless admin/teacher
    if request.user.is_student and student.user != request.user:
        messages.error(request, "Access denied. You can only view your own student profile.")
        return redirect('dashboard:index')

    enrollments = student.enrollments.select_related('class_section', 'academic_year').all()
    documents = student.documents.all()

    return render(request, 'students/student_detail.html', {
        'student': student,
        'enrollments': enrollments,
        'documents': documents
    })


@login_required
def student_create_view(request):
    if not (request.user.is_admin_or_staff or request.user.is_teacher):
        messages.error(request, "Access denied. Only administrators and staff can create student records.")
        return redirect('students:student_list')

    if request.method == 'POST':
        form = StudentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student '{student.user.get_full_name() or student.user.username}' ({student.student_id}) created successfully!")
            return redirect('students:student_detail', pk=student.pk)
    else:
        form = StudentCreateForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'is_edit': False
    })


@login_required
def student_edit_view(request, pk):
    if not (request.user.is_admin_or_staff or request.user.is_teacher):
        messages.error(request, "Access denied. Only administrators and staff can edit student records.")
        return redirect('students:student_list')

    student = get_object_or_404(StudentProfile, pk=pk)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student details for '{student.user.get_full_name() or student.user.username}' updated successfully!")
            return redirect('students:student_detail', pk=student.pk)
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'is_edit': True
    })

