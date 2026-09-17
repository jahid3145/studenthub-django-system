from rest_framework import serializers
from .models import FeeStructure, StudentFee, PaymentRecord


class FeeStructureSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)

    class Meta:
        model = FeeStructure
        fields = [
            'id', 'course', 'course_name', 'academic_year', 'academic_year_name',
            'semester', 'title', 'total_amount', 'due_date', 'created_at'
        ]


class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = ['id', 'student_fee', 'transaction_id', 'amount', 'payment_date', 'payment_method', 'notes']
        read_only_fields = ['id', 'transaction_id', 'payment_date']


class StudentFeeSerializer(serializers.ModelSerializer):
    student_id_str = serializers.CharField(source='student.student_id', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    fee_title = serializers.CharField(source='fee_structure.title', read_only=True)
    due_date = serializers.DateField(source='fee_structure.due_date', read_only=True)
    payments = PaymentRecordSerializer(many=True, read_only=True)

    class Meta:
        model = StudentFee
        fields = [
            'id', 'student', 'student_id_str', 'student_name', 'fee_structure',
            'fee_title', 'due_date', 'discount_amount', 'final_amount',
            'paid_amount', 'due_amount', 'status', 'payments', 'created_at'
        ]
        read_only_fields = ['id', 'final_amount', 'paid_amount', 'due_amount', 'status', 'created_at']
