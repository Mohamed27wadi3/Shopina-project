"""Notification models for user notifications."""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """User notification model."""
    
    TYPE_CHOICES = [
        ('ORDER', 'Order Update'),
        ('PAYMENT', 'Payment'),
        ('PRODUCT', 'Product'),
        ('SYSTEM', 'System'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
