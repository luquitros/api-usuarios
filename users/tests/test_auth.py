from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class AuthApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teacher',
            password='Teacher123!',
            email='teacher@example.com',
        )
        self.user.profile.user_type = 'professor'
        self.user.profile.save()

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
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

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
                'refresh': login_response.data['data']['refresh'],
            },
            format='json',
        )

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertTrue(logout_response.data['success'])

    def test_login_with_invalid_credentials_returns_friendly_message(self):
        response = self.client.post(
            '/login/',
            {
                'username': 'teacher',
                'password': 'wrong-password',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Credenciais invalidas. Verifique usuario e senha.')
