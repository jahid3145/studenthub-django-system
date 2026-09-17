from django.db import models
from django.conf import settings
from datetime import datetime


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True, help_text="e.g. EMP-2026-001")
    department = models.ForeignKey(
        'academics.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers'
    )
    designation = models.CharField(max_length=100, default='Assistant Professor')
    qualification = models.CharField(max_length=150, blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            year = datetime.now().year
            count = TeacherProfile.objects.count() + 1
            self.employee_id = f"EMP-{year}-{count:03d}"
        super().save(*args, **kwargs)
