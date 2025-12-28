"""
Cart serializers for data validation and transformation.
"""
from rest_framework import serializers
from carts.models import Cart, CartItem
from shop.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items with product details."""
    
    product = ProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'price_at_add', 'subtotal', 'created_at')
        read_only_fields = ('id', 'price_at_add', 'created_at')


class CartSerializer(serializers.ModelSerializer):
    """Serializer for cart with items and totals."""
    
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart."""
    
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1, min_value=1, max_value=10000)


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating cart item quantity."""
    
    quantity = serializers.IntegerField(required=True, min_value=1, max_value=10000)
