import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.filter(username='admin').first()
if u:
    print(f'STATUS: User {u.username} exists, Staff={u.is_staff}, Super={u.is_superuser}')
else:
    print('STATUS: User admin NOT FOUND')
