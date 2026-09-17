from django.db import models
from django.utils import timezone


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='assignments')
    class_section = models.ForeignKey('academics.ClassSection', on_delete=models.CASCADE, related_name='assignments')
    created_by = models.ForeignKey('teachers.TeacherProfile', on_delete=models.SET_NULL, null=True, related_name='created_assignments')
    due_date = models.DateTimeField()
    max_marks = models.PositiveIntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-due_date']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'

    def __str__(self):
        return f"{self.title} ({self.subject.code})"

    @property
    def is_overdue(self):
        return timezone.now() > self.due_date


class AssignmentSubmission(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Submitted'
        LATE = 'LATE', 'Submitted Late'
        GRADED = 'GRADED', 'Graded'

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='assignment_submissions')
    submission_text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.SUBMITTED)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey('teachers.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['assignment', 'student']
        verbose_name = 'Assignment Submission'
        verbose_name_plural = 'Assignment Submissions'

    def __str__(self):
        return f"{self.student.student_id} - {self.assignment.title}"

    def save(self, *args, **kwargs):
        if self.marks_obtained is not None:
            self.status = self.Status.GRADED
        elif self.submitted_at and self.assignment.due_date and self.submitted_at > self.assignment.due_date:
            self.status = self.Status.LATE
        super().save(*args, **kwargs)
