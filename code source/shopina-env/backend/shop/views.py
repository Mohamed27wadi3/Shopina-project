# PATTERN MVC: VIEW (V - Gère les requêtes HTTP)
# ================================================
#
# Les Views gèrent les requêtes HTTP du pattern MVC.
# Responsabilités:
# - Recevoir la requête HTTP
# - Extraire les données (URL params, body JSON)
# - Appeler le Service pour la logique métier
# - Retourner une réponse HTTP (JSON)
#
# FLUX MVC COMPLET:
# HTTP Request
#     ↓
# VIEW (c'est ICI) ← reçoit la requête
#     ↓
# SERVICE → REPOSITORY → MODEL → DATABASE
#     ↑
#     ↓
# HTTP Response (JSON)
#
# LES VIEWS NE FONT PAS:
# ❌ Logique métier (c'est Service)
# ❌ Accès direct à la BDD (c'est Repository)
# ❌ Transformation Model→JSON (c'est Serializer)
#
# AVANTAGES:
# ✅ Séparation claire des responsabilités
# ✅ Code HTTP indépendant de la logique métier
# ✅ Facile de changer le framework HTTP (Django → FastAPI)

from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .models import Announcement
from .serializers import AnnouncementSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import parser_classes

# V - Importe le SERVICE (logique métier), pas le Model directement
from .services.product_service import ProductService
from core.utils.exceptions import ValidationError as CustomValidationError, ResourceNotFoundError


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour récupérer les catégories.
    Gère les requêtes HTTP: GET /categories/, GET /categories/{id}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour récupérer les produits.
    Gère les requêtes HTTP: GET /products/, GET /products/{id}/
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category__name']

    @action(detail=False, methods=['get'])
    def top(self, request):
        """Endpoint custom: récupère les 10 meilleurs produits."""
        products = self.get_queryset().order_by('-rating')[:10]
        return Response(self.get_serializer(products, many=True).data)


# V - VIEW: Fonction pour créer un produit
# C - CONTROLLER: Cette fonction appelle le SERVICE pour la logique métier
# S - Responsabilité Unique: gère UNIQUEMENT la requête HTTP
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_api(request):
    """
    Merchant endpoint to create a product for their shop (supports image upload).
    Gère la requête HTTP: POST /api/products/create/
    Utilise ProductService pour la logique métier.
    """
    # V - Récupérer les données de la requête HTTP
    
    # V - Récupérer les données de la requête HTTP
    try:
        shop = request.user.shop
    except AttributeError:
        return Response({'detail': "Vous devez créer une boutique avant d'ajouter des produits."}, status=400)
    except Exception as e:
        return Response({'detail': f"Erreur lors de l'accès à la boutique: {str(e)}"}, status=400)

    # Extraire les données du formulaire/JSON
    name = request.data.get('name')
    price = request.data.get('price')
    description = request.data.get('description', '')
    category_name = request.data.get('category')
    stock = request.data.get('stock', 1)
    image = request.FILES.get('image')

    # Validation basique HTTP (champs requis)
    if not name or not price:
        return Response({'detail': 'name and price are required.'}, status=400)

    # C - Appeler le SERVICE pour la logique métier
    try:
        # Injection de dépendance: créer le service
        product_service = ProductService()
        # Appeler la méthode métier du service
        product = product_service.create_product_for_shop(
            shop=shop,
            name=name,
            price=price,
            description=description,
            category_name=category_name,
            stock=stock,
            image=image
        )
        
        # V - Transformer le Model en JSON avec le Serializer
        serializer = ProductSerializer(product, context={'request': request})
        # V - Retourner la réponse HTTP
        return Response(serializer.data, status=201)
        
    except CustomValidationError as e:
        return Response({'detail': str(e)}, status=400)
    except Exception as e:
        return Response({'detail': f'Erreur lors de la création du produit: {str(e)}'}, status=500)


