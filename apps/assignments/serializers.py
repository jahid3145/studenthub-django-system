from rest_framework import serializers
from .models import Assignment, AssignmentSubmission


class AssignmentSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_section_name = serializers.CharField(source='class_section.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.user.get_full_name', read_only=True)
    total_submissions = serializers.IntegerField(source='submissions.count', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'subject', 'subject_code', 'subject_name',
            'class_section', 'class_section_name', 'created_by', 'created_by_name',
            'due_date', 'max_marks', 'attachment', 'total_submissions', 'is_overdue', 'created_at'
        ]


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_id_str = serializers.CharField(source='student.student_id', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    max_marks = serializers.IntegerField(source='assignment.max_marks', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'assignment_title', 'student', 'student_id_str',
            'student_name', 'submission_text', 'file', 'submitted_at',
            'status', 'max_marks', 'marks_obtained', 'feedback', 'graded_by'
        ]
        read_only_fields = ['id', 'submitted_at', 'status']
