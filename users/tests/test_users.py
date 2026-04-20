from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class UserApiTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            password='Admin123!',
            email='admin@example.com',
        )
        self.admin_user.profile.user_type = 'admin'
        self.admin_user.profile.save()

        self.student_user = User.objects.create_user(
            username='student',
            password='Student123!',
            email='student@example.com',
        )
        self.student_user.profile.user_type = 'aluno'
        self.student_user.profile.save()

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
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'teacher')

    def test_me_returns_authenticated_user_data(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get('/users/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], 'student')
        self.assertEqual(response.data['data']['profile']['user_type'], 'aluno')

    def test_non_admin_cannot_list_users(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.get('/users/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'Voce nao tem permissao para executar esta acao.')

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('items', response.data['data'])
        self.assertGreaterEqual(len(response.data['data']['items']), 2)

    def test_public_signup_cannot_create_admin_user(self):
        response = self.client.post(
            '/users/',
            {
                'username': 'intruder',
                'password': 'Intruder123!',
                'email': 'intruder@example.com',
                'profile': {
                    'user_type': 'admin',
                },
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Dados invalidos. Revise os campos e tente novamente.')
        self.assertIn('errors', response.data)
        self.assertIn('profile', response.data['errors'])

    def test_admin_can_filter_users_by_user_type(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/users/?profile__user_type=aluno')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['items']), 1)
        self.assertEqual(response.data['data']['items'][0]['username'], 'student')

    def test_admin_can_search_users(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/users/?search=student')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['items']), 1)
        self.assertEqual(response.data['data']['items'][0]['username'], 'student')

    def test_user_can_patch_self_with_same_email(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.patch(
            '/users/me/',
            {
                'email': 'student@example.com',
                'first_name': 'Student',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'student@example.com')

    def test_superuser_is_treated_as_admin_in_api(self):
        superuser = User.objects.create_superuser(
            username='root',
            password='Root123!Pass',
            email='root@example.com',
        )
        self.client.force_authenticate(user=superuser)

        response = self.client.get('/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
