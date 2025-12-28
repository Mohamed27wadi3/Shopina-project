"""
Custom permission classes for role-based access control.
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to admin users.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated and has admin role.
        """
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and
            request.user.role == 'ADMIN'
        )


class IsSeller(permissions.BasePermission):
    """
    Permission class that allows access to sellers and admins.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated and has seller or admin role.
        """
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and
            request.user.role in ['SELLER', 'ADMIN']
        )


class IsCustomer(permissions.BasePermission):
    """
    Permission class that allows access to customers.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated and has customer role.
        """
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and
            request.user.role == 'CUSTOMER'
        )


class IsOwner(permissions.BasePermission):
    """
    Permission class that allows access only to the owner of the object.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is the owner of the object.
        Object must have a 'user' attribute.
        """
        return obj.user == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class that allows access to the owner or admin.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is the owner or an admin.
        """
        is_owner = obj.user == request.user
        is_admin = hasattr(request.user, 'role') and request.user.role == 'ADMIN'
        return is_owner or is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class that allows read access to everyone,
    but write access only to admins.
    """
    
    def has_permission(self, request, view):
        """
        Allow read access to everyone, write access only to admins.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and
            request.user.role == 'ADMIN'
        )
