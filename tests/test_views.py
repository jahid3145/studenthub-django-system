from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile
from apps.academics.models import Department, Course

User = get_user_model()


class StudentWebViewsTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='adminweb',
            email='adminweb@test.com',
            password='Password123',
            role=User.Role.SUPERADMIN,
            is_staff=True
        )
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(code='BTECH-CSE', name='B.Tech CSE', department=self.dept)

    def test_student_create_view_get(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('students:student_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_form.html')

    def test_student_create_view_post_success(self):
        self.client.force_login(self.admin)
        post_data = {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'first_name': 'New',
            'last_name': 'Student',
            'password': 'Student@123',
            'department': self.dept.id,
            'course': self.course.id,
            'current_semester': 1,
            'gender': 'M',
            'phone': '+91 9999999999',
            'address': 'Campus Hostel A',
            'guardian_name': 'Parent Name',
            'guardian_phone': '+91 8888888888',
            'status': 'ACTIVE'
        }
        response = self.client.post(reverse('students:student_create'), data=post_data)
        self.assertEqual(response.status_code, 302)  # Redirects to detail page
        
        # Verify student created in database
        self.assertTrue(User.objects.filter(username='newstudent').exists())
        self.assertTrue(StudentProfile.objects.filter(user__username='newstudent').exists())

    def test_student_edit_view(self):
        self.client.force_login(self.admin)
        user = User.objects.create_user(username='oldstudent', email='old@example.com', password='Password123', role=User.Role.STUDENT)
        student = StudentProfile.objects.create(user=user, department=self.dept, course=self.course)

        edit_data = {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'updated@example.com',
            'department': self.dept.id,
            'course': self.course.id,
            'current_semester': 2,
            'gender': 'M',
            'phone': '+91 7777777777',
            'address': 'Updated Address',
            'guardian_name': 'Updated Guardian',
            'guardian_phone': '+91 6666666666',
            'status': 'ACTIVE'
        }
        response = self.client.post(reverse('students:student_edit', kwargs={'pk': student.pk}), data=edit_data)
        self.assertEqual(response.status_code, 302)
        
        student.refresh_from_db()
        self.assertEqual(student.user.first_name, 'UpdatedFirst')
        self.assertEqual(student.current_semester, 2)
