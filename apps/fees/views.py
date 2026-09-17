from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import FeeStructure, StudentFee, PaymentRecord
from .serializers import FeeStructureSerializer, StudentFeeSerializer, PaymentRecordSerializer
from apps.accounts.permissions import IsAdminOrStaff, IsOwnerOrAdmin


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.select_related('course', 'academic_year').all()
    serializer_class = FeeStructureSerializer
    filterset_fields = ['course', 'academic_year', 'semester']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


class StudentFeeViewSet(viewsets.ModelViewSet):
    queryset = StudentFee.objects.select_related('student', 'student__user', 'fee_structure').prefetch_related('payments').all()
    serializer_class = StudentFeeSerializer
    filterset_fields = ['student', 'status']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_student:
            return StudentFee.objects.filter(student__user=user).select_related('student', 'student__user', 'fee_structure')
        return super().get_queryset()


class PaymentRecordViewSet(viewsets.ModelViewSet):
    queryset = PaymentRecord.objects.select_related('student_fee', 'student_fee__student').all()
    serializer_class = PaymentRecordSerializer
    filterset_fields = ['student_fee', 'payment_method']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAdminOrStaff]
        return [permission() for permission in permission_classes]


# Web Template Views
@login_required
def fee_dashboard_view(request):
    user = request.user
    if user.is_student:
        student = getattr(user, 'student_profile', None)
        fee_records = StudentFee.objects.filter(student=student).select_related('fee_structure') if student else []
        total_due = sum([f.due_amount for f in fee_records]) if student else 0
        total_paid = sum([f.paid_amount for f in fee_records]) if student else 0
        return render(request, 'fees/student_fees.html', {
            'fee_records': fee_records,
            'total_due': total_due,
            'total_paid': total_paid
        })

    fee_records = StudentFee.objects.select_related('student', 'student__user', 'fee_structure').all()
    fee_structures = FeeStructure.objects.all()
    return render(request, 'fees/fee_management.html', {
        'fee_records': fee_records,
        'fee_structures': fee_structures
    })
