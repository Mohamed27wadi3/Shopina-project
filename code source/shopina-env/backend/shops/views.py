from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import ShopTheme
from shop.serializers import ProductSerializer

from .models import Shop
from .forms import ShopCreationForm, ShopUpdateForm


class MyShopRedirectView(LoginRequiredMixin, View):
    """
    Smart redirect view:
    - If user has a shop -> redirect to shop dashboard
    - If user doesn't have a shop -> redirect to create shop
    """
    login_url = reverse_lazy('login')
    
    def get(self, request):
        try:
            shop = request.user.shop
            # User has a shop, redirect to dashboard
            return redirect('shop:dashboard', slug=shop.slug)
        except (Shop.DoesNotExist, AttributeError):
            # User doesn't have a shop, redirect to create
            return redirect('shop:create')


class CreateShopView(LoginRequiredMixin, CreateView):
    """
    Create a new shop for the authenticated user.
    Only one shop per user is allowed.
    """
    model = Shop
    form_class = ShopCreationForm
    template_name = 'shops/create_shop.html'
    login_url = reverse_lazy('login')
    
    def get_success_url(self):
        # Return dashboard URL with the shop slug
        return reverse_lazy('shop:dashboard', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Créer ma boutique'
        return context
    
    def get(self, request, *args, **kwargs):
        # Check if user already has a shop
        if hasattr(request.user, 'shop'):
            messages.warning(request, 'Vous avez déjà une boutique.')
            return redirect('shop:dashboard', slug=request.user.shop.slug)
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Assign the current user as the owner and save the shop.
        """
        shop = form.save(commit=False)
        shop.owner = self.request.user
        shop.save()
        
        messages.success(self.request, f'✅ Boutique "{shop.name}" créée avec succès!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la création de la boutique.')
        return super().form_invalid(form)


class ShopDashboardView(LoginRequiredMixin, View):
    """
    Display the authenticated user's shop dashboard.
    """
    login_url = reverse_lazy('login')
    template_name = 'shops/shop_dashboard.html'
    
    def get(self, request, slug=None):
        try:
            # Get the user's shop
            if not hasattr(request.user, 'shop'):
                messages.info(request, '🏪 Vous devez d\'abord créer une boutique.')
                return redirect('shop:create')
                
            shop = request.user.shop
            
            # Verify the slug matches (security check)
            if slug and shop.slug != slug:
                messages.error(request, 'Accès refusé.')
                return redirect('shop:dashboard', slug=shop.slug)
            
            context = {
                'shop': shop,
                'page_title': f'Tableau de bord - {shop.name}',
            }
            return render(request, self.template_name, context)
        except (Shop.DoesNotExist, AttributeError) as e:
            messages.info(request, '🏪 Vous devez d\'abord créer une boutique.')
            return redirect('shop:create')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('dashboard')


class UpdateShopView(LoginRequiredMixin, View):
    """
    Update the authenticated user's shop details.
    """
    login_url = reverse_lazy('login')
    template_name = 'shops/update_shop.html'
    
    def get(self, request):
        try:
            shop = request.user.shop
            form = ShopUpdateForm(instance=shop)
            context = {
                'shop': shop,
                'form': form,
                'page_title': f'Paramètres - {shop.name}',
            }
            return render(request, self.template_name, context)
        except Shop.DoesNotExist:
            messages.info(request, 'Vous devez d\'abord créer une boutique.')
            return redirect('shop:create')
    
    def post(self, request):
        try:
            shop = request.user.shop
            form = ShopUpdateForm(request.POST, request.FILES, instance=shop)
            if form.is_valid():
                form.save()
                messages.success(request, f'✅ Boutique "{shop.name}" mise à jour avec succès!')
                return redirect('shop:dashboard', slug=shop.slug)
            else:
                context = {
                    'shop': shop,
                    'form': form,
                    'page_title': f'Paramètres - {shop.name}',
                }
                return render(request, self.template_name, context)
        except Shop.DoesNotExist:
            messages.info(request, 'Vous devez d\'abord créer une boutique.')
            return redirect('shop:create')


# ============================================================================
# API Views
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_shop(request):
    """
    API endpoint to get the current user's shop.
    Returns 404 if user doesn't have a shop.
    """
    try:
        shop = request.user.shop
        return Response({
            'id': shop.id,
            'name': shop.name,
            'slug': shop.slug,
            'description': shop.description,
            'email': shop.email,
            'phone': shop.phone,
            'is_active': shop.is_active,
            'is_verified': shop.is_verified,
            'total_products': shop.total_products,
            'total_orders': shop.total_orders,
            'total_sales': float(shop.total_sales),
            'average_rating': shop.average_rating,
            'created_at': shop.created_at.isoformat(),
            'owner': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            },
        })
    except Shop.DoesNotExist:
        return Response(
            {'detail': 'You do not have a shop yet.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_shop_api(request):
    """
    API endpoint to create a shop.
    """
    if hasattr(request.user, 'shop'):
        return Response(
            {'detail': 'You already have a shop.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    form = ShopCreationForm(request.data)
    if form.is_valid():
        shop = form.save(commit=False)
        shop.owner = request.user
        shop.save()
        return Response({
            'id': shop.id,
            'name': shop.name,
            'slug': shop.slug,
            'message': 'Shop created successfully!'
        }, status=status.HTTP_201_CREATED)
    
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def public_shop(request, slug):
    """
    Public, read-only shop view by slug.
    - Returns only active shops
    - No owner-identifying data leaked
    """
    try:
        shop = Shop.objects.get(slug=slug, is_active=True)
    except Shop.DoesNotExist:
        return Response({'detail': 'Shop not found or inactive.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'id': shop.id,
        'name': shop.name,
        'slug': shop.slug,
        'description': shop.description,
        'email': shop.email,
        'phone': shop.phone,
        'logo': shop.logo.url if shop.logo else None,
        'banner': shop.banner.url if shop.banner else None,
        'is_active': shop.is_active,
        'total_products': shop.total_products,
        'total_orders': shop.total_orders,
        'total_sales': float(shop.total_sales),
        'average_rating': shop.average_rating,
        'created_at': shop.created_at.isoformat(),
    })


@api_view(['GET'])
def public_shop_products(request, slug):
    """Return public product list for a shop identified by slug."""
    try:
        shop = Shop.objects.get(slug=slug, is_active=True)
    except Shop.DoesNotExist:
        return Response({'detail': 'Shop not found or inactive.'}, status=status.HTTP_404_NOT_FOUND)

    products = shop.products.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_theme(request):
    """Save active template and customization options for the authenticated user's shop."""
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        return Response({'detail': 'You do not have a shop yet.'}, status=status.HTTP_404_NOT_FOUND)

    template_id = request.data.get('template_id')
    options = request.data.get('options') or {}
    if not template_id:
        return Response({'detail': 'template_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    theme, _ = ShopTheme.objects.update_or_create(
        shop=shop,
        defaults={
            'template_id': int(template_id),
            'options': options,
            'is_active': True,
        }
    )
    return Response({'message': 'Theme saved', 'template_id': theme.template_id, 'options': theme.options})
