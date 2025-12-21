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
