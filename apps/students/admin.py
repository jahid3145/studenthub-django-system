from django.contrib import admin
from .models import StudentProfile, Enrollment, StudentDocument


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'get_full_name', 'department', 'course', 'current_semester', 'status']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    list_filter = ['department', 'course', 'current_semester', 'status', 'gender']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Student Name'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_section', 'academic_year', 'semester', 'is_active', 'enrollment_date']
    search_fields = ['student__student_id', 'student__user__first_name']
    list_filter = ['academic_year', 'semester', 'is_active']


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'document_type', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified']
    search_fields = ['title', 'student__student_id']
