"""
Custom authentication backend that supports login with:
- Email
- Username
- Phone number
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailUsernamePhoneAuthBackend(ModelBackend):
    """
    Authenticate using email, username, or phone number with password.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Try to find user by email, username, or phone number
            user = User.objects.get(
                Q(email__iexact=username) | 
                Q(username__iexact=username) | 
                Q(phone_number=username)
            )
            
            # Check password
            if user.check_password(password):
                return user
                
        except User.DoesNotExist:
            # Run default password hasher to reduce timing difference
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # If multiple users found, return None for security
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
