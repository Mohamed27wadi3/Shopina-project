from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from shops.models import Shop
from shop.models import Product

User = get_user_model()


class ProductAPIOwnerTests(TestCase):
    def setUp(self):
        # Create owner user and shop
        self.owner = User.objects.create_user(username='owner', email='owner@example.com', password='pass')
        self.shop = Shop.objects.create(name='Owner Shop', owner=self.owner)

        # Create another user
        self.other = User.objects.create_user(username='other', email='other@example.com', password='pass')

        # Create product for owner shop
        self.product = Product.objects.create(name='Owner Product', price=5.0, stock=10, shop=self.shop)

        self.client = APIClient()

    def test_owner_can_update_product(self):
        self.client.force_authenticate(self.owner)
        resp = self.client.patch(f'/shop/api/{self.product.id}/update/', {'name': 'Updated Name', 'variants': [{'sku': 'S1'}]}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Name')
        self.assertIsInstance(self.product.variants, list)

    def test_non_owner_cannot_update_product(self):
        self.client.force_authenticate(self.other)
        resp = self.client.patch(f'/shop/api/{self.product.id}/update/', {'name': 'Bad Update'}, format='json')
        self.assertEqual(resp.status_code, 403)

    def test_owner_can_delete_product(self):
        self.client.force_authenticate(self.owner)
        resp = self.client.delete(f'/shop/api/{self.product.id}/delete/')
        # delete returns 204 with message
        self.assertIn(resp.status_code, (200, 204))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_non_owner_cannot_delete_product(self):
        # recreate product
        p = Product.objects.create(name='Other Product', price=3.0, stock=2, shop=self.shop)
        self.client.force_authenticate(self.other)
        resp = self.client.delete(f'/shop/api/{p.id}/delete/')
        self.assertEqual(resp.status_code, 403)
