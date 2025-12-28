"""
Product repository for data access operations.
"""
from typing import Optional, List
from django.db.models import QuerySet, Q, Avg
from core.repositories.base import BaseRepository
from shop.models import Product, Category


class ProductRepository(BaseRepository[Product]):
    """
    Repository for Product model data access.
    """
    
    def __init__(self):
        super().__init__(Product)
    
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """
        Get product by slug.
        
        Args:
            slug: Product slug
            
        Returns:
            Product instance or None
        """
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None
    
    def get_active_products(self) -> QuerySet[Product]:
        """
        Get all active products.
        
        Returns:
            QuerySet of active products
        """
        return self.model.objects.filter(stock__gt=0).select_related('category')
    
    def get_by_category(self, category_id: int) -> QuerySet[Product]:
        """
        Get products by category.
        
        Args:
            category_id: Category ID
            
        Returns:
            QuerySet of products
        """
        return self.model.objects.filter(category_id=category_id).select_related('category')
    
    def search_products(self, query: str) -> QuerySet[Product]:
        """
        Search products by name or description.
        
        Args:
            query: Search query
            
        Returns:
            QuerySet of matching products
        """
        return self.model.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).select_related('category')
    
    def get_top_rated(self, limit: int = 10) -> QuerySet[Product]:
        """
        Get top rated products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            QuerySet of top rated products
        """
        return self.model.objects.order_by('-rating')[:limit]
    
    def get_featured_products(self, limit: int = 10) -> QuerySet[Product]:
        """
        Get featured products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            QuerySet of featured products
        """
        # For now, return top rated. Can add 'featured' field later
        return self.get_top_rated(limit)
    
    def update_stock(self, product: Product, quantity_change: int) -> Product:
        """
        Update product stock.
        
        Args:
            product: Product instance
            quantity_change: Change in stock (positive or negative)
            
        Returns:
            Updated product
        """
        product.stock += quantity_change
        product.save()
        return product
    
    def update_rating(self, product: Product) -> Product:
        """
        Update product rating based on reviews.
        
        Args:
            product: Product instance
            
        Returns:
            Updated product
        """
        from reviews.models import Review
        
        avg_rating = Review.objects.filter(product=product).aggregate(
            avg=Avg('rating')
        )['avg']
        
        if avg_rating:
            product.rating = round(avg_rating, 1)
            product.reviews = Review.objects.filter(product=product).count()
            product.save()
        
        return product


class CategoryRepository(BaseRepository[Category]):
    """
    Repository for Category model data access.
    """
    
    def __init__(self):
        super().__init__(Category)
    
    def get_by_name(self, name: str) -> Optional[Category]:
        """
        Get category by name.
        
        Args:
            name: Category name
            
        Returns:
            Category instance or None
        """
        try:
            return self.model.objects.get(name__iexact=name)
        except self.model.DoesNotExist:
            return None
    
    def get_with_product_count(self):
        """
        Get categories with product count.
        
        Returns:
            QuerySet with annotations
        """
        from django.db.models import Count
        return self.model.objects.annotate(product_count=Count('products'))
