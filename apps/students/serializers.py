from rest_framework import serializers
from .models import StudentProfile, Enrollment, StudentDocument
from apps.accounts.serializers import UserSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_details', 'student_id', 'department', 'department_name',
            'course', 'course_name', 'current_semester', 'date_of_birth', 'gender',
            'phone', 'address', 'guardian_name', 'guardian_phone', 'admission_date',
            'status', 'photo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'student_id', 'created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    class_section_name = serializers.CharField(source='class_section.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'class_section', 'class_section_name',
            'academic_year', 'academic_year_name', 'semester', 'enrollment_date', 'is_active'
        ]


class StudentDocumentSerializer(serializers.ModelSerializer):
    student_id_str = serializers.CharField(source='student.student_id', read_only=True)

    class Meta:
        model = StudentDocument
        fields = [
            'id', 'student', 'student_id_str', 'title', 'document_type',
            'file', 'is_verified', 'uploaded_at'
        ]
