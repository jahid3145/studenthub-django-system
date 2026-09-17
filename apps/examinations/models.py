from django.db import models


class Exam(models.Model):
    class ExamType(models.TextChoices):
        INTERNAL = 'INTERNAL', 'Internal Assessment'
        MIDTERM = 'MIDTERM', 'Mid-Term Examination'
        FINAL = 'FINAL', 'Final Semester Examination'
        QUIZ = 'QUIZ', 'Quiz / Test'

    name = models.CharField(max_length=150)
    exam_type = models.CharField(max_length=20, choices=ExamType.choices, default=ExamType.MIDTERM)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='exams')
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def __str__(self):
        return f"{self.name} ({self.get_exam_type_display()})"


class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='exam_schedules')
    class_section = models.ForeignKey('academics.ClassSection', on_delete=models.CASCADE, related_name='exam_schedules')
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)

    class Meta:
        ordering = ['exam_date', 'start_time']
        unique_together = ['exam', 'subject', 'class_section']
        verbose_name = 'Exam Schedule'
        verbose_name_plural = 'Exam Schedules'

    def __str__(self):
        return f"{self.exam.name} - {self.subject.code} on {self.exam_date}"


class ExamResult(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='exam_results')
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    letter_grade = models.CharField(max_length=5, blank=True)
    grade_point = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    is_pass = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    entered_by = models.ForeignKey(
        'teachers.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entered_exam_results'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student__student_id']
        unique_together = ['student', 'exam_schedule']
        verbose_name = 'Exam Result'
        verbose_name_plural = 'Exam Results'

    def __str__(self):
        return f"{self.student.student_id} - {self.exam_schedule.subject.code}: {self.marks_obtained}/{self.exam_schedule.max_marks}"

    def calculate_grade(self):
        max_m = self.exam_schedule.max_marks
        pass_m = self.exam_schedule.passing_marks
        pct = (float(self.marks_obtained) / float(max_m)) * 100 if max_m > 0 else 0.0

        self.is_pass = float(self.marks_obtained) >= float(pass_m)

        if pct >= 90.0:
            self.letter_grade, self.grade_point = 'A+', 10.0
        elif pct >= 80.0:
            self.letter_grade, self.grade_point = 'A', 9.0
        elif pct >= 70.0:
            self.letter_grade, self.grade_point = 'B+', 8.0
        elif pct >= 60.0:
            self.letter_grade, self.grade_point = 'B', 7.0
        elif pct >= 50.0:
            self.letter_grade, self.grade_point = 'C', 6.0
        elif pct >= 40.0:
            self.letter_grade, self.grade_point = 'D', 5.0
        else:
            self.letter_grade, self.grade_point = 'F', 0.0

    def save(self, *args, **kwargs):
        self.calculate_grade()
        super().save(*args, **kwargs)
