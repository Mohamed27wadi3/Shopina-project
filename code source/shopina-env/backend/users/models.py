from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets


class User(AbstractUser):
    """
    Custom User model with extended fields for e-commerce platform.
    Supports three roles: Admin, Seller, and Customer.
    """
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('SELLER', 'Seller'),
        ('CUSTOMER', 'Customer'),
    ]
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    # Basic Information
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Role and Plan
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_slug = models.CharField(max_length=100, blank=True, null=True)
    
    # Address Information
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default='US')
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    # Password Reset
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    reset_password_expire = models.DateTimeField(blank=True, null=True)

    # Track last password change for audit / UI
    last_password_change = models.DateTimeField(blank=True, null=True)

    # Two-factor auth enabled
    two_factor_enabled = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']


class TwoFactor(models.Model):
    """Stores OTPs for two-factor authentication (email-based)."""
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='two_factors')
    otp_hash = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"TwoFactor(user={self.user.username}, verified={self.verified}, expires_at={self.expires_at})"

    def __str__(self):
        return f"{self.username} <{self.email}> ({self.get_role_display()})"
    
    def generate_reset_token(self):
        """Generate a password reset token valid for 1 hour."""
        self.reset_password_token = secrets.token_urlsafe(32)
        self.reset_password_expire = timezone.now() + timedelta(hours=1)
        self.save()
        return self.reset_password_token
    
    def is_reset_token_valid(self, token):
        """Check if the reset token is valid and not expired."""
        return (
            self.reset_password_token == token and
            self.reset_password_expire and
            timezone.now() < self.reset_password_expire
        )
    
    def clear_reset_token(self):
        """Clear the reset token after use."""
        self.reset_password_token = None
        self.reset_password_expire = None
        self.save()
