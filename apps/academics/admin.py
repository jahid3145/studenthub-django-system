from django.contrib import admin
from .models import Department, Course, Subject, AcademicYear, ClassSection


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'head_of_department', 'is_active', 'created_at']
    search_fields = ['code', 'name']
    list_filter = ['is_active']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'duration_years', 'total_semesters', 'is_active']
    search_fields = ['code', 'name']
    list_filter = ['department', 'is_active']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'course', 'semester', 'credits', 'teacher', 'is_active']
    search_fields = ['code', 'name']
    list_filter = ['course', 'semester', 'is_active']


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']


@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'semester', 'academic_year', 'capacity']
    search_fields = ['name']
    list_filter = ['course', 'semester', 'academic_year']
