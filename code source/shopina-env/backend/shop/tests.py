from django.urls import reverse
from rest_framework.test import APITestCase
from shop.models import Product, Category


class ShopTests(APITestCase):
    def setUp(self):
        cat = Category.objects.create(name='Mode')
        Product.objects.create(name='T-shirt', category=cat, price=19.99)

    def test_products_list(self):
        url = reverse('product-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) >= 1)
