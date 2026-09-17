from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    class_section_name = serializers.CharField(source='class_section.name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Notice
        fields = [
            'id', 'title', 'content', 'created_by', 'created_by_name',
            'target_audience', 'department', 'department_name', 'course',
            'course_name', 'class_section', 'class_section_name', 'priority',
            'attachment', 'expiry_date', 'is_expired', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
