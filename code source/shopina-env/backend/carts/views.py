"""
Cart views for API endpoints.
"""
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from core.utils.exceptions import (
    BusinessLogicError,
    InsufficientStockError,
    ResourceNotFoundError,
    ValidationError
)
from carts.services.cart_service import CartService
from carts.serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)


class CartView(APIView):
    """
    Get or clear user's cart.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_service = CartService()
    
    def get(self, request):
        """Get user's cart with all items."""
        cart = self.cart_service.get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        """Clear all items from cart."""
        self.cart_service.clear_cart(request.user)
        return Response({
            'message': 'Cart cleared successfully'
        }, status=status.HTTP_200_OK)


class CartItemView(APIView):
    """
    Add, update, or remove cart items.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_service = CartService()
    
    def post(self, request):
        """Add item to cart."""
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            cart_item = self.cart_service.add_to_cart(
                request.user,
                serializer.validated_data['product_id'],
                serializer.validated_data['quantity']
            )
            
            # Return updated cart
            cart = self.cart_service.get_or_create_cart(request.user)
            cart_serializer = CartSerializer(cart)
            
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
            
        except (ResourceNotFoundError, InsufficientStockError, 
                BusinessLogicError, ValidationError) as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """Update cart item quantity."""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            cart_item = self.cart_service.update_cart_item(
                request.user,
                pk,
                serializer.validated_data['quantity']
            )
            
            # Return updated cart
            cart = self.cart_service.get_or_create_cart(request.user)
            cart_serializer = CartSerializer(cart)
            
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
            
        except (ResourceNotFoundError, InsufficientStockError, 
                ValidationError) as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Remove item from cart."""
        try:
            self.cart_service.remove_from_cart(request.user, pk)
            
            # Return updated cart
            cart = self.cart_service.get_or_create_cart(request.user)
            cart_serializer = CartSerializer(cart)
            
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
            
        except ResourceNotFoundError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class CartValidateView(APIView):
    """
    Validate cart for checkout.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_service = CartService()
    
    def get(self, request):
        """Validate cart for checkout."""
        is_valid, error_message = self.cart_service.validate_cart_for_checkout(request.user)
        
        if is_valid:
            return Response({
                'valid': True,
                'message': 'Cart is valid for checkout'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'valid': False,
                'message': error_message
            }, status=status.HTTP_400_BAD_REQUEST)
