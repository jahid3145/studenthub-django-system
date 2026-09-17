from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'model_name', 'record_id', 'ip_address']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'description', 'action']
    readonly_fields = ['timestamp', 'user', 'action', 'model_name', 'record_id', 'description', 'ip_address']
