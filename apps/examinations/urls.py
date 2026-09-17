from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamViewSet,
    ExamScheduleViewSet,
    ExamResultViewSet,
    exam_list_view,
    result_transcript_view
)

app_name = 'examinations'

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'schedules', ExamScheduleViewSet, basename='exam-schedule')
router.register(r'results', ExamResultViewSet, basename='exam-result')

urlpatterns = [
    # Web Routes
    path('', exam_list_view, name='exam_list'),
    path('transcript/', result_transcript_view, name='transcript'),
    path('transcript/<int:student_id>/', result_transcript_view, name='transcript_detail'),

    # API Routes
    path('api/', include(router.urls)),
]
