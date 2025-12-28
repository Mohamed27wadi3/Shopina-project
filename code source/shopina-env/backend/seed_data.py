from django.contrib.auth import get_user_model
from shop.models import Product

# Create users if missing
User = get_user_model()
for i in range(1, 4):
    u, _ = User.objects.get_or_create(
        username=f'customer_{i}',
        defaults={'email': f'cust{i}@shopina.local', 'first_name': f'Client {i}'}
    )
    if _:
        u.set_password('pass123')
        u.save()

print(f"Users: {User.objects.count()}")
print(f"Products: {Product.objects.count()}")
