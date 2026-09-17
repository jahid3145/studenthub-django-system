from django.db import models
from django.utils import timezone
import uuid


class FeeStructure(models.Model):
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='fee_structures')
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='fee_structures')
    semester = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=150, help_text="e.g. B.Tech Sem 1 Tuition & Lab Fee")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']
        unique_together = ['course', 'academic_year', 'semester', 'title']
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fee Structures'

    def __str__(self):
        return f"{self.title} - ₹{self.total_amount}"


class StudentFee(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PARTIAL = 'PARTIAL', 'Partially Paid'
        PAID = 'PAID', 'Paid'
        OVERDUE = 'OVERDUE', 'Overdue'

    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='fees')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='student_fees')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'fee_structure']
        verbose_name = 'Student Fee Record'
        verbose_name_plural = 'Student Fee Records'

    def __str__(self):
        return f"{self.student.student_id} - {self.fee_structure.title} ({self.status})"

    def update_totals_and_status(self):
        from decimal import Decimal
        self.final_amount = max(Decimal('0.00'), Decimal(str(self.fee_structure.total_amount)) - Decimal(str(self.discount_amount)))
        self.due_amount = max(Decimal('0.00'), Decimal(str(self.final_amount)) - Decimal(str(self.paid_amount)))

        if self.due_amount <= Decimal('0.00'):
            self.status = self.Status.PAID
        elif Decimal(str(self.paid_amount)) > Decimal('0.00'):
            self.status = self.Status.PARTIAL
        elif self.fee_structure.due_date < timezone.now().date():
            self.status = self.Status.OVERDUE
        else:
            self.status = self.Status.UNPAID

    def save(self, *args, **kwargs):
        self.update_totals_and_status()
        super().save(*args, **kwargs)


class PaymentRecord(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Cash'
        BANK_TRANSFER = 'BANK', 'Bank Transfer'
        ONLINE_SIMULATION = 'ONLINE', 'Online Simulation'

    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.ONLINE_SIMULATION)
    notes = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Payment Record'
        verbose_name_plural = 'Payment Records'

    def __str__(self):
        return f"{self.transaction_id} - ₹{self.amount} for {self.student_fee.student.student_id}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

        # Sync paid amount back to StudentFee
        from decimal import Decimal
        tot_paid = Decimal(str(sum([p.amount for p in self.student_fee.payments.all()])))
        self.student_fee.paid_amount = tot_paid
        self.student_fee.save()
