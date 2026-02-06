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


# M - MODEL: Store Customization (Theme & Branding)
# ===================================================
class StoreCustomization(models.Model):
    """
    Stocke les paramètres de personnalisation d'une boutique:
    - Couleurs (primaire, secondaire, accent)
    - Police d'écriture
    - Logo
    - Nom de la boutique
    - Arrondi des boutons, ombres, etc.
    
    Chaque boutique a SON PROPRE enregistrement (one-to-one)
    """
    shop = models.OneToOneField('shops.Shop', on_delete=models.CASCADE, related_name='customization')
    
    # ========== COLORS ==========
    # Couleurs principales
    primary_color = models.CharField(
        max_length=7, 
        default='#0077FF',
        help_text="Couleur primaire (hex format: #RRGGBB)"
    )
    secondary_color = models.CharField(
        max_length=7, 
        default='#5AC8FA',
        help_text="Couleur secondaire"
    )
    accent_color = models.CharField(
        max_length=7, 
        default='#FFD43B',
        help_text="Couleur d'accent"
    )
    background_color = models.CharField(
        max_length=7, 
        default='#FFFFFF',
        help_text="Couleur de fond"
    )
    text_color = models.CharField(
        max_length=7, 
        default='#0A1A2F',
        help_text="Couleur du texte"
    )
    
    # ========== TYPOGRAPHY ==========
    # Police d'écriture disponible
    FONT_CHOICES = [
        ('inter', 'Inter (Default)'),
        ('poppins', 'Poppins'),
        ('roboto', 'Roboto'),
        ('ubuntu', 'Ubuntu'),
        ('dm-sans', 'DM Sans'),
        ('geist', 'Geist'),
    ]
    primary_font = models.CharField(
        max_length=20,
        choices=FONT_CHOICES,
        default='inter',
        help_text="Police principale"
    )
    
    # ========== BRANDING ==========
    # Logo de la boutique
    logo = models.ImageField(
        upload_to='shop_logos/',
        null=True,
        blank=True,
        help_text="Logo de la boutique (recommandé: 300x300px)"
    )
    
    # Nom de la boutique (peut être différent du shop.name)
    shop_name_custom = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Nom personnalisé (si vide, utilise shop.name)"
    )
    
    # ========== LAYOUT SETTINGS ==========
    # Arrondi des éléments
    BORDER_RADIUS_CHOICES = [
        ('rounded-none', 'Sharp (0px)'),
        ('rounded-sm', 'Very Small (4px)'),
        ('rounded-md', 'Small (8px)'),
        ('rounded-lg', 'Medium (12px)'),
        ('rounded-xl', 'Large (16px)'),
        ('rounded-2xl', 'Very Large (24px)'),
    ]
    border_radius = models.CharField(
        max_length=20,
        choices=BORDER_RADIUS_CHOICES,
        default='rounded-xl',
        help_text="Arrondi des boutons et cartes"
    )
    
    # Ombres
    SHADOW_CHOICES = [
        ('shadow-sm', 'Small'),
        ('shadow-md', 'Medium'),
        ('shadow-lg', 'Large'),
        ('shadow-xl', 'Extra Large'),
    ]
    shadow_style = models.CharField(
        max_length=20,
        choices=SHADOW_CHOICES,
        default='shadow-lg',
        help_text="Style d'ombre"
    )
    
    # ========== ADVANCED OPTIONS ==========
    # Options supplémentaires en JSON
    # Exemple: {"headerHeight": 80, "footerBgColor": "#f5f5f5", "enableAnimations": true}
    advanced_options = models.JSONField(
        default=dict,
        blank=True,
        help_text="Options avancées en JSON"
    )
    
    # ========== METADATA ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Store Customization"
        verbose_name_plural = "Store Customizations"
    
    def __str__(self):
        return f"Customization for {self.shop.name}"
    
    def get_colors_dict(self):
        """Retourne toutes les couleurs en dictionnaire"""
        return {
            'primary': self.primary_color,
            'secondary': self.secondary_color,
            'accent': self.accent_color,
            'background': self.background_color,
            'text': self.text_color,
        }
    
    def get_theme_dict(self):
        """Retourne le thème complet en dictionnaire"""
        return {
            'colors': self.get_colors_dict(),
            'font': self.primary_font,
            'logo': self.logo.url if self.logo else None,
            'shopName': self.shop_name_custom or self.shop.name,
            'layout': {
                'borderRadius': self.border_radius,
                'shadow': self.shadow_style,
            },
            'advanced': self.advanced_options,
        }
