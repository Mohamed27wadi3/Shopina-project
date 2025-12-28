"""
Order repository for data access operations.
"""
from typing import Optional, Dict, Any
from django.db.models import QuerySet, Sum, Count, Q
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from core.repositories.base import BaseRepository
from orders.models import Order, OrderItem


User = get_user_model()


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order model data access.
    """
    
    def __init__(self):
        super().__init__(Order)
    
    def get_user_orders(self, user: User) -> QuerySet[Order]:
        """
        Get all orders for a user.
        
        Args:
            user: User instance
            
        Returns:
            QuerySet of orders
        """
        return self.model.objects.filter(user=user).prefetch_related('items__product')
    
    def get_by_status(self, status: str) -> QuerySet[Order]:
        """
        Get orders by status.
        
        Args:
            status: Order status
            
        Returns:
            QuerySet of orders
        """
        return self.model.objects.filter(status=status)
    
    def get_recent_orders(self, limit: int = 10) -> QuerySet[Order]:
        """
        Get recent orders.
        
        Args:
            limit: Number of orders
            
        Returns:
            QuerySet of recent orders
        """
        return self.model.objects.order_by('-created_at')[:limit]
    
    def get_order_statistics(self) -> Dict[str, Any]:
        """
        Get order statistics for dashboard.
        
        Returns:
            Dictionary with statistics
        """
        total_orders = self.model.objects.count()
        total_revenue = self.model.objects.aggregate(total=Sum('total'))['total'] or 0
        
        orders_by_status = self.model.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Orders in last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_orders = self.model.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()
        
        return {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'orders_by_status': {item['status']: item['count'] for item in orders_by_status},
            'recent_orders_30_days': recent_orders,
        }


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository for OrderItem model data access.
    """
    
    def __init__(self):
        super().__init__(OrderItem)
    
    def get_order_items(self, order: Order) -> QuerySet[OrderItem]:
        """
        Get all items for an order.
        
        Args:
            order: Order instance
            
        Returns:
            QuerySet of order items
        """
        return self.model.objects.filter(order=order).select_related('product')
