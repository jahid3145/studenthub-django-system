from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet,
    CourseViewSet,
    SubjectViewSet,
    AcademicYearViewSet,
    ClassSectionViewSet,
    department_list_view,
    course_list_view,
    subject_list_view
)

app_name = 'academics'

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')
router.register(r'classes', ClassSectionViewSet, basename='class-section')

urlpatterns = [
    # Web Routes
    path('departments/', department_list_view, name='department_list'),
    path('courses/', course_list_view, name='course_list'),
    path('subjects/', subject_list_view, name='subject_list'),

    # API Routes
    path('api/', include(router.urls)),
]
