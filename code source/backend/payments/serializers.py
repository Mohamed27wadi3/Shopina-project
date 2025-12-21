from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'stripe_payment_intent', 'amount', 'currency', 'status', 'created_at')
