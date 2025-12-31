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


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category__name']

    @action(detail=False, methods=['get'])
    def top(self, request):
        products = self.get_queryset().order_by('-rating')[:10]
        return Response(self.get_serializer(products, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_api(request):
    """
    Merchant endpoint to create a product for their shop (supports image upload).
    """
    try:
        shop = request.user.shop
    except Exception:
        return Response({'detail': "Vous devez créer une boutique avant d'ajouter des produits."}, status=400)

    name = request.data.get('name')
    price = request.data.get('price')
    description = request.data.get('description', '')
    category_name = request.data.get('category')
    image = request.FILES.get('image')

    if not name or not price:
        return Response({'detail': 'name and price are required.'}, status=400)

    # Find or create category
    category = None
    if category_name:
        category, _ = Category.objects.get_or_create(name=category_name)

    product = Product.objects.create(
        name=name,
        price=price,
        description=description,
        category=category,
        shop=shop,
        image=image,
    )

    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data, status=201)


@api_view(['GET'])
def public_shop_products(request, slug):
    """Return public products for a shop identified by slug (only active shop)."""
    try:
        from shops.models import Shop as ShopModel
        shop = ShopModel.objects.get(slug=slug, is_active=True)
    except Exception:
        return Response({'detail': 'Shop not found.'}, status=404)

    products = Product.objects.filter(shop=shop)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_product_api(request, product_id):
    """
    Update a product owned by the authenticated user's shop.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=404)

    # Ensure user owns the shop for this product
    try:
        user_shop = request.user.shop
    except Exception:
        return Response({'detail': 'You do not own a shop.'}, status=403)

    if product.shop_id != user_shop.id:
        return Response({'detail': 'Permission denied.'}, status=403)

    # Partial update: allow name, description, price, stock, category, variants, image
    data = request.data
    if 'name' in data:
        product.name = data.get('name')
    if 'description' in data:
        product.description = data.get('description')
    if 'price' in data:
        product.price = data.get('price')
    if 'stock' in data:
        product.stock = data.get('stock')
    if 'variants' in data:
        product.variants = data.get('variants')
    if 'category' in data:
        cat_name = data.get('category')
        if cat_name:
            from .models import Category
            cat, _ = Category.objects.get_or_create(name=cat_name)
            product.category = cat
    if request.FILES.get('image'):
        product.image = request.FILES.get('image')

    product.save()
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_api(request, product_id):
    """
    Delete a product if it belongs to the authenticated user's shop.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=404)

    try:
        user_shop = request.user.shop
    except Exception:
        return Response({'detail': 'You do not own a shop.'}, status=403)

    if product.shop_id != user_shop.id:
        return Response({'detail': 'Permission denied.'}, status=403)

    product.delete()
    return Response({'message': 'Product deleted.'}, status=204)


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
