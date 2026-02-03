from rest_framework import serializers
from .models import Category, Product
from .models import Announcement


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = serializers.SerializerMethodField()
    variants = serializers.JSONField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'description', 'price', 'image', 'stock', 'rating', 'reviews', 'variants')

    def get_image(self, obj):
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

    def validate_variants(self, value):
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


class AnnouncementSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ('id', 'shop', 'title', 'message', 'image', 'created_at')

    def get_image(self, obj):
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
