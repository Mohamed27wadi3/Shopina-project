import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
try:
    u, created = User.objects.get_or_create(username='admin')
    u.set_password('admin')
    u.email = 'admin@example.com'
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print(f'SUCCESS: User {u.username} ready.')
except Exception as e:
    print(f'ERROR: {e}')
