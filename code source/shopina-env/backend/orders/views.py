from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views import View
from shop.models import Product
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # Return the full order representation
        out = OrderSerializer(order, context={'request': request})
        return Response(out.data, status=201)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrdersListPageView(ListView):
    """HTML view: list orders with pagination."""

    model = Order
    template_name = "orders/orders_list.html"
    context_object_name = "orders"
    paginate_by = 10
    ordering = "-created_at"

    def get_queryset(self):
        return (
            Order.objects.select_related("user")
            .prefetch_related("items")
            .order_by("-created_at")
        )
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailPageView(View):
    """HTML view: order detail page."""
    
    template_name = "orders/order_detail.html"
    
    def get(self, request, pk):
        # Get order with all related data
        order = get_object_or_404(
            Order.objects.select_related("user").prefetch_related("items__product"), 
            pk=pk
        )
        
        context = {
            'order': order,
            'items_count': order.items.count(),
        }
        return render(request, self.template_name, context)


class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def _pct_change(current: float, previous: float) -> float:
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 2)

    def _build_revenue_series(self, queryset, today):
        window_start = today - timedelta(days=6)
        aggregated = (
            queryset
            .filter(created_at__date__gte=window_start)
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(total=Coalesce(Sum('total'), Value(0, output_field=DecimalField(max_digits=10, decimal_places=2))))
        )
        mapping = {item['day']: item['total'] for item in aggregated}
        series = []
        for offset in range(6, -1, -1):
            day = today - timedelta(days=offset)
            series.append({
                'date': day.isoformat(),
                'value': float(mapping.get(day, Decimal('0'))),
            })
        total_value = float(sum(mapping.values())) if mapping else 0.0
        return series, total_value

    def _build_order_series(self, today):
        window_start = today - timedelta(days=6)
        aggregated = (
            Order.objects.filter(created_at__date__gte=window_start)
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(count=Count('id'))
        )
        mapping = {item['day']: item['count'] for item in aggregated}
        series = []
        for offset in range(6, -1, -1):
            day = today - timedelta(days=offset)
            series.append({
                'date': day.isoformat(),
                'value': mapping.get(day, 0),
            })
        total_count = sum(mapping.values()) if mapping else 0
        return series, total_count

    def get(self, request):
        today = timezone.localdate()
        period_start = today - timedelta(days=6)
        previous_start = period_start - timedelta(days=7)
        previous_end = period_start - timedelta(days=1)
        completed_statuses = ['processing', 'completed']

        # Scope all aggregations to the authenticated user's data to avoid cross-account leakage
        revenue_qs = Order.objects.filter(user=request.user, status__in=completed_statuses)
        total_revenue = revenue_qs.aggregate(
            total=Coalesce(Sum('total'), Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)))
        )['total']
        revenue_today = revenue_qs.filter(created_at__date=today).aggregate(
            total=Coalesce(Sum('total'), Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)))
        )['total']

        orders_today = Order.objects.filter(user=request.user, created_at__date=today).count()
        total_orders = Order.objects.filter(user=request.user).count()
        paid_orders = revenue_qs.count()

        current_revenue_total = revenue_qs.filter(created_at__date__gte=period_start).aggregate(
            total=Coalesce(Sum('total'), Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)))
        )['total']
        previous_revenue_total = revenue_qs.filter(created_at__date__gte=previous_start, created_at__date__lte=previous_end).aggregate(
            total=Coalesce(Sum('total'), Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)))
        )['total']

        current_orders = Order.objects.filter(user=request.user, created_at__date__gte=period_start).count()
        previous_orders = Order.objects.filter(user=request.user, created_at__date__gte=previous_start, created_at__date__lte=previous_end).count()

        avg_order_value = float(current_revenue_total) / current_orders if current_orders else 0.0

        revenue_series, revenue_window_sum = self._build_revenue_series(revenue_qs, today)
        orders_series, orders_window_sum = self._build_order_series(today)

        top_products = list(
            OrderItem.objects.filter(order__user=request.user, order__status__in=completed_statuses, product__isnull=False)
            .values('product__id', 'product__name')
            .annotate(
                quantity=Coalesce(Sum('quantity'), Value(0)),
                revenue=Coalesce(
                    Sum(
                        ExpressionWrapper(
                            F('price') * F('quantity'),
                            output_field=DecimalField(max_digits=10, decimal_places=2),
                        )
                    ),
                    Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)),
                ),
            )
            .order_by('-revenue')[:5]
        )

        recent_orders = [
            {
                'id': order.id,
                'customer': order.user.get_full_name() or order.user.username,
                'status': order.status,
                'total': float(order.total),
                'created_at': order.created_at.isoformat(),
            }
            for order in Order.objects.select_related('user').filter(user=request.user).order_by('-created_at')[:6]
        ]

        User = get_user_model()
        response_data = {
            'totals': {
                'revenue': float(total_revenue),
                'revenue_today': float(revenue_today),
                'orders': total_orders,
                'orders_today': orders_today,
                'paid_orders': paid_orders,
                'customers': User.objects.count(),
                'products': Product.objects.count(),
                'avg_order_value': round(avg_order_value, 2),
            },
            'changes': {
                'revenue_pct': self._pct_change(float(current_revenue_total), float(previous_revenue_total)),
                'orders_pct': self._pct_change(current_orders, previous_orders),
                'window_revenue': round(revenue_window_sum, 2),
                'window_orders': orders_window_sum,
            },
            'series': {
                'revenue': revenue_series,
                'orders': orders_series,
            },
            'top_products': [
                {
                    'id': item.get('product__id'),
                    'name': item.get('product__name'),
                    'quantity': item.get('quantity', 0),
                    'revenue': float(item.get('revenue', 0)),
                }
                for item in top_products
            ],
            'recent_orders': recent_orders,
        }

        return Response(response_data)
