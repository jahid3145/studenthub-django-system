from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherProfileViewSet, teacher_list_view, teacher_detail_view

app_name = 'teachers'

router = DefaultRouter()
router.register(r'teachers', TeacherProfileViewSet, basename='teacher')

urlpatterns = [
    # Web Routes
    path('', teacher_list_view, name='teacher_list'),
    path('<int:pk>/', teacher_detail_view, name='teacher_detail'),

    # API Routes
    path('api/', include(router.urls)),
]
