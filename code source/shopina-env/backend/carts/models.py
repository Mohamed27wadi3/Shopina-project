"""
Cart models for shopping cart functionality.
"""
from django.db import models
from django.conf import settings
from shop.models import Product


class Cart(models.Model):
    """
    Shopping cart model.
    Each user has one active cart.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_items(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Calculate total price of all items in cart."""
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    """
    Individual item in a shopping cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_add = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of product when added to cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this cart item."""
        return self.price_at_add * self.quantity
    
    def save(self, *args, **kwargs):
        """Set price_at_add if not set."""
        if not self.price_at_add:
            self.price_at_add = self.product.price
        super().save(*args, **kwargs)
