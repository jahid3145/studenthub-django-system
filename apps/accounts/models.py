from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Super Admin'
        ADMIN = 'ADMIN', 'Admin / Staff'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Role determining permissions across StudentHub."
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.username}) - {self.get_role_display()}"
        return f"{self.username} - {self.get_role_display()}"

    @property
    def is_superadmin(self):
        return self.role == self.Role.SUPERADMIN or self.is_superuser

    @property
    def is_admin_or_staff(self):
        return self.role in [self.Role.SUPERADMIN, self.Role.ADMIN] or self.is_staff

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT


# Ensure AnonymousUser also safely returns False for role properties
from django.contrib.auth.models import AnonymousUser
AnonymousUser.is_superadmin = property(lambda self: False)
AnonymousUser.is_admin_or_staff = property(lambda self: False)
AnonymousUser.is_teacher = property(lambda self: False)
AnonymousUser.is_student = property(lambda self: False)

