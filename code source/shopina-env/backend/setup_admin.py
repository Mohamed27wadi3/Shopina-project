import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Créer/réinitialiser le mot de passe admin
admin_user, created = User.objects.get_or_create(username='admin')
admin_user.set_password('Admin123456!')
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()

print("=" * 60)
print("✅ ACCÈS ADMIN CONFIGURÉ")
print("=" * 60)
print("\n🔓 Identifiants de connexion:")
print("   Utilisateur: admin")
print("   Mot de passe: Admin123456!")
print("\n📍 URL d'administration:")
print("   http://127.0.0.1:8000/admin/")
print("\n" + "=" * 60)
