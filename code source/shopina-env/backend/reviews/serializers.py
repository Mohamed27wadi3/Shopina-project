"""Review serializers."""
from rest_framework import serializers
from reviews.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'comment', 'is_verified', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'is_verified', 'created_at', 'updated_at')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reviews."""
    
    class Meta:
        model = Review
        fields = ('product', 'rating', 'comment')
