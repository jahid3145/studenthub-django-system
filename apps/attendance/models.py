from django.db import models


class AttendanceSession(models.Model):
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='attendance_sessions')
    class_section = models.ForeignKey('academics.ClassSection', on_delete=models.CASCADE, related_name='attendance_sessions')
    date = models.DateField()
    marked_by = models.ForeignKey(
        'teachers.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendance_sessions'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        unique_together = ['subject', 'class_section', 'date']
        verbose_name = 'Attendance Session'
        verbose_name_plural = 'Attendance Sessions'

    def __str__(self):
        return f"{self.subject.code} - {self.class_section.name} on {self.date}"


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'P', 'Present'
        ABSENT = 'A', 'Absent'
        LATE = 'L', 'Late'
        EXCUSED = 'E', 'Excused'

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PRESENT)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['student__student_id']
        unique_together = ['session', 'student']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.student.student_id} - {self.get_status_display()}"
