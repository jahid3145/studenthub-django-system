from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssignmentViewSet,
    AssignmentSubmissionViewSet,
    assignment_list_view,
    assignment_detail_view
)

app_name = 'assignments'

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', AssignmentSubmissionViewSet, basename='assignment-submission')

urlpatterns = [
    # Web Routes
    path('', assignment_list_view, name='assignment_list'),
    path('<int:pk>/', assignment_detail_view, name='assignment_detail'),

    # API Routes
    path('api/', include(router.urls)),
]
