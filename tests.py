from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Profile


class UserApiTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            password='Admin123!',
            email='admin@example.com',
        )
        Profile.objects.create(user=self.admin_user, user_type='admin')

        self.student_user = User.objects.create_user(
            username='student',
            password='Student123!',
            email='student@example.com',
        )
        Profile.objects.create(user=self.student_user, user_type='aluno')

    def test_signup_creates_profile(self):
        response = self.client.post(
            '/users/',
            {
                'username': 'teacher',
                'password': 'Teacher123!',
                'email': 'teacher@example.com',
                'first_name': 'Ada',
                'last_name': 'Lovelace',
                'profile': {
                    'user_type': 'professor',
                    'phone': '11999999999',
                    'bio': 'Docente de matematica.',
                },
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.get(username='teacher')
        self.assertEqual(created_user.profile.user_type, 'professor')

    def test_me_returns_authenticated_user_data(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get('/users/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'student')
        self.assertEqual(response.data['profile']['user_type'], 'aluno')

    def test_non_admin_cannot_list_users(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get('/users/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)
