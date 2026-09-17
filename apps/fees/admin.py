from django.contrib import admin
from .models import FeeStructure, StudentFee, PaymentRecord


class PaymentRecordInline(admin.TabularInline):
    model = PaymentRecord
    extra = 0


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'academic_year', 'semester', 'total_amount', 'due_date']
    list_filter = ['course', 'academic_year', 'semester']
    search_fields = ['title']


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_structure', 'final_amount', 'paid_amount', 'due_amount', 'status']
    list_filter = ['status', 'fee_structure__course']
    search_fields = ['student__student_id', 'student__user__first_name']
    inlines = [PaymentRecordInline]


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'student_fee', 'amount', 'payment_method', 'payment_date']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['transaction_id', 'student_fee__student__student_id']
