"""
Custom exception classes for the application.

DESIGN PATTERNS UTILISÉS:
=======================

1. EXCEPTION PATTERN / CUSTOM EXCEPTION PATTERN:
   - Définit des exceptions spécifiques au métier
   - Chaque exception représente un type d'erreur particulier
   - Permet une gestion d'erreurs précise et granulaire

2. HIERARCHY PATTERN (Héritage):
   - BusinessLogicError est la classe mère
   - InsufficientStockError, PaymentError héritent
   - Crée une hiérarchie d'exceptions

3. STRATEGY PATTERN (via status_code):
   - Chaque exception a une stratégie de réponse HTTP différente
   - InsufficientStockError → 400 Bad Request
   - PaymentError → 402 Payment Required
   - UnauthorizedAccessError → 403 Forbidden

UTILISATION:
try:
    # logique métier
except InsufficientStockError as e:
    # gère l'erreur de stock
except PaymentError as e:
    # gère l'erreur de paiement

AVANTAGES:
✅ Exceptions métier clairement nommées
✅ Code métier plus lisible (pas de "generic errors")
✅ Gestion d'erreurs granulaire et précise
✅ Messages d'erreurs cohérents
✅ Status HTTP appropriés pour chaque erreur

PRINCIPES SOLID: S (Single Responsibility)
- Chaque exception a UNE responsabilité: définir un type d'erreur
- InsufficientStockError DÉFINIT l'erreur, ne la gère pas
- La gestion est dans les Views/Services
"""
from rest_framework.exceptions import APIException
from rest_framework import status


# EXCEPTION PATTERN: Classe mère pour toutes les erreurs métier
# S - Single Responsibility: définit UNIQUEMENT les erreurs de logique métier
class BusinessLogicError(APIException):
    """
    Exception raised when business logic validation fails.
    Classe mère pour toutes les erreurs métier (Stock, Paiement, etc.)
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic validation failed.'
    default_code = 'business_logic_error'


# EXCEPTION PATTERN: Exception spécifique pour erreur de stock
class InsufficientStockError(BusinessLogicError):
    """
    Exception raised when product stock is insufficient.
    STRATEGY PATTERN: Status 400
    """
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'


# EXCEPTION PATTERN: Exception spécifique pour état d'ordre invalide
class InvalidOrderStateError(BusinessLogicError):
    """
    Exception raised when order is in invalid state for operation.
    STRATEGY PATTERN: Status 400
    """
    default_detail = 'Order is in invalid state for this operation.'
    default_code = 'invalid_order_state'


# EXCEPTION PATTERN: Exception spécifique pour erreur paiement
# STRATEGY PATTERN: Status code différent (402 au lieu de 400)
class PaymentError(APIException):
    """
    Exception raised when payment processing fails.
    STRATEGY PATTERN: Status 402 (Payment Required)
    """
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Payment processing failed.'
    default_code = 'payment_error'


# EXCEPTION PATTERN: Exception spécifique pour accès non autorisé
# STRATEGY PATTERN: Status code différent (403)
class UnauthorizedAccessError(APIException):
    """
    Exception raised when user attempts unauthorized access.
    STRATEGY PATTERN: Status 403 (Forbidden)
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'unauthorized_access'


class ResourceNotFoundError(APIException):
    """
    Exception raised when requested resource is not found.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Requested resource not found.'
    default_code = 'resource_not_found'


class DuplicateResourceError(BusinessLogicError):
    """
    Exception raised when attempting to create duplicate resource.
    """
    default_detail = 'Resource already exists.'
    default_code = 'duplicate_resource'


class ValidationError(BusinessLogicError):
    """
    Exception raised when data validation fails.
    """
    default_detail = 'Data validation failed.'
    default_code = 'validation_error'
