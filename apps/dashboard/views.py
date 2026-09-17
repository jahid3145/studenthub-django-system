from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q

from apps.students.models import StudentProfile, Enrollment
from apps.teachers.models import TeacherProfile
from apps.academics.models import Department, Course, Subject, ClassSection
from apps.attendance.models import AttendanceRecord
from apps.examinations.models import ExamResult, ExamSchedule
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.fees.models import StudentFee
from apps.notices.models import Notice


@login_required
def index_view(request):
    user = request.user

    if user.is_admin_or_staff:
        context = {
            'total_students': StudentProfile.objects.count(),
            'total_teachers': TeacherProfile.objects.count(),
            'total_departments': Department.objects.count(),
            'total_courses': Course.objects.count(),
            'total_fees_collected': StudentFee.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0.00,
            'total_fees_pending': StudentFee.objects.aggregate(Sum('due_amount'))['due_amount__sum'] or 0.00,
            'recent_notices': Notice.objects.filter(is_active=True)[:5],
            'recent_students': StudentProfile.objects.select_related('user', 'department', 'course')[:5]
        }
        return render(request, 'dashboard/admin_dashboard.html', context)

    elif user.is_teacher:
        teacher = getattr(user, 'teacher_profile', None)
        assigned_subjects = teacher.assigned_subjects.all() if teacher else []
        context = {
            'teacher': teacher,
            'assigned_subjects': assigned_subjects,
            'total_assigned_subjects': len(assigned_subjects),
            'pending_assignments': Assignment.objects.filter(created_by=teacher)[:5] if teacher else [],
            'recent_notices': Notice.objects.filter(is_active=True)[:5]
        }
        return render(request, 'dashboard/teacher_dashboard.html', context)

    else:  # Student
        student = getattr(user, 'student_profile', None)
        attendance_records = AttendanceRecord.objects.filter(student=student) if student else []
        total_att = attendance_records.count()
        present_att = attendance_records.filter(status__in=['P', 'L']).count()
        att_percentage = round((present_att / total_att * 100), 2) if total_att > 0 else 0.0

        results = ExamResult.objects.filter(student=student).select_related('exam_schedule__subject') if student else []
        pending_assignments = Assignment.objects.all()[:5]
        fees = StudentFee.objects.filter(student=student) if student else []
        notices = Notice.objects.filter(is_active=True)[:5]

        context = {
            'student': student,
            'attendance_percentage': att_percentage,
            'is_low_attendance': att_percentage < 75.0,
            'recent_results': results[:5],
            'pending_assignments': pending_assignments,
            'fee_records': fees,
            'notices': notices
        }
        return render(request, 'dashboard/student_dashboard.html', context)


class DashboardStatsAPIView(APIView):
    """API endpoint providing role-tailored analytical data for dashboard consumption."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_admin_or_staff:
            data = {
                'role': user.role,
                'total_students': StudentProfile.objects.count(),
                'total_teachers': TeacherProfile.objects.count(),
                'total_departments': Department.objects.count(),
                'total_courses': Course.objects.count(),
                'financials': {
                    'total_collected': float(StudentFee.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0.00),
                    'total_pending': float(StudentFee.objects.aggregate(Sum('due_amount'))['due_amount__sum'] or 0.00),
                }
            }
        elif user.is_teacher:
            teacher = getattr(user, 'teacher_profile', None)
            data = {
                'role': user.role,
                'assigned_subjects_count': teacher.assigned_subjects.count() if teacher else 0,
                'assignments_created_count': Assignment.objects.filter(created_by=teacher).count() if teacher else 0,
            }
        else:  # Student
            student = getattr(user, 'student_profile', None)
            att_records = AttendanceRecord.objects.filter(student=student) if student else []
            total_att = att_records.count()
            present_att = att_records.filter(status__in=['P', 'L']).count()
            data = {
                'role': user.role,
                'student_id': student.student_id if student else None,
                'attendance_percentage': round((present_att / total_att * 100), 2) if total_att > 0 else 0.0,
                'is_low_attendance_warning': (present_att / total_att * 100) < 75.0 if total_att > 0 else False,
            }

        return Response({"success": True, "data": data})
