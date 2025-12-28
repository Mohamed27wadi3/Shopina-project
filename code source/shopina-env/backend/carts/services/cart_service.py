"""
Cart service for business logic operations.
"""
from typing import Dict, Any
from decimal import Decimal
from django.contrib.auth import get_user_model
from core.services.base import BaseService
from core.utils.exceptions import (
    BusinessLogicError,
    InsufficientStockError,
    ResourceNotFoundError,
    ValidationError
)
from core.utils.validators import validate_quantity
from carts.models import Cart, CartItem
from carts.repositories.cart_repository import CartRepository, CartItemRepository
from shop.models import Product


User = get_user_model()


class CartService(BaseService[Cart]):
    """
    Service class for Cart business logic.
    Handles cart operations with stock validation.
    """
    
    def __init__(self):
        self.cart_repository = CartRepository()
        self.cart_item_repository = CartItemRepository()
        super().__init__(self.cart_repository)
    
    def get_or_create_cart(self, user: User) -> Cart:
        """
        Get or create cart for user.
        
        Args:
            user: User instance
            
        Returns:
            Cart instance
        """
        cart, created = self.cart_repository.get_or_create_cart(user)
        if created:
            self.log_operation('cart_created', {'user_id': user.id})
        return cart
    
    def add_to_cart(self, user: User, product_id: int, quantity: int = 1) -> CartItem:
        """
        Add product to cart with stock validation.
        
        Args:
            user: User instance
            product_id: Product ID
            quantity: Quantity to add
            
        Returns:
            CartItem instance
            
        Raises:
            ResourceNotFoundError: If product not found
            InsufficientStockError: If insufficient stock
            ValidationError: If quantity is invalid
        """
        # Validate quantity
        is_valid, error_msg = validate_quantity(quantity)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Get or create cart
        cart = self.get_or_create_cart(user)
        
        # Get product
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ResourceNotFoundError("Product not found")
        
        # Check if product is active
        if hasattr(product, 'is_active') and not product.is_active:
            raise BusinessLogicError("Product is not available")
        
        # Check stock availability
        existing_item = self.cart_item_repository.get_cart_item(cart, product)
        total_quantity = quantity
        if existing_item:
            total_quantity += existing_item.quantity
        
        if total_quantity > product.stock:
            raise InsufficientStockError(
                f"Only {product.stock} items available in stock"
            )
        
        # Add or update cart item
        if existing_item:
            existing_item.quantity = total_quantity
            existing_item.save()
            cart_item = existing_item
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                price_at_add=product.price
            )
        
        self.log_operation('item_added_to_cart', {
            'user_id': user.id,
            'product_id': product_id,
            'quantity': quantity
        })
        
        return cart_item
    
    def update_cart_item(self, user: User, cart_item_id: int, quantity: int) -> CartItem:
        """
        Update cart item quantity.
        
        Args:
            user: User instance
            cart_item_id: CartItem ID
            quantity: New quantity
            
        Returns:
            Updated CartItem instance
            
        Raises:
            ResourceNotFoundError: If cart item not found
            InsufficientStockError: If insufficient stock
            ValidationError: If quantity is invalid
        """
        # Validate quantity
        is_valid, error_msg = validate_quantity(quantity)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Get cart item
        try:
            cart_item = CartItem.objects.select_related('product', 'cart').get(
                pk=cart_item_id,
                cart__user=user
            )
        except CartItem.DoesNotExist:
            raise ResourceNotFoundError("Cart item not found")
        
        # Check stock
        if quantity > cart_item.product.stock:
            raise InsufficientStockError(
                f"Only {cart_item.product.stock} items available in stock"
            )
        
        # Update quantity
        cart_item.quantity = quantity
        cart_item.save()
        
        self.log_operation('cart_item_updated', {
            'user_id': user.id,
            'cart_item_id': cart_item_id,
            'new_quantity': quantity
        })
        
        return cart_item
    
    def remove_from_cart(self, user: User, cart_item_id: int) -> None:
        """
        Remove item from cart.
        
        Args:
            user: User instance
            cart_item_id: CartItem ID
            
        Raises:
            ResourceNotFoundError: If cart item not found
        """
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id, cart__user=user)
            cart_item.delete()
            
            self.log_operation('item_removed_from_cart', {
                'user_id': user.id,
                'cart_item_id': cart_item_id
            })
        except CartItem.DoesNotExist:
            raise ResourceNotFoundError("Cart item not found")
    
    def clear_cart(self, user: User) -> None:
        """
        Clear all items from cart.
        
        Args:
            user: User instance
        """
        cart = self.cart_repository.get_user_cart(user)
        if cart:
            self.cart_repository.clear_cart(cart)
            self.log_operation('cart_cleared', {'user_id': user.id})
    
    def get_cart_summary(self, user: User) -> Dict[str, Any]:
        """
        Get cart summary with totals.
        
        Args:
            user: User instance
            
        Returns:
            Dictionary with cart summary
        """
        cart = self.cart_repository.get_user_cart(user)
        if not cart:
            return {
                'total_items': 0,
                'total_price': Decimal('0.00'),
                'items': []
            }
        
        items = self.cart_item_repository.get_cart_items(cart)
        
        return {
            'total_items': cart.total_items,
            'total_price': cart.total_price,
            'items': items
        }
    
    def validate_cart_for_checkout(self, user: User) -> tuple[bool, str]:
        """
        Validate cart before checkout.
        
        Args:
            user: User instance
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        cart = self.cart_repository.get_user_cart(user)
        if not cart or cart.total_items == 0:
            return False, "Cart is empty"
        
        # Check stock for all items
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                return False, f"Insufficient stock for {item.product.name}"
        
        return True, ""
