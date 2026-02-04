"""
Base service class for all business logic services.
Following the Service Layer Pattern.

DESIGN PATTERNS UTILISÉS:
=======================

1. SERVICE LAYER PATTERN (Principal):
   - Encapsule toute la logique métier
   - Centralise les opérations complexes
   - Réutilisable par plusieurs Views/Contrôleurs
   - Utilisé: BaseService pour la logique commune, ProductService pour logique métier produit

2. GENERIC/TEMPLATE PATTERN:
   - Generic[ModelType] permet de réutiliser pour n'importe quel Model
   - validate_business_rules(), log_operation() fonctionnent pour tous
   - Évite duplication de code

3. TEMPLATE METHOD PATTERN:
   - BaseService définit le "template" (structure)
   - validate_business_rules() et log_operation() sont les points d'extension
   - Les enfants (ProductService) implémentent/surcharger ces méthodes
   - Contrôle du flux sans duplication

4. DEPENDENCY INJECTION PATTERN:
   - Le repository est injecté via le constructeur
   - Pas de dépendances hardcodées
   - Facile de remplacer le repository par un mock (tests)

FLUX MVC COMPLET:
HTTP Request
    ↓
  VIEW (gère la requête HTTP)
    ↓
SERVICE (logique métier, c'est ICI) ← Vous êtes ici
    ↓
REPOSITORY (accès aux données)
    ↓
MODEL → DATABASE (stockage physique)

AVANTAGES:
✅ Logique métier centralisée et testable
✅ Réutilisable (mobile app, CLI, script peuvent utiliser le Service)
✅ Facile à maintenir (logique métier centralisée)
✅ Facile de changer la BDD (juste changer Repository)
✅ Template Method évite duplication
"""
from typing import Generic, TypeVar, Optional, List
from django.db import models


ModelType = TypeVar('ModelType', bound=models.Model)


# C - CONTROLLER/SERVICE: Classe de base pour tous les services
class BaseService(Generic[ModelType]):
    """
    Base service class that provides common business logic patterns.
    All service classes should inherit from this base class.
    """
    
    def __init__(self, repository=None):
        """
        Initialize service with optional repository.
        
        Args:
            repository: Repository instance for data access
        """
        self.repository = repository
    
    def validate_business_rules(self, data: dict) -> tuple[bool, Optional[str]]:
        """
        Validate business rules before performing operations.
        Override this method in child classes.
        
        Args:
            data: Data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        return True, None
    
    def log_operation(self, operation: str, details: dict):
        """
        Log service operations for audit trail.
        
        Args:
            operation: Name of the operation
            details: Operation details
        """
        # TODO: Implement proper logging
        pass
