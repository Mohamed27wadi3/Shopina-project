from rest_framework import serializers
from .models import Order, OrderItem
from shop.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'price', 'quantity')


class CreateOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ('product_id', 'price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total', 'created_at', 'items')


class CreateOrderSerializer(serializers.ModelSerializer):
    items = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('items',)

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=user)
        total = 0
        for item in items_data:
            product = ProductSerializer.Meta.model.objects.get(pk=item['product_id'])
            oi = OrderItem.objects.create(order=order, product=product, price=item['price'], quantity=item['quantity'])
            total += oi.price * oi.quantity
        order.total = total
        order.save()
        return order
