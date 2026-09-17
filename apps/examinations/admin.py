from django.contrib import admin
from .models import Exam, ExamSchedule, ExamResult


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'academic_year', 'start_date', 'end_date', 'is_published']
    list_filter = ['exam_type', 'academic_year', 'is_published']
    search_fields = ['name']


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ['exam', 'subject', 'class_section', 'exam_date', 'max_marks', 'passing_marks']
    list_filter = ['exam', 'subject', 'class_section']


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_schedule', 'marks_obtained', 'letter_grade', 'is_pass']
    list_filter = ['letter_grade', 'is_pass', 'exam_schedule__exam']
    search_fields = ['student__student_id', 'student__user__first_name']
