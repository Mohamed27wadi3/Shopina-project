# DESIGN PATTERNS UTILISÉS DANS CE FICHIER
# ==========================================
#
# 1. ROUTER PATTERN (Django REST Framework):
# - Mappe automatiquement les URLs aux ViewSets
# - Crée les routes CRUD automatiquement
# - Pattern utilisé: router.register() pour ProductViewSet et CategoryViewSet
#
# 2. ROUTING PATTERN (MVC):
# - Associe les URLs aux contrôleurs (Views/ViewSets)
# - Centralise la configuration des routes
# - Facile de modifier les URLs sans toucher au code métier
#
# FLUX DE ROUTING:
# Requête HTTP → URL Matcher (urls.py) → VIEW correspondante
#
# AVANTAGES:
# ✅ URLs centralisées (facile à modifier)
# ✅ Cohérence (tous les routes au même endroit)
# ✅ Automatisation (Router crée les CRUD routes)

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryViewSet,
    ProductViewSet,
    create_product_api,
    public_shop_products,
    merchant_shop_products,
    update_product_api,
    delete_product_api,
    announcements_list,
    public_shop_announcements,
)

# ROUTER PATTERN: Crée automatiquement les routes CRUD
router = DefaultRouter()
# Mappe ProductViewSet → /products/ avec tous les endpoints CRUD
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Routes automatiques du ROUTER PATTERN
    path('', include(router.urls)),
    # Routes personnalisées
    path('create/', create_product_api, name='api-create-product'),
    path('my-products/', merchant_shop_products, name='api-merchant-products'),
    path('public/<slug:slug>/products/', public_shop_products, name='api-public-products'),
    path('<int:product_id>/update/', update_product_api, name='api-update-product'),
    path('<int:product_id>/delete/', delete_product_api, name='api-delete-product'),
    path('announcements/', announcements_list, name='api-announcements'),
    path('public/<slug:slug>/announcements/', public_shop_announcements, name='api-public-announcements'),
]
