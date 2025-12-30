import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','shopina.settings')
import django
django.setup()
from rest_framework.test import APIRequestFactory
from shops.models import Shop
from shop.models import Product
from shop.views import update_product_api, delete_product_api
from django.contrib.auth import get_user_model

User = get_user_model()
shop = Shop.objects.first()
if not shop:
    print('NO_SHOP')
    raise SystemExit(0)
owner = shop.owner
product, created = Product.objects.get_or_create(name='SMOKE Test Product', shop=shop, defaults={'price':9.99, 'stock':10})
print('PRODUCT', product.id, 'created=', created)

factory = APIRequestFactory()
req = factory.patch(f'/shop/api/{product.id}/update/', {'name':'SMOKE Updated','variants':[{'sku':'SKU1','price':9.99}]}, format='json')
req.user = owner
resp = update_product_api(req, product_id=product.id)
print('UPDATE RESP TYPE:', type(resp), 'STATUS:', getattr(resp, 'status_code', None))
print('UPDATED NAME:', Product.objects.get(id=product.id).name)

non_owner, _ = User.objects.get_or_create(username='e2e_non_owner', defaults={'email':'e2e_non_owner@example.com'})
req2 = factory.delete(f'/shop/api/{product.id}/delete/')
req2.user = non_owner
resp2 = delete_product_api(req2, product_id=product.id)
print('DELETE BY NON-OWNER STATUS:', getattr(resp2, 'status_code', None), 'CONTENT:', getattr(resp2, 'data', None))

req3 = factory.delete(f'/shop/api/{product.id}/delete/')
req3.user = owner
resp3 = delete_product_api(req3, product_id=product.id)
print('DELETE BY OWNER STATUS:', getattr(resp3, 'status_code', None), 'DATA:', getattr(resp3, 'data', None))
print('PRODUCT EXISTS AFTER DELETE:', Product.objects.filter(id=product.id).exists())
