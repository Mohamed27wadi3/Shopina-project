# PATTERN MVC: MODEL (M)
# ========================
# Les Order models représentent les commandes en base de données
# Voir shop/models.py pour la documentation complète du pattern MVC

from django.db import models
from django.conf import settings


# M - MODEL: Classe qui représente une COMMANDE (TABLE 'orders_order')
class Order(models.Model):
    """Commande d'un utilisateur.
    Représente la table 'orders_order' en base de données.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user}"


# M - MODEL: Classe qui représente les ARTICLES d'une commande (TABLE 'orders_orderitem')
class OrderItem(models.Model):
    """Article dans une commande.
    Représente la table 'orders_orderitem' en base de données.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('shop.Product', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        """Calculate line total (price × quantity)"""
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product}"
