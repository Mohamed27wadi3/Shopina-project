"""
Script pour activer la boutique "belaid auto"
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from shops.models import Shop
from shop.models import Product

# Chercher la boutique belaid
shop = Shop.objects.filter(name__icontains='belaid').first()

if not shop:
    print("❌ Boutique 'belaid' non trouvée")
    print("\n📋 Boutiques disponibles:")
    for s in Shop.objects.all():
        print(f"   • {s.name} (slug: {s.slug}, active: {s.is_active})")
    sys.exit(1)

print("=" * 60)
print(f"🏪 Boutique: {shop.name}")
print(f"   Slug: {shop.slug}")
print(f"   Active: {'✅ OUI' if shop.is_active else '❌ NON'}")
print(f"   Propriétaire: {shop.owner.username if shop.owner else 'N/A'}")

products = Product.objects.filter(shop=shop)
print(f"   Produits: {products.count()}")

if products.exists():
    print("\n   📦 Premiers produits:")
    for p in products[:5]:
        print(f"      • {p.name} - {p.price}€")

print("\n   🌐 URL publique: /shop/" + shop.slug)
print("=" * 60)

# Activer si nécessaire
if not shop.is_active:
    print("\n⚙️ Activation de la boutique...")
    shop.is_active = True
    shop.save()
    print("✅ Boutique activée avec succès!")
else:
    print("\n✅ La boutique est déjà active")

print(f"\n💡 Accédez à votre boutique: http://localhost:3001/shop/{shop.slug}")
