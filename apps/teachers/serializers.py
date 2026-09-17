from rest_framework import serializers
from .models import TeacherProfile
from apps.accounts.serializers import UserSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    assigned_subjects_count = serializers.IntegerField(source='assigned_subjects.count', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'user_details', 'employee_id', 'department', 'department_name',
            'designation', 'qualification', 'joining_date', 'emergency_contact',
            'address', 'photo', 'assigned_subjects_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'employee_id', 'created_at', 'updated_at']
