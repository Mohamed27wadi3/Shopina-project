"""
Cart repository for data access operations.
"""
from typing import Optional
from django.contrib.auth import get_user_model
from core.repositories.base import BaseRepository
from carts.models import Cart, CartItem
from shop.models import Product


User = get_user_model()


class CartRepository(BaseRepository[Cart]):
    """
    Repository for Cart model data access.
    """
    
    def __init__(self):
        super().__init__(Cart)
    
    def get_or_create_cart(self, user: User) -> tuple[Cart, bool]:
        """
        Get or create cart for user.
        
        Args:
            user: User instance
            
        Returns:
            Tuple of (cart, created)
        """
        return self.model.objects.get_or_create(user=user)
    
    def get_user_cart(self, user: User) -> Optional[Cart]:
        """
        Get cart for user.
        
        Args:
            user: User instance
            
        Returns:
            Cart instance or None
        """
        try:
            return self.model.objects.get(user=user)
        except self.model.DoesNotExist:
            return None
    
    def clear_cart(self, cart: Cart) -> None:
        """
        Clear all items from cart.
        
        Args:
            cart: Cart instance
        """
        cart.items.all().delete()


class CartItemRepository(BaseRepository[CartItem]):
    """
    Repository for CartItem model data access.
    """
    
    def __init__(self):
        super().__init__(CartItem)
    
    def get_cart_item(self, cart: Cart, product: Product) -> Optional[CartItem]:
        """
        Get specific cart item.
        
        Args:
            cart: Cart instance
            product: Product instance
            
        Returns:
            CartItem instance or None
        """
        try:
            return self.model.objects.get(cart=cart, product=product)
        except self.model.DoesNotExist:
            return None
    
    def get_cart_items(self, cart: Cart):
        """
        Get all items in cart.
        
        Args:
            cart: Cart instance
            
        Returns:
            QuerySet of CartItems
        """
        return self.model.objects.filter(cart=cart).select_related('product', 'product__category')
