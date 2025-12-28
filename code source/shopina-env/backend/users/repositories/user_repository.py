"""
User repository for data access operations.
"""
from typing import Optional, List
from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Count, Q
from core.repositories.base import BaseRepository


User = get_user_model()


class UserRepository(BaseRepository[User]):
    """
    Repository for User model data access.
    """
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User email
            
        Returns:
            User instance or None
        """
        try:
            return self.model.objects.get(email__iexact=email)
        except self.model.DoesNotExist:
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            User instance or None
        """
        try:
            return self.model.objects.get(username__iexact=username)
        except self.model.DoesNotExist:
            return None
    
    def get_by_reset_token(self, token: str) -> Optional[User]:
        """
        Get user by password reset token.
        
        Args:
            token: Reset token
            
        Returns:
            User instance or None
        """
        try:
            return self.model.objects.get(reset_password_token=token)
        except self.model.DoesNotExist:
            return None
    
    def get_users_by_role(self, role: str) -> QuerySet[User]:
        """
        Get all users with specific role.
        
        Args:
            role: User role (ADMIN, SELLER, CUSTOMER)
            
        Returns:
            QuerySet of users
        """
        return self.model.objects.filter(role=role)
    
    def search_users(self, query: str) -> QuerySet[User]:
        """
        Search users by username, email, or name.
        
        Args:
            query: Search query
            
        Returns:
            QuerySet of matching users
        """
        return self.model.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    def get_user_statistics(self) -> dict:
        """
        Get user statistics for admin dashboard.
        
        Returns:
            Dictionary with user statistics
        """
        total_users = self.model.objects.count()
        users_by_role = self.model.objects.values('role').annotate(count=Count('id'))
        
        return {
            'total_users': total_users,
            'users_by_role': {item['role']: item['count'] for item in users_by_role},
            'verified_users': self.model.objects.filter(is_verified=True).count(),
            'unverified_users': self.model.objects.filter(is_verified=False).count(),
        }
    
    def email_exists(self, email: str) -> bool:
        """
        Check if email already exists.
        
        Args:
            email: Email to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.model.objects.filter(email__iexact=email).exists()
    
    def username_exists(self, username: str) -> bool:
        """
        Check if username already exists.
        
        Args:
            username: Username to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.model.objects.filter(username__iexact=username).exists()
