# PATTERN MVC: MODEL (M)
# ========================
#
# Les Models Django définissent la STRUCTURE DES DONNÉES (M de MVC)
# Ces classes représentent les tables de la base de données
# Elles contiennent:
# - Les champs de la base de données (CharField, DecimalField, etc.)
# - Les méthodes utilitaires (save, __str__)
# - Les validations au niveau du modèle
#
# FLUX MVC:
# HTTP Request → VIEW → SERVICE → REPOSITORY → MODEL ← → DATABASE
#                                             ↑
#                                      (Vous êtes ici)
#
# Les Models sont utilisés par:
# - Repository (pour accéder aux données)
# - Service (pour les manipuler)
# - Serializer (pour les transformer en JSON)
# - Admin (pour l'administration)
#
# AVANTAGES:
# ✅ Schéma de données centralisé
# ✅ Migrations automatiques
# ✅ Validations au niveau BDD
# ✅ Relations entre tables faciles

from django.db import models
from django.utils.text import slugify


# M - MODEL: Classe qui représente la TABLE 'category' dans la BDD
class Category(models.Model):
    """
    Catégorie de produits.
    Représente la table 'shop_category' en base de données.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# M - MODEL: Classe qui représente la TABLE 'product' dans la BDD
class Product(models.Model):
    """
    Produit de la boutique.
    Représente la table 'shop_product' en base de données.
    Chaque champ = une colonne
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # ForeignKey = relation "un à plusieurs" (une catégorie, plusieurs produits)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    # Link product to a Shop (optional)
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Allow uploading images for products
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    # Optional variants/options stored as JSON, example: [{"sku":"S-RED","options":{"size":"S","color":"red"},"price":9.99,"stock":5}]
    variants = models.JSONField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    # M - Logique métier au niveau du MODEL (avant de sauvegarder)
    def save(self, *args, **kwargs):
        # Générer un slug si pas présent
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            # Handle slug conflicts by appending counter
            counter = 1
            while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# M - MODEL: Classe qui représente la TABLE 'announcement' en base de données
class Announcement(models.Model):
    """Shop announcement or banner that can include an image.
    Représente la table 'shop_announcement' en BDD.
    """
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, null=True, blank=True, related_name='announcements')
    title = models.CharField(max_length=200)
    message = models.TextField()
    image = models.ImageField(upload_to='announcements/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Announcement: {self.title}"
