# PATTERN MVC: SERIALIZER (Transformateur Modèle ↔ Vue)
# ======================================================
#
# Le Serializer transforme:
# - MODEL (Python) → JSON (pour envoyer au frontend)
# - JSON (du frontend) → MODEL (pour sauvegarder en BDD)
#
# FLUX COMPLET:
# Frontend (JSON) ← SERIALIZER ← MODEL ← REPOSITORY ← DATABASE
# Frontend (JSON) → SERIALIZER → MODEL → REPOSITORY → DATABASE
#
# Le Serializer:
# - Valide les données du frontend
# - Convertit les types (date, decimal, relations)
# - Inclut/exclut certains champs
# - Transforme les images en URLs
# - Crée des champs calculés (get_image, etc.)
#
# AVANTAGES:
# ✅ Sécurité (on expose que ce qu'on veut)
# ✅ Validation (avant de sauvegarder)
# ✅ Flexibilité (différent serializer selon le contexte)
# ✅ Transformation (JSON ↔ Model)

from rest_framework import serializers
from .models import Category, Product
from .models import Announcement
from .models import StoreCustomization


# V - VIEW SERIALIZER: Transforme Category Model en JSON
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer pour la Category.
    Transforme le Model Category en JSON pour le frontend.
    """
    class Meta:
        model = Category
        fields = ('id', 'name')


# V - VIEW SERIALIZER: Transforme Product Model en JSON
class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer pour Product.
    Transforme Model Product en JSON + validation.
    """
    # Champ relié: inclure les données complètes de la catégorie
    category = CategorySerializer()
    # Champ personnalisé: transformer l'image en URL complète
    image = serializers.SerializerMethodField()
    # Champ JSON: validation spéciale pour variants
    variants = serializers.JSONField(required=False)

    class Meta:
        model = Product
        # Champs à inclure dans la réponse JSON
        fields = ('id', 'name', 'slug', 'category', 'description', 'price', 'image', 'stock', 'rating', 'reviews', 'variants')

    # V - Méthode pour transformer l'image du serveur en URL complète pour le frontend
    def get_image(self, obj):
        """Transforme le chemin de l'image en URL complète."""
        request = self.context.get('request')
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                url = obj.image
            if request and url and not url.startswith('http'):
                return request.build_absolute_uri(url)
            return url
        return None

    # V - Validation: s'assure que les variants ont le bon format
    def validate_variants(self, value):
        """Valide la structure des variants."""
        # Basic validation for variants structure
        if value is None:
            return value
        if not isinstance(value, list):
            raise serializers.ValidationError('variants must be a list of variant objects')
        for v in value:
            if not isinstance(v, dict):
                raise serializers.ValidationError('each variant must be an object')
            # require sku and price/stock optionally
            if 'sku' not in v:
                raise serializers.ValidationError('each variant must include a sku')
        return value


# V - VIEW SERIALIZER: Transforme Announcement Model en JSON
class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Serializer pour Announcement.
    Transforme Model Announcement en JSON.
    """
    # Champ personnalisé: transformer l'image en URL
    image = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ('id', 'shop', 'title', 'message', 'image', 'created_at')

    # V - Méthode pour transformer l'image
    def get_image(self, obj):
        """Transforme le chemin de l'image en URL complète."""
        request = self.context.get('request')
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                url = obj.image
            if request and url and not str(url).startswith('http'):
                return request.build_absolute_uri(url)
            return url
        return None

# V - VIEW SERIALIZER: Store Customization
# ==========================================
class StoreCustomizationSerializer(serializers.ModelSerializer):
    """
    Serializer pour StoreCustomization.
    Transforme les paramètres de personnalisation en JSON.
    """
    # Champ personnalisé: transformer le logo en URL
    logo = serializers.SerializerMethodField()
    
    # Champs calculés
    colors = serializers.SerializerMethodField()
    theme = serializers.SerializerMethodField()
    
    class Meta:
        model = StoreCustomization
        fields = (
            'id',
            'shop',
            # Colors
            'primary_color',
            'secondary_color',
            'accent_color',
            'background_color',
            'text_color',
            # Typography
            'primary_font',
            # Branding
            'logo',
            'shop_name_custom',
            # Layout
            'border_radius',
            'shadow_style',
            # Advanced
            'advanced_options',
            # Metadata
            'created_at',
            'updated_at',
            # Champs calculés
            'colors',
            'theme',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'colors', 'theme')
    
    def get_logo(self, obj):
        """Transforme le logo en URL complète."""
        request = self.context.get('request')
        if obj.logo:
            try:
                url = obj.logo.url
            except Exception:
                url = obj.logo
            if request and url and not str(url).startswith('http'):
                return request.build_absolute_uri(url)
            return url
        return None
    
    def get_colors(self, obj):
        """Retourne les couleurs en dictionnaire"""
        return obj.get_colors_dict()
    
    def get_theme(self, obj):
        """Retourne le thème complet"""
        return obj.get_theme_dict()
    
    def validate_primary_color(self, value):
        """Valide que la couleur est au format hex"""
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Color must be in hex format: #RRGGBB')
        return value
    
    def validate_secondary_color(self, value):
        """Valide que la couleur est au format hex"""
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Color must be in hex format: #RRGGBB')
        return value
    
    def validate_accent_color(self, value):
        """Valide que la couleur est au format hex"""
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Color must be in hex format: #RRGGBB')
        return value