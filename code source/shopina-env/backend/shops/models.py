from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User
from django.db.models import JSONField


class Shop(models.Model):
    """
    Represents a seller's shop on the Shopina platform.
    One shop per user - enforced at the database level.
    """
    
    # Owner relationship - one shop per user
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    
    # Shop information
    name = models.CharField(max_length=255, help_text="Name of the shop")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly shop identifier")
    description = models.TextField(blank=True, default="", help_text="Shop description")
    
    # Shop branding
    logo = models.ImageField(upload_to='shops/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='shops/banners/', blank=True, null=True)
    
    # Contact information
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Shop status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    # Statistics
    total_products = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    average_rating = models.FloatField(default=0.0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shops_shop'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['owner']),
            models.Index(fields=['is_active']),
        ]
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
    
    def __str__(self):
        return f"{self.name} (by {self.owner.username})"
    
    def save(self, *args, **kwargs):
        """
        Auto-generate slug and ensure one shop per user.
        """
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Ensure slug is unique
        existing = Shop.objects.filter(slug=self.slug).exclude(pk=self.pk)
        if existing.exists():
            self.slug = f"{self.slug}-{timezone.now().timestamp()}"
        
        super().save(*args, **kwargs)
        
        # Update user's shop_name and shop_slug
        self.owner.shop_name = self.name
        self.owner.shop_slug = self.slug
        self.owner.role = 'SELLER'
        self.owner.save(update_fields=['shop_name', 'shop_slug', 'role'])
    
    def delete(self, *args, **kwargs):
        """
        When shop is deleted, update user fields.
        """
        super().delete(*args, **kwargs)
        self.owner.shop_name = None
        self.owner.shop_slug = None
        self.owner.save(update_fields=['shop_name', 'shop_slug'])
    
    @property
    def get_absolute_url(self):
        """Get the absolute URL for this shop."""
        return f"/shop/{self.slug}/"


class ShopTheme(models.Model):
    """Active template and customization options per shop."""
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='theme')
    template_id = models.PositiveIntegerField()
    options = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shops_theme'
        verbose_name = 'Shop Theme'
        verbose_name_plural = 'Shop Themes'

    def __str__(self):
        return f"Theme for {self.shop.slug} (template {self.template_id})"
