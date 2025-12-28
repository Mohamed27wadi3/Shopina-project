"""
Base service class for all business logic services.
Following the Service Layer Pattern.
"""
from typing import Generic, TypeVar, Optional, List
from django.db import models


ModelType = TypeVar('ModelType', bound=models.Model)


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
