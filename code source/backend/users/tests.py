from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class UserTests(APITestCase):
    def test_register_and_token(self):
        url = reverse('users:register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'P@ssw0rd!'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_profile_requires_auth(self):
        url = reverse('users:profile')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
