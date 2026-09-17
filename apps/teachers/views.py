from rest_framework import viewsets, permissions
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import TeacherProfile
from .serializers import TeacherProfileSerializer
from apps.accounts.permissions import IsAdminOrStaff, IsTeacher


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.select_related('user', 'department').prefetch_related('assigned_subjects').all()
    serializer_class = TeacherProfileSerializer
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email']
    filterset_fields = ['department', 'designation']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


@login_required
def teacher_list_view(request):
    teachers = TeacherProfile.objects.select_related('user', 'department').all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})


@login_required
def teacher_detail_view(request, pk):
    teacher = get_object_or_404(TeacherProfile.objects.select_related('user', 'department'), pk=pk)
    assigned_subjects = teacher.assigned_subjects.select_related('course').all()
    return render(request, 'teachers/teacher_detail.html', {
        'teacher': teacher,
        'assigned_subjects': assigned_subjects
    })
