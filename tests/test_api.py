from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile

User = get_user_model()


class StudentHubAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='adminapi', password='Password123', role=User.Role.SUPERADMIN, is_staff=True)
        self.student_user = User.objects.create_user(username='studentapi', password='Password123', role=User.Role.STUDENT)
        self.student = StudentProfile.objects.create(user=self.student_user)

    def test_jwt_login_success(self):
        """Test authentication via JWT endpoint."""
        response = self.client.post('/accounts/api/auth/login/', {
            'username': 'studentapi',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_unauthenticated_api_access_blocked(self):
        """Verify protected endpoints return 401 when unauthenticated."""
        response = self.client.get('/students/api/students/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_cannot_access_other_student_profile(self):
        """Verify role-based access control prevents student data leak (returns 404 or 403)."""
        other_user = User.objects.create_user(username='otherstudent', password='Password123', role=User.Role.STUDENT)
        other_student = StudentProfile.objects.create(user=other_user)

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(f'/students/api/students/{other_student.id}/')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
