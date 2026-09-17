from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet

app_name = 'audit'

router = DefaultRouter()
router.register(r'logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('api/', include(router.urls)),
]
