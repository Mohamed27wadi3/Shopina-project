# DESIGN PATTERNS UTILISÉS DANS CE FICHIER
# ==========================================
#
# 1. DECORATOR PATTERN (@admin.register):
# - Ajoute des fonctionnalités à une classe (CategoryAdmin)
# - Sans modifier la classe originale
# - Le décorateur @admin.register enregistre automatiquement l'admin
#
# 2. ADAPTER PATTERN (ModelAdmin):
# - Adapte le Model Django pour l'interface Admin
# - Transforme Category Model en interface admin personnalisée
# - Permet de personnaliser l'affichage (list_display, search_fields)
#
# 3. CONFIGURATION PATTERN:
# - Centralise la configuration de l'admin
# - list_display: quels champs afficher
# - search_fields: quels champs sont searchables
# - list_filter: quels champs filtrer
#
# AVANTAGES:
# ✅ Interface admin auto-générée
# ✅ Facile de personnaliser
# ✅ Pas besoin de code HTML/CSS

from django.contrib import admin
from .models import Category, Product


# DECORATOR PATTERN: @admin.register enregistre automatiquement
# ADAPTER PATTERN: CategoryAdmin adapte Category pour l'admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface pour Category.
    Decorator Pattern: @admin.register enregistre automatiquement cette classe.
    """
    # Quels champs afficher dans la liste
    list_display = ('id', 'name')
    # Quels champs utiliser pour la recherche
    search_fields = ('name',)


# DECORATOR PATTERN: @admin.register enregistre automatiquement
# ADAPTER PATTERN: ProductAdmin adapte Product pour l'admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface pour Product.
    Adapter Pattern: transforme Product Model en interface admin.
    """
    # Quels champs afficher dans la liste
    list_display = ('id', 'name', 'category', 'price', 'stock')
    # Quels champs utiliser pour la recherche
    search_fields = ('name', 'category__name')
    # Quels champs utiliser pour les filtres
    list_filter = ('category',)
