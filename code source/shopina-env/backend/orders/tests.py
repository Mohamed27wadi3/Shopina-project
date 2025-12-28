from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from shop.models import Product, Category


class OrdersTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='u', email='u@example.com', password='pass')
        cat = Category.objects.create(name='Mode')
        self.p = Product.objects.create(name='T-shirt', category=cat, price=19.99)

    def test_create_order_requires_auth(self):
        url = reverse('orders')
        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, 401)

    def test_full_order_flow(self):
        # Register a new user and obtain token
        reg_url = reverse('users:register')
        data = {'username': 'intuser', 'email': 'int@example.com', 'password': 'P@ssw0rd!'}
        resp = self.client.post(reg_url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)
        token = resp.data['access']

        # Create a product to order
        cat = Category.objects.create(name='Integration')
        prod = Product.objects.create(name='Integration Product', category=cat, price=10.00, stock=5)

        # Create an order using the authenticated client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        orders_url = reverse('orders')
        payload = {'items': [{'product_id': prod.id, 'price': '10.00', 'quantity': 2}]}
        order_resp = self.client.post(orders_url, payload, format='json')
        self.assertEqual(order_resp.status_code, 201)
        self.assertIn('id', order_resp.data)
        self.assertEqual(float(order_resp.data['total']), 20.00)
