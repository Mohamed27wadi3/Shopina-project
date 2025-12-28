from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.filter(username='admin').first()
if admin:
    print(f'Admin exists: {admin.email}')
else:
    admin = User.objects.create_superuser('admin', 'admin@shopina.local', 'admin123')
    print(f'Created admin: {admin.email}')
