from rest_framework import serializers
from .models import Exam, ExamSchedule, ExamResult


class ExamSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    total_schedules = serializers.IntegerField(source='schedules.count', read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'exam_type', 'academic_year', 'academic_year_name',
            'start_date', 'end_date', 'is_published', 'total_schedules', 'created_at'
        ]


class ExamScheduleSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source='exam.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_section_name = serializers.CharField(source='class_section.name', read_only=True)

    class Meta:
        model = ExamSchedule
        fields = [
            'id', 'exam', 'exam_name', 'subject', 'subject_code', 'subject_name',
            'class_section', 'class_section_name', 'exam_date', 'start_time',
            'end_time', 'max_marks', 'passing_marks'
        ]


class ExamResultSerializer(serializers.ModelSerializer):
    student_id_str = serializers.CharField(source='student.student_id', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_code = serializers.CharField(source='exam_schedule.subject.code', read_only=True)
    subject_name = serializers.CharField(source='exam_schedule.subject.name', read_only=True)
    max_marks = serializers.IntegerField(source='exam_schedule.max_marks', read_only=True)

    class Meta:
        model = ExamResult
        fields = [
            'id', 'student', 'student_id_str', 'student_name', 'exam_schedule',
            'subject_code', 'subject_name', 'max_marks', 'marks_obtained',
            'letter_grade', 'grade_point', 'is_pass', 'remarks', 'created_at'
        ]
        read_only_fields = ['id', 'letter_grade', 'grade_point', 'is_pass', 'created_at']
