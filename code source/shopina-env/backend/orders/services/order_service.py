"""
Order service for business logic operations.
"""
from typing import Dict, Any, List
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction
from core.services.base import BaseService
from core.utils.exceptions import (
    BusinessLogicError,
    ResourceNotFoundError,
    InvalidOrderStateError,
    InsufficientStockError
)
from orders.models import Order, OrderItem
from orders.repositories.order_repository import OrderRepository, OrderItemRepository
from carts.services.cart_service import CartService
from shop.services.product_service import ProductService


User = get_user_model()


class OrderService(BaseService[Order]):
    """
    Service class for Order business logic.
    """
    
    def __init__(self):
        self.order_repository = OrderRepository()
        self.order_item_repository = OrderItemRepository()
        self.cart_service = CartService()
        self.product_service = ProductService()
        super().__init__(self.order_repository)
    
    @transaction.atomic
    def create_order_from_cart(self, user: User, shipping_address: Dict[str, str] = None) -> Order:
        """
        Create order from user's cart.
        
        Args:
            user: User instance
            shipping_address: Shipping address details
            
        Returns:
            Created order
            
        Raises:
            BusinessLogicError: If cart is empty or invalid
            InsufficientStockError: If insufficient stock
        """
        # Validate cart
        is_valid, error_msg = self.cart_service.validate_cart_for_checkout(user)
        if not is_valid:
            raise BusinessLogicError(error_msg)
        
        # Get cart
        cart = self.cart_service.cart_repository.get_user_cart(user)
        if not cart or cart.total_items == 0:
            raise BusinessLogicError("Cart is empty")
        
        # Create order
        order = Order.objects.create(
            user=user,
            total=cart.total_price,
            status='pending'
        )
        
        # Create order items and decrease stock
        for cart_item in cart.items.all():
            # Decrease product stock
            try:
                self.product_service.decrease_stock(
                    cart_item.product.id,
                    cart_item.quantity
                )
            except InsufficientStockError:
                # Rollback will happen automatically due to @transaction.atomic
                raise
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.price_at_add,
                quantity=cart_item.quantity
            )
        
        # Clear cart
        self.cart_service.clear_cart(user)
        
        self.log_operation('order_created', {
            'user_id': user.id,
            'order_id': order.id,
            'total': float(order.total)
        })
        
        return order
    
    def get_user_orders(self, user: User):
        """
        Get all orders for a user.
        
        Args:
            user: User instance
            
        Returns:
            QuerySet of orders
        """
        return self.order_repository.get_user_orders(user)
    
    def update_order_status(self, order_id: int, new_status: str) -> Order:
        """
        Update order status.
        
        Args:
            order_id: Order ID
            new_status: New status
            
        Returns:
            Updated order
            
        Raises:
            ResourceNotFoundError: If order not found
            InvalidOrderStateError: If status transition is invalid
        """
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ResourceNotFoundError("Order not found")
        
        # Validate status transition
        valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            raise InvalidOrderStateError(f"Invalid status: {new_status}")
        
        # Cannot change status of completed or cancelled orders
        if order.status in ['completed', 'cancelled']:
            raise InvalidOrderStateError(
                f"Cannot change status of {order.status} order"
            )
        
        order = self.order_repository.update(order, status=new_status)
        
        self.log_operation('order_status_updated', {
            'order_id': order_id,
            'new_status': new_status
        })
        
        return order
    
    @transaction.atomic
    def cancel_order(self, order_id: int, user: User) -> Order:
        """
        Cancel an order and restore stock.
        
        Args:
            order_id: Order ID
            user: User requesting cancellation
            
        Returns:
            Cancelled order
            
        Raises:
            ResourceNotFoundError: If order not found
            InvalidOrderStateError: If order cannot be cancelled
        """
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ResourceNotFoundError("Order not found")
        
        # Check ownership
        if order.user != user:
            raise BusinessLogicError("You can only cancel your own orders")
        
        # Can only cancel pending orders
        if order.status != 'pending':
            raise InvalidOrderStateError(
                "Only pending orders can be cancelled"
            )
        
        # Restore stock for all items
        for item in order.items.all():
            self.product_service.increase_stock(
                item.product.id,
                item.quantity
            )
        
        # Update order status
        order = self.order_repository.update(order, status='cancelled')
        
        self.log_operation('order_cancelled', {
            'order_id': order_id,
            'user_id': user.id
        })
        
        return order
    
    def get_order_statistics(self) -> Dict[str, Any]:
        """
        Get order statistics for admin dashboard.
        
        Returns:
            Dictionary with statistics
        """
        return self.order_repository.get_order_statistics()
