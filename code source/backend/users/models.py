from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    email = models.EmailField(unique=True)
    avatar = models.URLField(blank=True, null=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    shop_name = models.CharField(max_length=255, blank=True, null=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} <{self.email}>"
