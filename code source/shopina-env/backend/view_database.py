import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from users.models import User
from shop.models import Product
from shops.models import Shop
from orders.models import Order, OrderItem

print("=" * 70)
print("📊 VOTRE BASE DE DONNÉES SHOPINA")
print("=" * 70)

print("\n👥 UTILISATEURS:")
print(f"   Total: {User.objects.count()}")
for u in User.objects.all():
    print(f"   - {u.username} ({u.email}) - Role: {u.role}")

print("\n🛍️ PRODUITS:")
print(f"   Total: {Product.objects.count()}")
for p in Product.objects.all():
    print(f"   - {p.name} - Prix: {p.price} DA - Stock: {p.stock}")

print("\n🏪 BOUTIQUES:")
print(f"   Total: {Shop.objects.count()}")
for s in Shop.objects.all():
    print(f"   - {s.name} (Propriétaire: {s.owner.username})")

print("\n📦 COMMANDES:")
print(f"   Total: {Order.objects.count()}")
for o in Order.objects.all():
    print(f"   - Commande #{o.id} - Client: {o.user.username} - Total: {o.total} DA - Statut: {o.status} - Date: {o.created_at.strftime('%d/%m/%Y')}")
    for item in o.items.all():
        print(f"      └─ {item.product.name if item.product else 'Produit supprimé'} x{item.quantity} @ {item.price} DA")

print("\n" + "=" * 70)
