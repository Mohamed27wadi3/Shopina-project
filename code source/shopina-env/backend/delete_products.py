#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from shop.models import Product

# Afficher les anciens produits
old_products = Product.objects.all()
print(f"📦 Nombre total de produits: {old_products.count()}")
for p in old_products[:10]:
    print(f"  - ID {p.id}: {p.name} (Prix: {p.price}, Shop: {p.shop})")

# Supprimer tous les anciens produits
if old_products.exists():
    deleted_count, _ = Product.objects.all().delete()
    print(f"\n✅ {deleted_count} produits supprimés!")
else:
    print("\n✅ Aucun produit à supprimer - base de données déjà vide!")
