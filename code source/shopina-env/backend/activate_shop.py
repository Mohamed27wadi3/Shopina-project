"""
Script pour activer une boutique par son slug
Usage: python activate_shop.py <slug>
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from shops.models import Shop

def activate_shop(slug):
    try:
        shop = Shop.objects.get(slug=slug)
        if shop.is_active:
            print(f"✅ La boutique '{slug}' est déjà active")
        else:
            shop.is_active = True
            shop.save()
            print(f"✅ Boutique '{slug}' activée avec succès!")
        
        print(f"\n📊 Informations de la boutique:")
        print(f"   - Nom: {shop.name}")
        print(f"   - Slug: {shop.slug}")
        print(f"   - Propriétaire: {shop.owner.username}")
        print(f"   - Active: {shop.is_active}")
        print(f"   - Produits: {shop.products.count()}")
        
    except Shop.DoesNotExist:
        print(f"❌ Aucune boutique trouvée avec le slug '{slug}'")
        print(f"\n📋 Boutiques disponibles:")
        for s in Shop.objects.all():
            print(f"   - {s.slug} ({s.name}) - Active: {s.is_active}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python activate_shop.py <slug>")
        print("\n📋 Boutiques disponibles:")
        for s in Shop.objects.all():
            print(f"   - {s.slug} ({s.name}) - Active: {s.is_active}")
        sys.exit(1)
    
    activate_shop(sys.argv[1])
