"""
Product service for business logic operations.
"""
from typing import Optional, List, Dict, Any
from django.db.models import QuerySet
from core.services.base import BaseService
from core.utils.exceptions import (
    BusinessLogicError,
    ResourceNotFoundError,
    ValidationError,
    InsufficientStockError
)
from core.utils.validators import validate_price, validate_quantity
from shop.models import Product, Category
from shop.repositories.product_repository import ProductRepository, CategoryRepository


class ProductService(BaseService[Product]):
    """
    Service class for Product business logic.
    """
    
    def __init__(self):
        self.product_repository = ProductRepository()
        self.category_repository = CategoryRepository()
        super().__init__(self.product_repository)
    
    def create_product(self, name: str, price: float, category_id: int,
                      description: str = '', stock: int = 0, **kwargs) -> Product:
        """
        Create a new product.
        
        Args:
            name: Product name
            price: Product price
            category_id: Category ID
            description: Product description
            stock: Initial stock
            **kwargs: Additional fields
            
        Returns:
            Created product
            
        Raises:
            ValidationError: If validation fails
            ResourceNotFoundError: If category not found
        """
        # Validate price
        is_valid, error_msg = validate_price(price)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Validate stock
        if stock < 0:
            raise ValidationError("Stock cannot be negative")
        
        # Get category
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ResourceNotFoundError("Category not found")
        
        # Create product
        product = Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            stock=stock,
            **kwargs
        )
        
        self.log_operation('product_created', {'product_id': product.id})
        return product
    
    def update_product(self, product_id: int, **kwargs) -> Product:
        """
        Update product.
        
        Args:
            product_id: Product ID
            **kwargs: Fields to update
            
        Returns:
            Updated product
            
        Raises:
            ResourceNotFoundError: If product not found
            ValidationError: If validation fails
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Product not found")
        
        # Validate price if being updated
        if 'price' in kwargs:
            is_valid, error_msg = validate_price(kwargs['price'])
            if not is_valid:
                raise ValidationError(error_msg)
        
        # Validate stock if being updated
        if 'stock' in kwargs and kwargs['stock'] < 0:
            raise ValidationError("Stock cannot be negative")
        
        # Update product
        product = self.product_repository.update(product, **kwargs)
        self.log_operation('product_updated', {'product_id': product_id})
        return product
    
    def delete_product(self, product_id: int) -> None:
        """
        Delete product.
        
        Args:
            product_id: Product ID
            
        Raises:
            ResourceNotFoundError: If product not found
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Product not found")
        
        self.product_repository.delete(product)
        self.log_operation('product_deleted', {'product_id': product_id})
    
    def search_products(self, query: str = '', category_id: Optional[int] = None) -> QuerySet[Product]:
        """
        Search products with filters.
        
        Args:
            query: Search query
            category_id: Filter by category
            
        Returns:
            QuerySet of products
        """
        if category_id:
            products = self.product_repository.get_by_category(category_id)
        elif query:
            products = self.product_repository.search_products(query)
        else:
            products = self.product_repository.get_active_products()
        
        return products
    
    def get_featured_products(self, limit: int = 10) -> QuerySet[Product]:
        """
        Get featured products.
        
        Args:
            limit: Number of products
            
        Returns:
            QuerySet of featured products
        """
        return self.product_repository.get_featured_products(limit)
    
    def decrease_stock(self, product_id: int, quantity: int) -> Product:
        """
        Decrease product stock (for order processing).
        
        Args:
            product_id: Product ID
            quantity: Quantity to decrease
            
        Returns:
            Updated product
            
        Raises:
            ResourceNotFoundError: If product not found
            InsufficientStockError: If insufficient stock
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Product not found")
        
        if product.stock < quantity:
            raise InsufficientStockError(f"Only {product.stock} items available")
        
        product = self.product_repository.update_stock(product, -quantity)
        self.log_operation('stock_decreased', {
            'product_id': product_id,
            'quantity': quantity
        })
        return product
    
    def increase_stock(self, product_id: int, quantity: int) -> Product:
        """
        Increase product stock (for restocking or order cancellation).
        
        Args:
            product_id: Product ID
            quantity: Quantity to increase
            
        Returns:
            Updated product
            
        Raises:
            ResourceNotFoundError: If product not found
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Product not found")
        
        product = self.product_repository.update_stock(product, quantity)
        self.log_operation('stock_increased', {
            'product_id': product_id,
            'quantity': quantity
        })
        return product
    
    def update_product_rating(self, product_id: int) -> Product:
        """
        Update product rating based on reviews.
        
        Args:
            product_id: Product ID
            
        Returns:
            Updated product
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Product not found")
        
        return self.product_repository.update_rating(product)


class CategoryService(BaseService[Category]):
    """
    Service class for Category business logic.
    """
    
    def __init__(self):
        self.repository = CategoryRepository()
        super().__init__(self.repository)
    
    def create_category(self, name: str) -> Category:
        """
        Create a new category.
        
        Args:
            name: Category name
            
        Returns:
            Created category
            
        Raises:
            ValidationError: If category already exists
        """
        if self.repository.get_by_name(name):
            raise ValidationError("Category already exists")
        
        category = self.repository.create(name=name)
        self.log_operation('category_created', {'category_id': category.id})
        return category
    
    def get_categories_with_count(self):
        """
        Get categories with product count.
        
        Returns:
            QuerySet with product counts
        """
        return self.repository.get_with_product_count()
