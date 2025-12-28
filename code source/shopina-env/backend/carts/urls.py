"""
Cart URL configuration.
"""
from django.urls import path
from .views import CartView, CartItemView, CartValidateView

app_name = 'carts'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items/', CartItemView.as_view(), name='cart_items_add'),
    path('items/<int:pk>/', CartItemView.as_view(), name='cart_items_update_delete'),
    path('validate/', CartValidateView.as_view(), name='cart_validate'),
]
