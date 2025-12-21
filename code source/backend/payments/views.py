import os
import stripe

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order
from .models import Payment


stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', getattr(settings, 'STRIPE_SECRET_KEY', ''))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    order_id = request.data.get('order_id')
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    intent = stripe.PaymentIntent.create(
        amount=int(order.total * 100),
        currency='usd',
        metadata={'order_id': order.id},
    )

    Payment.objects.create(order=order, stripe_payment_intent=intent['id'], amount=order.total, currency='usd', status='created')

    return Response({'client_secret': intent['client_secret']})


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', getattr(settings, 'STRIPE_WEBHOOK_SECRET', ''))

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception as e:
        return Response({'detail': 'Invalid signature'}, status=400)

    # Handle the checkout.session.completed or payment_intent.succeeded
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        pid = intent['id']
        # Update Payment and Order status
        try:
            payment = Payment.objects.get(stripe_payment_intent=pid)
            payment.status = 'succeeded'
            payment.save()
            order = payment.order
            order.status = 'completed'
            order.save()
        except Payment.DoesNotExist:
            pass

    return Response({'status': 'received'})
