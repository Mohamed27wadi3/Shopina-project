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
