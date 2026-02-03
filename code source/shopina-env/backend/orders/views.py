import csv
import datetime
import io
import re
from datetime import timedelta
import traceback
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.contrib.auth import get_user_model
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer

User = get_user_model()


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Order.objects.select_related('user')
            .prefetch_related('items__product')
            .order_by('-created_at')
        )
        role = getattr(user, 'role', None)
        if role in ('SELLER', 'ADMIN'):
            return qs
        return qs.filter(user=user)

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


@method_decorator(csrf_exempt, name='dispatch')
class OrdersImportPageView(View):
    """Simple import page placeholder for uploading CSV or bulk orders."""
    template_name = "orders/import.html"
    PRODUCT_FIELDS = ('product_name', 'product', 'Produit', 'Article', 'item', 'sku')
    QUANTITY_FIELDS = ('quantity', 'qty', 'Quantité', 'Qte', 'qte', 'Quantity')
    PRICE_FIELDS = ('price', 'unit_price', 'Prix', 'price_ht', 'price_ttc', 'unitPrice')
    TOTAL_FIELDS = ('total', 'montant', 'total_ttc', 'Total', 'amount', 'grand_total')
    STATUS_FIELDS = ('status', 'order_status', 'Statut', 'Etat')
    CUSTOMER_EMAIL_FIELDS = ('customer_email', 'email', 'Email', 'client_email', 'Customer Email')
    CUSTOMER_NAME_FIELDS = ('customer_name', 'name', 'client', 'Client', 'Customer Name')
    CUSTOMER_FIRST_NAME_FIELDS = ('first_name', 'prenom', 'Prénom')
    CUSTOMER_LAST_NAME_FIELDS = ('last_name', 'nom', 'Nom')
    CUSTOMER_PHONE_FIELDS = ('phone', 'phone_number', 'Telephone', 'téléphone')
    CUSTOMER_CITY_FIELDS = ('city', 'ville', 'City')
    ORDER_DATE_FIELDS = ('order_date', 'date', 'created_at', 'Date de commande')
    STATUS_ALIASES = {
        'pending': {'pending', 'en attente', 'nouveau', 'nouvelle', 'waiting', 'draft'},
        'processing': {'processing', 'en cours', 'traitement', 'processing_order'},
        'completed': {'completed', 'terminée', 'livrée', 'paid', 'delivered', 'shipped'},
        'cancelled': {'cancelled', 'annulée', 'refusée', 'failed', 'canceled'},
    }

    def dispatch(self, request, *args, **kwargs):
        self._attach_jwt_user(request)
        return super().dispatch(request, *args, **kwargs)

    def _attach_jwt_user(self, request):
        if getattr(request, 'user', None) and request.user.is_authenticated:
            return
        authenticator = JWTAuthentication()
        try:
            auth_result = authenticator.authenticate(request)
        except AuthenticationFailed:
            return
        if not auth_result:
            return
        user, token = auth_result
        request.user = user
        request.auth = token
        request._cached_user = user

    def _pick(self, row, keys):
        for key in keys:
            value = row.get(key)
            if value is None:
                continue
            text = str(value).strip()
            if text:
                return text
        return ''

    def _normalize_phone(self, phone):
        phone = (phone or '').strip()
        if not phone:
            return ''
        digits = re.sub(r'[^0-9+]', '', phone)
        return digits or phone

    def _parse_quantity(self, raw):
        try:
            quantity = int(float(str(raw).replace(',', '.')))
        except (ValueError, TypeError):
            quantity = 1
        return max(1, quantity)

    def _parse_decimal(self, raw, fallback='0'):
        text = str(raw).strip() if raw is not None else ''
        if not text:
            text = fallback
        normalized = text.replace('\u00A0', '').replace(' ', '')
        normalized = re.sub(r'[^0-9,.-]', '', normalized)
        if normalized.count(',') == 1 and normalized.count('.') == 0:
            normalized = normalized.replace(',', '.')
        elif normalized.count(',') > 1 and normalized.count('.') == 0:
            normalized = normalized.replace(',', '')
        try:
            return Decimal(normalized)
        except (InvalidOperation, ValueError):
            return Decimal(fallback)

    def _normalize_status(self, raw):
        value = (raw or '').strip().lower()
        for status, aliases in self.STATUS_ALIASES.items():
            if value in aliases:
                return status
        return 'pending'

    def _build_unique_username(self, seed):
        base = slugify(seed or 'client') or 'client'
        candidate = base
        suffix = 1
        while User.objects.filter(username=candidate).exists():
            suffix += 1
            candidate = f"{base}-{suffix}"
        return candidate

    def _generate_placeholder_email(self, label):
        base = slugify(label or 'client') or 'client'
        domain = 'import.shopina.local'
        candidate = base
        suffix = 1
        while User.objects.filter(email__iexact=f"{candidate}@{domain}").exists():
            suffix += 1
            candidate = f"{base}{suffix}"
        return f"{candidate}@{domain}"

    def _cache_user(self, cache, user, email, phone, full_name):
        keys = []
        if email:
            keys.append(email.lower())
        if phone:
            keys.append(self._normalize_phone(phone))
        if full_name:
            keys.append(full_name.lower())
        for key in filter(None, keys):
            cache[key] = user

    def _get_or_create_customer(self, row, cache):
        email_value = self._pick(row, self.CUSTOMER_EMAIL_FIELDS)
        email = email_value.lower() if email_value else ''
        first_name = self._pick(row, self.CUSTOMER_FIRST_NAME_FIELDS)
        last_name = self._pick(row, self.CUSTOMER_LAST_NAME_FIELDS)
        full_name = self._pick(row, self.CUSTOMER_NAME_FIELDS)
        if not (first_name or last_name) and full_name:
            parts = full_name.split()
            first_name = parts[0]
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        if not full_name and (first_name or last_name):
            full_name = f"{first_name or ''} {last_name or ''}".strip()
        phone = self._normalize_phone(self._pick(row, self.CUSTOMER_PHONE_FIELDS))
        city = self._pick(row, self.CUSTOMER_CITY_FIELDS)

        cache_key = email or phone or (full_name.lower() if full_name else '')
        if cache_key and cache_key in cache:
            return cache[cache_key], False

        user = None
        if email:
            user = User.objects.filter(email__iexact=email).first()
        if not user and phone:
            user = User.objects.filter(phone_number=phone).first()
        if not user and (first_name or last_name):
            name_filters = {}
            if first_name:
                name_filters['first_name__iexact'] = first_name
            if last_name:
                name_filters['last_name__iexact'] = last_name
            user = User.objects.filter(**name_filters).first()

        created = False
        if not user:
            email_for_user = email or self._generate_placeholder_email(full_name or first_name or 'client')
            username_seed = email_for_user.split('@')[0] if email_for_user else (full_name or 'client')
            username = self._build_unique_username(username_seed)
            password = User.objects.make_random_password(length=12)
            user = User.objects.create_user(
                username=username,
                email=email_for_user,
                password=password,
                first_name=first_name or '',
                last_name=last_name or '',
                role='CUSTOMER'
            )
            created = True

        updates = {}
        if first_name and not user.first_name:
            updates['first_name'] = first_name
        if last_name and not user.last_name:
            updates['last_name'] = last_name
        if phone and not user.phone_number:
            updates['phone_number'] = phone
        if city and not getattr(user, 'city', None):
            updates['city'] = city
        if user.role != 'CUSTOMER':
            updates['role'] = 'CUSTOMER'
        if updates:
            for field, value in updates.items():
                setattr(user, field, value)
            user.save(update_fields=list(updates.keys()))

        self._cache_user(cache, user, email_value, phone, full_name)
        return user, created

    def _maybe_apply_order_date(self, order, row):
        raw_date = self._pick(row, self.ORDER_DATE_FIELDS)
        if not raw_date:
            return False
        dt = parse_datetime(raw_date)
        if not dt:
            parsed_date = parse_date(raw_date)
            if parsed_date:
                dt = datetime.datetime.combine(parsed_date, datetime.time.min)
        if not dt:
            return False
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        order.created_at = dt
        order.save(update_fields=['created_at'])
        return True

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, self.template_name, {'error': 'Veuillez vous connecter pour importer un fichier.'})
        return render(request, self.template_name, {})

    def post(self, request):
        wants_json = request.path.startswith('/api/')

        if not request.user.is_authenticated:
            message = 'Authentification requise.'
            if wants_json:
                return JsonResponse({'detail': message}, status=401)
            return HttpResponse(message, status=401)

        upload = request.FILES.get('file')
        if not upload:
            if wants_json:
                return JsonResponse({'detail': 'Aucun fichier fourni.'}, status=400)
            return HttpResponse('Aucun fichier fourni', status=400)

        raw = upload.read()
        decoded = None
        for encoding in ('utf-8-sig', 'utf-8', 'latin-1'):
            try:
                decoded = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if decoded is None:
            if wants_json:
                return JsonResponse({'detail': "Impossible de lire le fichier (encodage inconnu)."}, status=400)
            return HttpResponse('Encodage de fichier non supporté', status=400)

        reader = csv.DictReader(io.StringIO(decoded))
        if not reader.fieldnames:
            if wants_json:
                return JsonResponse({'detail': 'CSV vide ou sans en-têtes.'}, status=400)
            return HttpResponse('CSV vide ou sans en-têtes', status=400)

        created = []
        customer_cache = {}
        customers_created = 0
        customers_matched = 0
        for row in reader:
            if not row or not any((value or '').strip() for value in row.values()):
                continue

            product_name = self._pick(row, self.PRODUCT_FIELDS)
            quantity = self._parse_quantity(self._pick(row, self.QUANTITY_FIELDS) or '1')
            unit_price = self._parse_decimal(self._pick(row, self.PRICE_FIELDS) or '0', fallback='0')
            try:
                unit_price = unit_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            except (InvalidOperation, AttributeError):
                unit_price = Decimal('0.00')
            total_raw = self._pick(row, self.TOTAL_FIELDS)
            total_amount = unit_price * quantity
            if total_raw:
                parsed_total = self._parse_decimal(total_raw, fallback=str(total_amount or '0'))
                if parsed_total > 0:
                    total_amount = parsed_total
                    if quantity:
                        unit_price = (parsed_total / quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            status_value = self._normalize_status(self._pick(row, self.STATUS_FIELDS))
            customer, customer_created = self._get_or_create_customer(row, customer_cache)
            if customer_created:
                customers_created += 1
            elif customer:
                customers_matched += 1

            assigned_user = customer or request.user

            product = None
            if product_name:
                product = Product.objects.filter(name__iexact=product_name.strip()).first()

            order = Order.objects.create(
                user=assigned_user,
                status=status_value,
                total=total_amount
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                price=unit_price,
                quantity=quantity,
            )
            self._maybe_apply_order_date(order, row)

            customer_label = assigned_user.get_full_name() or assigned_user.username or assigned_user.email
            created.append({
                'order_id': order.id,
                'customer': customer_label,
                'status': order.status,
                'product': product_name or (product.name if product else 'Inconnu'),
                'quantity': quantity,
                'total': float(total_amount),
            })

        if not created:
            if wants_json:
                return JsonResponse({'detail': 'Aucune ligne valide trouvée dans le fichier.'}, status=400)
            return HttpResponse('Aucune ligne valide dans le fichier', status=400)

        summary = {
            'orders_imported': len(created),
            'customers_created': customers_created,
            'customers_matched': customers_matched,
        }
        message_parts = [f"{summary['orders_imported']} commande(s) importée(s) avec succès." ]
        if summary['customers_created']:
            message_parts.append(f"{summary['customers_created']} nouveau(x) client(s) créé(s).")
        if summary['customers_matched']:
            message_parts.append(f"{summary['customers_matched']} client(s) existant(s) mis à jour.")
        message = ' '.join(message_parts)
        if wants_json:
            return JsonResponse({'message': message, 'orders': created, 'summary': summary}, status=201)
        return HttpResponse(message)


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
        try:
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
        except Exception as e:
            tb = traceback.format_exc()
            # Return JSON error details (useful during DEBUG) to avoid HTML error pages
            return Response({
                'error': str(e),
                'traceback': tb,
            }, status=500)
