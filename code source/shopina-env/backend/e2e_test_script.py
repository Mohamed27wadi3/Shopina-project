from django.contrib.auth import get_user_model
from django.core.files import File
import os, sys

User = get_user_model()
username = 'e2e_test_user'
pwd = 'Password123'
user, created = User.objects.get_or_create(username=username, defaults={'email':'e2e@example.com'})
if created:
    user.set_password(pwd)
    user.save()
    print('USER_CREATED')
else:
    print('USER_EXISTS')

from shops.models import Shop
shop, screated = Shop.objects.get_or_create(owner=user, defaults={
    'name':'E2E Shop',
    'slug':'e2e-shop',
    'description':'Shop for E2E testing',
    'email':'e2e@example.com'
})
print('SHOP_CREATED' if screated else 'SHOP_EXISTS', shop.id, shop.slug)

from shop.models import Product
img_path = r'D:\Shopina Project\logo and disign\shopina logo.png'
if not os.path.exists(img_path):
    print('IMAGE_NOT_FOUND', img_path)
    sys.exit(1)

prod = Product.objects.create(name='E2E Product Auto', price=9.99, shop=shop, stock=10, description='Auto product')
with open(img_path, 'rb') as f:
    prod.image.save('e2e_auto.png', File(f), save=True)
print('PRODUCT_CREATED', prod.id, prod.image.url)

from carts.services.cart_service import CartService
cs = CartService()
item = cs.add_to_cart(user, prod.id, 2)
print('CART_ITEM_ADDED', item.id, item.product.id, item.quantity, item.price_at_add)
summary = cs.get_cart_summary(user)
print('CART_SUMMARY', summary)
