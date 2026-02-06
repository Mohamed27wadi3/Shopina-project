"""
Script de diagnostic pour vérifier les boutiques et leurs produits
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from shops.models import Shop
from shop.models import Product

print("=" * 60)
print("📊 DIAGNOSTIC DES BOUTIQUES")
print("=" * 60)

shops = Shop.objects.all()

if not shops.exists():
    print("❌ Aucune boutique trouvée dans la base de données")
    sys.exit(0)

for shop in shops:
    products = Product.objects.filter(shop=shop)
    print(f"\n🏪 Boutique: {shop.name}")
    print(f"   └─ Slug: {shop.slug}")
    print(f"   └─ Propriétaire: {shop.owner.username if shop.owner else 'N/A'}")
    print(f"   └─ Active: {'✅ OUI' if shop.is_active else '❌ NON'}")
    print(f"   └─ Nombre de produits: {products.count()}")
    
    if products.exists():
        print(f"   └─ Produits:")
        for p in products[:5]:  # Afficher max 5 produits
            print(f"      • {p.name} - {p.price}€ (stock: {p.stock})")
        if products.count() > 5:
            print(f"      ... et {products.count() - 5} autres produits")
    
    # Afficher l'URL publique
    print(f"   └─ URL publique: /shop/api/public/{shop.slug}/products/")
    
    # Vérifier si accessible
    if not shop.is_active:
        print(f"   └─ ⚠️ PROBLÈME: Boutique pas active, URL publique retournera 403")
    elif products.count() == 0:
        print(f"   └─ ⚠️ AVERTISSEMENT: Aucun produit, la page sera vide")
    else:
        print(f"   └─ ✅ OK: Boutique accessible publiquement avec {products.count()} produit(s)")

print("\n" + "=" * 60)
print("💡 Pour activer une boutique: python activate_shop.py <slug>")
print("=" * 60)
