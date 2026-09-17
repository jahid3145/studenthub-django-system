from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Department, Course, Subject, AcademicYear, ClassSection


class DepartmentSerializer(serializers.ModelSerializer):
    head_of_department_name = serializers.CharField(
        source='head_of_department.user.get_full_name',
        read_only=True
    )
    total_courses = serializers.IntegerField(source='courses.count', read_only=True)

    class Meta:
        model = Department
        fields = [
            'id', 'code', 'name', 'head_of_department', 'head_of_department_name',
            'description', 'is_active', 'total_courses', 'created_at', 'updated_at'
        ]


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    total_subjects = serializers.IntegerField(source='subjects.count', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'department', 'department_name', 'department_code',
            'duration_years', 'total_semesters', 'description', 'is_active',
            'total_subjects', 'created_at', 'updated_at'
        ]


class SubjectSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'code', 'name', 'course', 'course_code', 'course_name',
            'semester', 'credits', 'teacher', 'teacher_name', 'is_active',
            'created_at', 'updated_at'
        ]


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'name', 'start_date', 'end_date', 'is_current', 'created_at']


class ClassSectionSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = ClassSection
        fields = [
            'id', 'name', 'course', 'course_name', 'semester',
            'academic_year', 'academic_year_name', 'capacity', 'total_students', 'created_at'
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_total_students(self, obj):
        return obj.enrollments.filter(is_active=True).count()
