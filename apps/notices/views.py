from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import Notice
from .serializers import NoticeSerializer
from apps.accounts.permissions import IsAdminOrStaff, IsTeacher


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer
    search_fields = ['title', 'content']
    filterset_fields = ['target_audience', 'priority', 'is_active']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsTeacher | IsAdminOrStaff]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Notice.objects.filter(is_active=True).filter(
            Q(expiry_date__isnull=True) | Q(expiry_date__gte=timezone.now().date())
        )

        if user and user.is_authenticated:
            if user.is_student and hasattr(user, 'student_profile'):
                student = user.student_profile
                dept_id = student.department_id
                course_id = student.course_id
                
                queryset = queryset.filter(
                    Q(target_audience=Notice.Audience.ALL) |
                    Q(target_audience=Notice.Audience.DEPARTMENT, department_id=dept_id) |
                    Q(target_audience=Notice.Audience.COURSE, course_id=course_id)
                )
            elif user.is_teacher and hasattr(user, 'teacher_profile'):
                teacher = user.teacher_profile
                dept_id = teacher.department_id
                queryset = queryset.filter(
                    Q(target_audience=Notice.Audience.ALL) |
                    Q(target_audience=Notice.Audience.DEPARTMENT, department_id=dept_id)
                )

        return queryset.select_related('created_by', 'department', 'course', 'class_section')


# Web Template Views
@login_required
def notice_list_view(request):
    user = request.user
    queryset = Notice.objects.filter(is_active=True)

    if user.is_student and hasattr(user, 'student_profile'):
        student = user.student_profile
        queryset = queryset.filter(
            Q(target_audience=Notice.Audience.ALL) |
            Q(target_audience=Notice.Audience.DEPARTMENT, department_id=student.department_id) |
            Q(target_audience=Notice.Audience.COURSE, course_id=student.course_id)
        )

    return render(request, 'notices/notice_list.html', {'notices': queryset})


@login_required
def notice_detail_view(request, pk):
    notice = get_object_or_404(Notice.objects.select_related('created_by', 'department', 'course'), pk=pk)
    return render(request, 'notices/notice_detail.html', {'notice': notice})
