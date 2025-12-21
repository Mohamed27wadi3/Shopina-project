from django.urls import path
from .views import create_payment_intent, stripe_webhook

app_name = 'payments'

urlpatterns = [
    path('create-intent/', create_payment_intent, name='create_intent'),
    path('webhook/', stripe_webhook, name='webhook'),
]
