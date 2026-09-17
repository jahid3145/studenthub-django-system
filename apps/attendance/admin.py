from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['subject', 'class_section', 'date', 'marked_by', 'created_at']
    list_filter = ['subject', 'class_section', 'date']
    inlines = [AttendanceRecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'remarks']
    list_filter = ['status', 'session__subject']
    search_fields = ['student__student_id', 'student__user__first_name']
