from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import AttendanceSession, AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'session', 'student', 'student_id', 'student_name', 'status', 'remarks']


class AttendanceSessionSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_section_name = serializers.CharField(source='class_section.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.user.get_full_name', read_only=True)
    records = AttendanceRecordSerializer(many=True, read_only=True)
    total_present = serializers.SerializerMethodField()
    total_absent = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSession
        fields = [
            'id', 'subject', 'subject_code', 'subject_name', 'class_section',
            'class_section_name', 'date', 'marked_by', 'marked_by_name',
            'records', 'total_present', 'total_absent', 'created_at'
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_total_present(self, obj):
        return obj.records.filter(status=AttendanceRecord.Status.PRESENT).count()

    @extend_schema_field(serializers.IntegerField())
    def get_total_absent(self, obj):
        return obj.records.filter(status=AttendanceRecord.Status.ABSENT).count()


class MarkBatchAttendanceSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField(required=True)
    class_section_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
    records = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        required=True,
        help_text="List of objects containing 'student_id', 'status', and optional 'remarks'"
    )
