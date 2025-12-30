from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    # Link product to a Shop (optional)
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Allow uploading images for products
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    # Optional variants/options stored as JSON, example: [{"sku":"S-RED","options":{"size":"S","color":"red"},"price":9.99,"stock":5}]
    variants = models.JSONField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
