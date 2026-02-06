from rest_framework import serializers
from .models import Order, OrderItem
from shop.serializers import ProductSerializer
from shop.models import Product
from notifications.models import Notification


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'price', 'quantity')


class CreateOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=10000)

    class Meta:
        model = OrderItem
        fields = ('product_id', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total', 'created_at', 'items')

    def get_user(self, obj):
        user = getattr(obj, 'user', None)
        if not user:
            return None
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': getattr(user, 'phone_number', None),
        }


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
        seller_users = set()
        for item in items_data:
            try:
                product = Product.objects.get(pk=item['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError({'items': f"Produit introuvable: {item['product_id']}"})
            oi = OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=item['quantity']
            )
            total += oi.price * oi.quantity

            shop = getattr(product, 'shop', None)
            owner = getattr(shop, 'owner', None) if shop else None
            if owner and owner.id != user.id:
                seller_users.add(owner)

        order.total = total
        order.save()

        if seller_users:
            notifications = []
            for seller in seller_users:
                notifications.append(Notification(
                    user=seller,
                    type='ORDER',
                    title='Nouvelle commande',
                    message=f'Commande #{order.id} reçue. Consultez vos commandes pour plus de détails.'
                ))
            Notification.objects.bulk_create(notifications)

        return order
