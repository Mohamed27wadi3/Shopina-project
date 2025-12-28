"""
Cart admin configuration.
"""
from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price_at_add', 'subtotal')
    list_filter = ('created_at',)
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ('created_at', 'updated_at')
