from rest_framework import viewsets, permissions
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Department, Course, Subject, AcademicYear, ClassSection
from .serializers import (
    DepartmentSerializer,
    CourseSerializer,
    SubjectSerializer,
    AcademicYearSerializer,
    ClassSectionSerializer
)
from apps.accounts.permissions import IsAdminOrStaff, IsTeacher


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name', 'code']
    filterset_fields = ['is_active']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('department').all()
    serializer_class = CourseSerializer
    search_fields = ['name', 'code']
    filterset_fields = ['department', 'is_active']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('course', 'teacher', 'teacher__user').all()
    serializer_class = SubjectSerializer
    search_fields = ['name', 'code']
    filterset_fields = ['course', 'semester', 'teacher', 'is_active']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class ClassSectionViewSet(viewsets.ModelViewSet):
    queryset = ClassSection.objects.select_related('course', 'academic_year').all()
    serializer_class = ClassSectionSerializer
    search_fields = ['name']
    filterset_fields = ['course', 'semester', 'academic_year']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


# Web Template Views
@login_required
def department_list_view(request):
    departments = Department.objects.all()
    return render(request, 'academics/department_list.html', {'departments': departments})


@login_required
def course_list_view(request):
    courses = Course.objects.select_related('department').all()
    return render(request, 'academics/course_list.html', {'courses': courses})


@login_required
def subject_list_view(request):
    subjects = Subject.objects.select_related('course', 'teacher', 'teacher__user').all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})
