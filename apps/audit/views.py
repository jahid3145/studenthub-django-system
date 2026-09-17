from rest_framework import viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer
from apps.accounts.permissions import IsSuperAdmin


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsSuperAdmin]
    search_fields = ['user__username', 'action', 'description']
    filterset_fields = ['action', 'model_name']
