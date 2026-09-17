from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal

from apps.academics.models import Department, Course, Subject, AcademicYear, ClassSection
from apps.teachers.models import TeacherProfile
from apps.students.models import StudentProfile
from apps.examinations.models import Exam, ExamSchedule, ExamResult
from apps.fees.models import FeeStructure, StudentFee

User = get_user_model()


class StudentHubModelTests(TestCase):
    def setUp(self):
        self.year = AcademicYear.objects.create(
            name='2025-2026', start_date=date(2025, 8, 1), end_date=date(2026, 6, 30), is_current=True
        )
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(code='BTECH-CSE', name='B.Tech CSE', department=self.dept)
        self.subject = Subject.objects.create(code='CS101', name='Data Structures', course=self.course, semester=1, credits=4)
        self.class_sec = ClassSection.objects.create(name='CSE-1A', course=self.course, semester=1, academic_year=self.year)

        self.student_user = User.objects.create_user(username='teststudent', email='student@test.com', password='password123', role=User.Role.STUDENT)
        self.student = StudentProfile.objects.create(user=self.student_user, department=self.dept, course=self.course)

        self.teacher_user = User.objects.create_user(username='testteacher', email='teacher@test.com', password='password123', role=User.Role.TEACHER)
        self.teacher = TeacherProfile.objects.create(user=self.teacher_user, department=self.dept)

    def test_auto_generated_ids(self):
        """Verify Student ID and Employee ID auto-generation format."""
        self.assertTrue(self.student.student_id.startswith('STU-'))
        self.assertTrue(self.teacher.employee_id.startswith('EMP-'))

    def test_automated_grade_calculation(self):
        """Verify letter grade and pass status calculation."""
        exam = Exam.objects.create(name='Midterm', academic_year=self.year, start_date=date.today(), end_date=date.today())
        sched = ExamSchedule.objects.create(exam=exam, subject=self.subject, class_section=self.class_sec, exam_date=date.today(), start_time='10:00', end_time='12:00', max_marks=100, passing_marks=40)

        result = ExamResult.objects.create(student=self.student, exam_schedule=sched, marks_obtained=85.0)
        self.assertEqual(result.letter_grade, 'A')
        self.assertTrue(result.is_pass)

        failed_result = ExamResult.objects.create(
            student=StudentProfile.objects.create(user=User.objects.create_user(username='failingstudent', role=User.Role.STUDENT)),
            exam_schedule=sched,
            marks_obtained=30.0
        )
        self.assertEqual(failed_result.letter_grade, 'F')
        self.assertFalse(failed_result.is_pass)

    def test_fee_totals_and_status(self):
        """Verify Fee final amount and status updating logic."""
        fee_struct = FeeStructure.objects.create(course=self.course, academic_year=self.year, semester=1, title='Tuition Fee', total_amount=Decimal('1000.00'), due_date=date.today())
        stu_fee = StudentFee.objects.create(student=self.student, fee_structure=fee_struct, discount_amount=Decimal('100.00'))

        self.assertEqual(stu_fee.final_amount, Decimal('900.00'))
        self.assertEqual(stu_fee.due_amount, Decimal('900.00'))
        self.assertEqual(stu_fee.status, StudentFee.Status.UNPAID)
