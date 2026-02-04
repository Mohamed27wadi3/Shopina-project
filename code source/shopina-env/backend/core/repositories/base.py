"""
Base repository class for data access abstraction.
Following the Repository Pattern.

DESIGN PATTERNS UTILISÉS:
=======================

1. REPOSITORY PATTERN (Principal):
   - Centralise l'accès aux données
   - Masque les détails de la base de données
   - Permet de changer de BDD sans toucher au code métier
   - Utilisé: BaseRepository comme classe mère, ProductRepository, OrderRepository en enfants

2. GENERIC/TEMPLATE PATTERN:
   - Generic[ModelType] permet de réutiliser BaseRepository pour n'importe quel Model
   - get_by_id(), get_all(), filter() fonctionnent pour tous les Models
   - Évite la duplication de code

3. ABSTRACT CLASS PATTERN:
   - BaseRepository est une classe abstraite (de facto)
   - Définit l'interface que tous les repositories doivent suivre
   - Les enfants (ProductRepository) héritent et étendent

4. DATA ACCESS OBJECT (DAO) PATTERN:
   - Repository = Data Access Object
   - Encapsule la logique d'accès aux données
   - Simplifie l'interaction avec la BDD

FLUX MVC COMPLET:
HTTP Request
    ↓
  VIEW (gère la requête HTTP)
    ↓
SERVICE (logique métier, utilise Repository pour les données)
    ↓
REPOSITORY (accès aux données, c'est ICI) ← Vous êtes ici
    ↓
MODEL → DATABASE (stockage physique)

AVANTAGES:
✅ Séparation des responsabilités (S du SOLID)
✅ Facile de changer la BDD (juste modifier le Repository)
✅ Facile de tester (on peut mocker le Repository)
✅ Code métier indépendant de la BDD
✅ Pas de duplication (Generic[ModelType])
"""
from typing import Generic, TypeVar, Optional, List, Dict, Any
from django.db import models
from django.db.models import QuerySet


ModelType = TypeVar('ModelType', bound=models.Model)


# R - REPOSITORY: Classe de base pour tous les accès données
class BaseRepository(Generic[ModelType]):
    """
    Base repository class that provides common data access patterns.
    All repository classes should inherit from this base class.
    """
    
    def __init__(self, model: type[ModelType]):
        """
        Initialize repository with model class.
        
        Args:
            model: Django model class
        """
        self.model = model
    
    # S - Responsabilité Unique: Cette méthode fait UNE CHOSE: récupérer par ID
    # L - Liskov: Retourne Optional[ModelType] comme tous les enfants attendent
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get a single instance by ID.
        
        Args:
            id: Primary key of the instance
            
        Returns:
            Model instance or None
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
    
    def get_all(self) -> QuerySet[ModelType]:
        """
        Get all instances.
        
        Returns:
            QuerySet of all instances
        """
        return self.model.objects.all()
    
    def filter(self, **kwargs) -> QuerySet[ModelType]:
        """
        Filter instances by criteria.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            Filtered QuerySet
        """
        return self.model.objects.filter(**kwargs)
    
    def create(self, **kwargs) -> ModelType:
        """
        Create a new instance.
        
        Args:
            **kwargs: Instance data
            
        Returns:
            Created instance
        """
        return self.model.objects.create(**kwargs)
    
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """
        Update an existing instance.
        
        Args:
            instance: Instance to update
            **kwargs: Updated data
            
        Returns:
            Updated instance
        """
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def delete(self, instance: ModelType) -> None:
        """
        Delete an instance.
        
        Args:
            instance: Instance to delete
        """
        instance.delete()
    
    def exists(self, **kwargs) -> bool:
        """
        Check if instance exists.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            True if exists, False otherwise
        """
        return self.model.objects.filter(**kwargs).exists()
    
    def count(self, **kwargs) -> int:
        """
        Count instances.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            Count of instances
        """
        return self.model.objects.filter(**kwargs).count()
