from django.db import models
from django.conf import settings
from datetime import datetime


class StudentProfile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        GRADUATED = 'GRADUATED', 'Graduated'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        INACTIVE = 'INACTIVE', 'Inactive'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    student_id = models.CharField(max_length=20, unique=True, help_text="e.g. STU-2026-001")
    department = models.ForeignKey(
        'academics.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    course = models.ForeignKey(
        'academics.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    current_semester = models.PositiveIntegerField(default=1)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, default=GenderChoices.MALE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name() or self.user.username}"

    def save(self, *args, **kwargs):
        if not self.student_id:
            year = datetime.now().year
            count = StudentProfile.objects.count() + 1
            self.student_id = f"STU-{year}-{count:03d}"
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    class_section = models.ForeignKey('academics.ClassSection', on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='enrollments')
    semester = models.PositiveIntegerField(default=1)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-academic_year', 'semester']
        unique_together = ['student', 'class_section', 'academic_year']
        verbose_name = 'Student Enrollment'
        verbose_name_plural = 'Student Enrollments'

    def __str__(self):
        return f"{self.student.student_id} in {self.class_section.name} ({self.academic_year.name})"


class StudentDocument(models.Model):
    class DocumentType(models.TextChoices):
        IDENTITY_PROOF = 'IDENTITY', 'Identity Proof'
        MARKSHEET = 'MARKSHEET', 'Marksheet'
        CERTIFICATE = 'CERTIFICATE', 'Certificate'
        OTHER = 'OTHER', 'Other'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=150)
    document_type = models.CharField(max_length=20, choices=DocumentType.choices, default=DocumentType.OTHER)
    file = models.FileField(upload_to='student_documents/')
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Student Document'
        verbose_name_plural = 'Student Documents'

    def __str__(self):
        return f"{self.title} - {self.student.student_id}"
