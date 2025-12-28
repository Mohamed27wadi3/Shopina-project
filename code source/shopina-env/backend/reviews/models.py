"""Review models for product reviews and ratings."""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Product


class Review(models.Model):
    """Product review model."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False, help_text="Verified purchase")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"
