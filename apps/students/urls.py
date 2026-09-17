from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentProfileViewSet,
    EnrollmentViewSet,
    StudentDocumentViewSet,
    student_list_view,
    student_detail_view,
    student_create_view,
    student_edit_view
)

app_name = 'students'

router = DefaultRouter()
router.register(r'students', StudentProfileViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'documents', StudentDocumentViewSet, basename='student-document')

urlpatterns = [
    # Web Routes
    path('', student_list_view, name='student_list'),
    path('create/', student_create_view, name='student_create'),
    path('<int:pk>/', student_detail_view, name='student_detail'),
    path('<int:pk>/edit/', student_edit_view, name='student_edit'),

    # API Routes
    path('api/', include(router.urls)),
]
