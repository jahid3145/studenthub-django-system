from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AttendanceSessionViewSet,
    AttendanceRecordViewSet,
    student_attendance_summary,
    attendance_dashboard_view
)

app_name = 'attendance'

router = DefaultRouter()
router.register(r'sessions', AttendanceSessionViewSet, basename='attendance-session')
router.register(r'records', AttendanceRecordViewSet, basename='attendance-record')

urlpatterns = [
    # Web View
    path('', attendance_dashboard_view, name='dashboard'),

    # API Routes
    path('api/summary/', student_attendance_summary, name='api_student_summary'),
    path('api/summary/<int:student_id>/', student_attendance_summary, name='api_student_summary_detail'),
    path('api/', include(router.urls)),
]
