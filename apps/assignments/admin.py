from django.contrib import admin
from .models import Assignment, AssignmentSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'class_section', 'created_by', 'due_date', 'max_marks']
    list_filter = ['subject', 'class_section', 'due_date']
    search_fields = ['title', 'description']


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'status', 'submitted_at', 'marks_obtained']
    list_filter = ['status', 'submitted_at']
    search_fields = ['student__student_id', 'assignment__title']
