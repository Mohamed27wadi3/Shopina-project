from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class UserTests(APITestCase):
    def test_register_and_token(self):
        url = reverse('users:register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'P@ssw0rd!', 'password_confirm': 'P@ssw0rd!'}
        resp = self.client.post(url, data)
        # Accept 201 Created or 200 OK depending on implementation
        self.assertIn(resp.status_code, (200, 201))
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_profile_requires_auth(self):
        url = reverse('users:profile')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

    def _get_token_for_user(self, username='pwuser', email='pw@example.com', password='StrongPassw0rd!'):
        User = get_user_model()
        user = User.objects.create_user(username=username, email=email, password=password)
        url = reverse('users:token_obtain_pair')
        resp = self.client.post(url, {'username': username, 'password': password})
        self.assertEqual(resp.status_code, 200)
        return resp.data['access']

    def test_change_password_success(self):
        token = self._get_token_for_user()
        url = reverse('users:change_password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.post(url, {
            'old_password': 'StrongPassw0rd!',
            'new_password': 'An0ther_StrongPass!',
            'new_password_confirm': 'An0ther_StrongPass!'
        })
        self.assertEqual(resp.status_code, 200)
        # Fetch the user again and verify password changed
        User = get_user_model()
        user = User.objects.get(username='pwuser')
        self.assertTrue(user.check_password('An0ther_StrongPass!'))
        self.assertIsNotNone(user.last_password_change)

    def test_change_password_wrong_old(self):
        token = self._get_token_for_user(username='wrongold', email='wo@example.com')
        url = reverse('users:change_password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # Trying without 2FA should be forbidden when 2FA is enabled
        User = get_user_model()
        u = User.objects.get(username='wrongold')
        u.two_factor_enabled = True
        u.save()

        resp = self.client.post(url, {
            'old_password': 'incorrect',
            'new_password': 'S0m3NewPass!',
            'new_password_confirm': 'S0m3NewPass!'
        })
        self.assertEqual(resp.status_code, 403)

        # Now start 2FA and verify
        start_url = reverse('users:2fa_start')
        resp = self.client.post(start_url)
        self.assertEqual(resp.status_code, 200)
        # In DEBUG mode, debug_otp should be available
        otp = resp.data.get('debug_otp')
        self.assertIsNotNone(otp)

        verify_url = reverse('users:2fa_verify')
        resp = self.client.post(verify_url, {'otp': otp})
        self.assertEqual(resp.status_code, 200)

        # Now try change password again
        resp = self.client.post(url, {
            'old_password': 'incorrect',
            'new_password': 'S0m3NewPass!',
            'new_password_confirm': 'S0m3NewPass!'
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.data)
    def test_change_password_weak_new(self):
        token = self._get_token_for_user(username='weakpw', email='weak@example.com')
        url = reverse('users:change_password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.post(url, {
            'old_password': 'StrongPassw0rd!',
            'new_password': '12345',
            'new_password_confirm': '12345'
        })
        self.assertEqual(resp.status_code, 400)
        # Response should indicate password validation failure
        self.assertTrue(
            ('new_password' in str(resp.data)) or ('error' in resp.data),
            msg=f"Unexpected response body: {resp.data}"
        )

    def test_update_shop_settings(self):
        token = self._get_token_for_user(username='shopuser', email='shop@example.com')
        url = reverse('users:profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.patch(url, {
            'shop_name': 'Ma Boutique Test',
            'shop_slug': 'ma-boutique-test'
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get('shop_name'), 'Ma Boutique Test')
        self.assertEqual(resp.data.get('shop_slug'), 'ma-boutique-test')

    def test_enable_two_factor_flow(self):
        token = self._get_token_for_user(username='twofauser', email='tf@example.com')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Start 2FA
        start_url = reverse('users:2fa_start')
        resp = self.client.post(start_url)
        self.assertEqual(resp.status_code, 200)
        otp = resp.data.get('debug_otp')
        self.assertIsNotNone(otp)

        # Verify and request enabling 2FA
        verify_url = reverse('users:2fa_verify')
        resp = self.client.post(verify_url, {'otp': otp, 'enable': True}, format='json')
        self.assertEqual(resp.status_code, 200)

        # Retrieve user and assert two_factor_enabled True
        User = get_user_model()
        user = User.objects.get(username='twofauser')
        self.assertTrue(user.two_factor_enabled)

