from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.conf import settings

from orders.models import Order, OrderItem
from shop.models import Product

User = get_user_model()


class FrontendIndexView(View):
    """
    Serve the frontend React app (index.html).
    In development, redirect to Vite dev server (port 3003).
    In production, serve built index.html.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        if settings.DEBUG:
            # In development, redirect to configured frontend URL
            return redirect(settings.FRONTEND_URL)
        else:
            # In production, serve built index.html
            # You would configure Django to serve static files from frontend/build
            return render(request, 'frontend/index.html')


class CreateOrderView(View):
    template_name = "orders/create.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'users': User.objects.filter(role='CUSTOMER'),
            'products': Product.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            user_id = request.POST.get('user_id')
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            total = Decimal(request.POST.get('total', '0'))
            price = Decimal(request.POST.get('price', '0'))
            status = request.POST.get('status', 'processing')

            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)

            order = Order.objects.create(user=user, total=total, status=status)
            OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            messages.success(request, f"Commande #{order.id} créée avec succès!")
            return redirect('dashboard')
        except (User.DoesNotExist, Product.DoesNotExist, ValueError) as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('create-order')


class CreateProductView(View):
    template_name = "products/create.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            name = request.POST.get('name', '').strip()
            price = Decimal(request.POST.get('price', '0'))
            stock = int(request.POST.get('stock', 0))
            description = request.POST.get('description', '').strip()
            image = request.POST.get('image', '').strip()

            if not name:
                raise ValueError("Le nom du produit est requis.")

            product = Product.objects.create(
                name=name, price=price, stock=stock, description=description, image=image
            )

            messages.success(request, f"Produit '{product.name}' créé avec succès!")
            return redirect('dashboard')
        except (ValueError, Exception) as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('create-product')


class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        self._ensure_demo_data()
        context = self._build_context()
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        action = request.POST.get("action")
        if action == "create_order":
            self._create_order()
            messages.success(request, "Commande de démonstration ajoutée avec succès.")
        elif action == "create_product":
            self._create_product()
            messages.success(request, "Produit de démonstration ajouté avec succès.")
        elif action == "refresh":
            messages.info(request, "Statistiques actualisées.")
        else:
            messages.warning(request, "Action inconnue. Rien n'a été modifié.")
        return redirect("dashboard")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _ensure_demo_data(self) -> None:
        """Idempotent demo data seeding for local testing without breaking prod data."""
        if Order.objects.count() >= 3:
            return

        # Demo users
        demo_users = []
        for idx in range(1, 3 + 1):
            username = f"demo_customer_{idx}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": f"Client {idx}",
                },
            )
            if created:
                user.set_password("changeme123")
                user.save(update_fields=["password"])
            demo_users.append(user)

        # Demo products
        product_specs = [
            ("T-shirt coton", Decimal("3500.00"), "demo-tshirt"),
            ("Sneakers", Decimal("12500.00"), "demo-sneakers"),
            ("Veste légère", Decimal("8200.00"), "demo-veste"),
        ]
        products = []
        for name, price, slug in product_specs:
            product, _ = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "price": price,
                    "stock": 25,
                },
            )
            products.append(product)

        # Ensure at least 3 orders exist, spread over the last few days
        now = timezone.now()
        sample_totals = [Decimal("14500.00"), Decimal("18900.00"), Decimal("9200.00")]
        existing = Order.objects.count()
        needed = max(0, 3 - existing)
        for idx in range(needed):
            total = sample_totals[idx % len(sample_totals)]
            order = Order.objects.create(
                user=demo_users[idx % len(demo_users)],
                total=total,
                status="completed",
            )
            order.created_at = now - timedelta(days=idx * 2)
            order.save(update_fields=["created_at"])

        # Attach one item per order when missing so product counts remain meaningful
        # (lightweight; we avoid touching existing data)
        for order in Order.objects.filter(items__isnull=True):
            Product.objects.first()  # ensure at least one product exists
            # Skip if no product present (unlikely after seed)
            product = Product.objects.first()
            if not product:
                break
            order.items.create(product=product, price=product.price, quantity=1)

    def _create_product(self) -> None:
        """Create a lightweight demo product without disturbing existing ones."""
        suffix = int(timezone.now().timestamp())
        Product.objects.get_or_create(
            slug=f"quick-product-{suffix}",
            defaults={
                "name": f"Nouveau produit {suffix}",
                "price": Decimal("5000.00"),
                "stock": 10,
            },
        )

    def _create_order(self) -> None:
        """Create a simple paid order for demo purposes."""
        user = User.objects.order_by("id").first()
        if not user:
            return
        amount = Decimal("7500.00")
        order = Order.objects.create(user=user, total=amount, status="completed")
        product = Product.objects.first()
        if product:
            order.items.create(product=product, price=product.price, quantity=1)

    def _build_context(self) -> dict:
        now = timezone.now()
        start_date = now.date() - timedelta(days=6)

        orders_last_week = (
            Order.objects.filter(created_at__date__gte=start_date)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(total=Sum("total"))
        )
        by_day = {entry["day"].isoformat(): float(entry["total"] or 0) for entry in orders_last_week}
        labels = []
        values = []
        for offset in range(7):
            day = start_date + timedelta(days=offset)
            labels.append(day.strftime("%d %b"))
            values.append(round(by_day.get(day.isoformat(), 0), 2))

        orders_qs = Order.objects.select_related("user").order_by("-created_at")[:5]

        context = {
            "stats": {
                "orders": Order.objects.count(),
                "clients": User.objects.filter(orders__isnull=False).distinct().count(),
                "products": Product.objects.count(),
                "revenue": Order.objects.aggregate(total=Sum("total"))['total'] or Decimal("0"),
            },
            "recent_orders": [
                {
                    "id": order.id,
                    "customer": order.user.get_full_name() or order.user.username,
                    "status": order.status,
                    "total": float(order.total),
                    "created": order.created_at,
                }
                for order in orders_qs
            ],
            "chart": {"labels": labels, "values": values},
        }
        return context


class ClientsListPageView(View):
    """Server-rendered clients list page with simple search and pagination-like slicing."""
    template_name = "clients/list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        # Require authentication
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('login')
        
        q = (request.GET.get("q") or "").strip()
        
        # Get all customers or filter by shop ownership if needed
        users_qs = User.objects.filter(role="CUSTOMER").order_by("-date_joined")
        
        if q:
            # Basic search across username, first_name, last_name, email
            from django.db.models import Q
            users_qs = users_qs.filter(
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q)
            )

        # Build client data with avatar and order count
        clients = []
        for u in users_qs.select_related():
            # Get orders count
            orders_count = 0
            try:
                if hasattr(u, "buyer_orders"):
                    orders_count = u.buyer_orders.count()
            except:
                pass
            
            # Get avatar URL
            avatar_url = None
            if u.avatar:
                try:
                    avatar_url = u.avatar.url
                except:
                    pass
            
            clients.append({
                "id": u.id,
                "name": (u.get_full_name() or u.username),
                "email": u.email,
                "username": u.username,
                "plan": u.plan,
                "joined": u.date_joined,
                "orders_count": orders_count,
                "avatar_url": avatar_url,
                "phone": getattr(u, "phone_number", None),
            })

        total_clients = users_qs.count()
        active_clients = users_qs.filter(is_active=True).count()
        activity_rate = round((active_clients / total_clients * 100)) if total_clients > 0 else 0
        
        context = {
            "clients": clients,
            "query": q,
            "stats": {
                "total": total_clients,
                "active": active_clients,
                "activity_rate": activity_rate,
            },
        }
        return render(request, self.template_name, context)


class ProfileDynamicView(LoginRequiredMixin, View):
    """Dynamic profile page with 3D animations and interactive features."""
    template_name = "profile_dynamic.html"
    login_url = '/accounts/login/'
    
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, {'user': request.user})
