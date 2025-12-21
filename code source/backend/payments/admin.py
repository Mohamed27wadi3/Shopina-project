from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'stripe_payment_intent', 'order', 'amount', 'status', 'created_at')
    search_fields = ('stripe_payment_intent', 'order__id')
