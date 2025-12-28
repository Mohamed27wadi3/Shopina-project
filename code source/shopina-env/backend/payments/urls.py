from django.urls import path
from .views import stripe_webhook, CreatePaymentIntentView, SubscriptionCheckoutView

app_name = 'payments'

urlpatterns = [
    path('webhook/', stripe_webhook, name='webhook'),
    path('create-intent/', CreatePaymentIntentView.as_view(), name='create-intent'),
    path('subscribe/', SubscriptionCheckoutView.as_view(), name='subscribe'),
]
