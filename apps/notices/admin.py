from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'target_audience', 'created_by', 'is_active', 'created_at']
    list_filter = ['priority', 'target_audience', 'is_active']
    search_fields = ['title', 'content']
