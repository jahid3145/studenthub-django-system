from django.db import models


class Department(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="e.g. CSE, ECE, MECH")
    name = models.CharField(max_length=100)
    head_of_department = models.ForeignKey(
        'teachers.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    code = models.CharField(max_length=15, unique=True, help_text="e.g. BTECH-CSE, MBA")
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    duration_years = models.PositiveIntegerField(default=4)
    total_semesters = models.PositiveIntegerField(default=8)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Subject(models.Model):
    code = models.CharField(max_length=15, unique=True, help_text="e.g. CS101, EC204")
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    semester = models.PositiveIntegerField(default=1)
    credits = models.PositiveIntegerField(default=3)
    teacher = models.ForeignKey(
        'teachers.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_subjects'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['semester', 'code']
        unique_together = ['course', 'code']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f"{self.code} - {self.name} (Sem {self.semester})"


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text="e.g. 2025-2026")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class ClassSection(models.Model):
    name = models.CharField(max_length=50, help_text="e.g. CSE-3A")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes')
    semester = models.PositiveIntegerField(default=1)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classes')
    capacity = models.PositiveIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course', 'semester', 'name']
        unique_together = ['name', 'academic_year', 'semester']
        verbose_name = 'Class / Section'
        verbose_name_plural = 'Classes & Sections'

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"
