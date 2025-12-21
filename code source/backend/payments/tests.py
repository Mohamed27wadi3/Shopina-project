from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from orders.models import Order
from shop.models import Category, Product
from unittest.mock import patch


class PaymentsTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='p', email='p@example.com', password='pass')
        cat = Category.objects.create(name='Mode')
        prod = Product.objects.create(name='T-shirt', category=cat, price=19.99)
        self.order = Order.objects.create(user=self.user, total=19.99)

    @patch('payments.views.stripe.PaymentIntent.create')
    def test_create_payment_intent(self, mock_create):
        mock_create.return_value = {'id': 'pi_123', 'client_secret': 'secret_123'}
        # Obtain JWT token
        token_resp = self.client.post(reverse('users:token_obtain_pair'), {'username': 'p', 'password': 'pass'}, format='json')
        self.assertEqual(token_resp.status_code, 200)
        token = token_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('payments:create_intent')
        resp = self.client.post(url, {'order_id': self.order.id}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('client_secret', resp.data)
