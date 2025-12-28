import os
import stripe
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            # Create a PaymentIntent
            # Ensure order.total_price is decimal or float
            amount = int(float(order.total_price) * 100)
            
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={'order_id': order.id}
            )
            
            return Response({
                'client_secret': intent.client_secret
            })
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent.get('metadata', {}).get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'paid' # Update based on your Order model fields
                order.save()
            except Order.DoesNotExist:
                pass

    return JsonResponse({'status': 'received'})


class SubscriptionCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    PLAN_PRICING = {
        'free': Decimal('0'),
        'starter': Decimal('19'),
        'pro': Decimal('49'),
        'enterprise': Decimal('99'),
    }

    def post(self, request, *args, **kwargs):
        plan = request.data.get('plan', 'free')
        billing_cycle = request.data.get('billing_cycle', 'monthly')
        last4 = (request.data.get('last4') or '')[:4]

        if plan not in self.PLAN_PRICING:
            return Response({'error': 'Invalid plan'}, status=status.HTTP_400_BAD_REQUEST)
        if billing_cycle not in ['monthly', 'yearly']:
            return Response({'error': 'Invalid billing cycle'}, status=status.HTTP_400_BAD_REQUEST)

        price = self.PLAN_PRICING[plan]
        if billing_cycle == 'yearly':
            price = price * Decimal('12') * Decimal('0.9')  # 10% off yearly

        status_value = 'pending' if plan == 'enterprise' else 'active'
        period_end = timezone.now() + timezone.timedelta(days=30 if billing_cycle == 'monthly' else 365)

        sub, _ = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                'plan': plan,
                'price': price,
                'billing_cycle': billing_cycle,
                'status': status_value,
                'current_period_end': period_end,
                'last4': last4 or None,
                'activated_at': timezone.now(),
            }
        )

        # Store plan on user for quick access
        request.user.plan = plan
        request.user.save(update_fields=['plan'])

        return Response({
            'status': sub.status,
            'plan': sub.plan,
            'billing_cycle': sub.billing_cycle,
            'price': str(sub.price),
            'current_period_end': sub.current_period_end,
        })
