from django.db import models
from django.conf import settings
from django.utils import timezone


class Notice(models.Model):
    class Audience(models.TextChoices):
        ALL = 'ALL', 'All Users'
        DEPARTMENT = 'DEPARTMENT', 'Specific Department'
        COURSE = 'COURSE', 'Specific Course'
        CLASS = 'CLASS', 'Specific Class Section'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        NORMAL = 'NORMAL', 'Normal'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_notices')
    target_audience = models.CharField(max_length=15, choices=Audience.choices, default=Audience.ALL)
    department = models.ForeignKey('academics.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='notices')
    course = models.ForeignKey('academics.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='notices')
    class_section = models.ForeignKey('academics.ClassSection', on_delete=models.SET_NULL, null=True, blank=True, related_name='notices')
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.NORMAL)
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title}"

    @property
    def is_expired(self):
        if self.expiry_date:
            return timezone.now().date() > self.expiry_date
        return False
