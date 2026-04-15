from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Profile


class AuthApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teacher',
            password='Teacher123!',
            email='teacher@example.com',
        )
        Profile.objects.create(user=self.user, user_type='professor')

    def test_login_returns_tokens(self):
        response = self.client.post(
            '/login/',
            {
                'username': 'teacher',
                'password': 'Teacher123!',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout_blacklists_refresh_token(self):
        login_response = self.client.post(
            '/login/',
            {
                'username': 'teacher',
                'password': 'Teacher123!',
            },
            format='json',
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        logout_response = self.client.post(
            '/logout/',
            {
                'refresh': login_response.data['refresh'],
            },
            format='json',
        )

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
