import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','shopina.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client
from shop.models import Product

User = get_user_model()

user = User.objects.filter(username='e2e_test_user').first()
if not user:
    print('TEST USER NOT FOUND')
    raise SystemExit(1)

prod = Product.objects.filter(name__icontains='E2E Product Auto').first()
if not prod:
    print('TEST PRODUCT NOT FOUND')
    raise SystemExit(1)

refresh = RefreshToken.for_user(user)
access = str(refresh.access_token)

c = Client()
headers = {'HTTP_AUTHORIZATION': f'Bearer {access}', 'HTTP_HOST': 'localhost:8000'}

import json
print('Posting to /api/carts/items/ with product', prod.id)
resp = c.post('/api/carts/items/', data=json.dumps({'product_id': prod.id, 'quantity': 1}), content_type='application/json', **headers)
print('POST STATUS', resp.status_code)
print(resp.content.decode('utf-8'))

resp2 = c.get('/api/carts/', **headers)
print('GET CART STATUS', resp2.status_code)
print(resp2.content.decode('utf-8'))