@api_view(['GET'])
def public_shop_products(request, slug):
    """Return public products for a shop identified by slug (only active shop)."""
    from shops.models import Shop as ShopModel
    
    try:
        shop = ShopModel.objects.get(slug=slug)
    except ShopModel.DoesNotExist:
        return Response({'detail': f'Shop with slug "{slug}" not found.'}, status=404)
    
    if not shop.is_active:
        return Response({
            'detail': 'This shop is not publicly available yet.',
            'is_active': False
        }, status=403)

    products = Product.objects.filter(shop=shop)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_shop_products(request):
    """
    Endpoint pour le marchand: retourne les produits de sa propre boutique
    (même si elle n'est pas active publiquement).
    """
    try:
        user_shop = request.user.shop
    except AttributeError:
        return Response({'detail': 'Vous n\'avez pas de boutique.'}, status=404)

    products = Product.objects.filter(shop=user_shop)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_product_api(request, product_id):
    """
    Update a product owned by the authenticated user's shop.
    Uses ProductService for business logic (MVC architecture).
    """
    # Check user ownership
    try:
        user_shop = request.user.shop
    except Exception:
        return Response({'detail': 'You do not own a shop.'}, status=403)

    # Check product exists and belongs to user's shop
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=404)

    if product.shop_id != user_shop.id:
        return Response({'detail': 'Permission denied.'}, status=403)

    # Build update data
    update_data = {}
    data = request.data
    
    if 'name' in data:
        update_data['name'] = data.get('name')
    if 'description' in data:
        update_data['description'] = data.get('description')
    if 'price' in data:
        update_data['price'] = data.get('price')
    if 'stock' in data:
        update_data['stock'] = data.get('stock')
    if 'variants' in data:
        update_data['variants'] = data.get('variants')
    if 'category' in data:
        cat_name = data.get('category')
        if cat_name:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            update_data['category'] = cat
    if request.FILES.get('image'):
        update_data['image'] = request.FILES.get('image')

    # Use service layer
    try:
        product_service = ProductService()
        updated_product = product_service.update_product(product_id, **update_data)
        serializer = ProductSerializer(updated_product, context={'request': request})
        return Response(serializer.data)
        
    except CustomValidationError as e:
        return Response({'detail': str(e)}, status=400)
    except ResourceNotFoundError as e:
        return Response({'detail': str(e)}, status=404)
    except Exception as e:
        return Response({'detail': f'Erreur lors de la mise à jour: {str(e)}'}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_api(request, product_id):
    """
    Delete a product if it belongs to the authenticated user's shop.
    Uses ProductService for business logic (MVC architecture).
    """
    # Check user ownership
    try:
        user_shop = request.user.shop
    except Exception:
        return Response({'detail': 'You do not own a shop.'}, status=403)

    # Check product exists and belongs to user's shop
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=404)

    if product.shop_id != user_shop.id:
        return Response({'detail': 'Permission denied.'}, status=403)

    # Use service layer
    try:
        product_service = ProductService()
        product_service.delete_product(product_id)
        return Response({'message': 'Product deleted.'}, status=204)
        
    except ResourceNotFoundError as e:
        return Response({'detail': str(e)}, status=404)
    except Exception as e:
        return Response({'detail': f'Erreur lors de la suppression: {str(e)}'}, status=500)


@api_view(['GET', 'POST'])
def announcements_list(request):
    """Create announcement (POST, authenticated merchant) or list all announcements (GET).
    For creation, user must have `request.user.shop` set (merchant).
    """
    if request.method == 'GET':
        announcements = Announcement.objects.all().select_related('shop')[:50]
        serializer = AnnouncementSerializer(announcements, many=True, context={'request': request})
        return Response(serializer.data)

    # POST: create announcement for authenticated user's shop
    if request.method == 'POST':
        if not request.user or not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=401)
        try:
            shop = request.user.shop
        except Exception:
            return Response({'detail': 'You must have a shop to create an announcement.'}, status=400)

        title = request.data.get('title') or request.POST.get('title')
        message = request.data.get('message') or request.POST.get('message')
        image = request.FILES.get('image')
        if not title or not message:
            return Response({'detail': 'title and message are required.'}, status=400)

        ann = Announcement.objects.create(shop=shop, title=title, message=message, image=image)
        serializer = AnnouncementSerializer(ann, context={'request': request})
        return Response(serializer.data, status=201)


@api_view(['GET'])
def public_shop_announcements(request, slug):
    """Return announcements for a public shop (by slug)."""
    try:
        from shops.models import Shop as ShopModel
        shop = ShopModel.objects.get(slug=slug, is_active=True)
    except Exception:
        return Response({'detail': 'Shop not found.'}, status=404)

    announcements = Announcement.objects.filter(shop=shop)
    serializer = AnnouncementSerializer(announcements, many=True, context={'request': request})
    return Response(serializer.data)
