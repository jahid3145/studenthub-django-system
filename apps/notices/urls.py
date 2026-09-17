from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NoticeViewSet,
    notice_list_view,
    notice_detail_view
)

app_name = 'notices'

router = DefaultRouter()
router.register(r'notices', NoticeViewSet, basename='notice')

urlpatterns = [
    # Web Routes
    path('', notice_list_view, name='notice_list'),
    path('<int:pk>/', notice_detail_view, name='notice_detail'),

    # API Routes
    path('api/', include(router.urls)),
]
