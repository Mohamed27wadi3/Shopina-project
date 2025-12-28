"""
User service for business logic operations.
"""
from typing import Optional, Dict, Any
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from core.services.base import BaseService
from core.utils.exceptions import (
    BusinessLogicError, 
    DuplicateResourceError,
    ResourceNotFoundError,
    ValidationError
)
from users.repositories.user_repository import UserRepository


User = get_user_model()


class UserService(BaseService[User]):
    """
    Service class for User business logic.
    Handles user registration, profile management, and password reset.
    """
    
    def __init__(self):
        self.repository = UserRepository()
        super().__init__(self.repository)
    
    def register_user(self, username: str, email: str, password: str, 
                     first_name: str = '', last_name: str = '', 
                     role: str = 'CUSTOMER') -> User:
        """
        Register a new user.
        
        Args:
            username: Username
            email: Email address
            password: Password
            first_name: First name (optional)
            last_name: Last name (optional)
            role: User role (default: CUSTOMER)
            
        Returns:
            Created user instance
            
        Raises:
            DuplicateResourceError: If username or email already exists
        """
        # Check if email already exists
        if self.repository.email_exists(email):
            raise DuplicateResourceError("Email already registered")
        
        # Check if username already exists
        if self.repository.username_exists(username):
            raise DuplicateResourceError("Username already taken")
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        
        self.log_operation('user_registered', {'user_id': user.id, 'email': email})
        return user
    
    def update_profile(self, user: User, **kwargs) -> User:
        """
        Update user profile.
        
        Args:
            user: User instance to update
            **kwargs: Fields to update
            
        Returns:
            Updated user instance
        """
        # Fields that can be updated
        allowed_fields = [
            'first_name', 'last_name', 'phone_number', 
            'street_address', 'city', 'postal_code', 'country',
            'shop_name', 'shop_slug', 'avatar'
        ]
        
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if update_data:
            user = self.repository.update(user, **update_data)
            self.log_operation('profile_updated', {'user_id': user.id})
        
        return user
    
    def request_password_reset(self, email: str) -> str:
        """
        Request password reset for user.
        
        Args:
            email: User email
            
        Returns:
            Reset token
            
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = self.repository.get_by_email(email)
        if not user:
            raise ResourceNotFoundError("User with this email not found")
        
        # Generate reset token
        token = user.generate_reset_token()
        
        # Send email (in production, use proper email template)
        self._send_password_reset_email(user, token)
        
        self.log_operation('password_reset_requested', {'user_id': user.id})
        return token
    
    def reset_password(self, token: str, new_password: str) -> User:
        """
        Reset user password using token.
        
        Args:
            token: Reset token
            new_password: New password
            
        Returns:
            User instance
            
        Raises:
            ValidationError: If token is invalid or expired
        """
        user = self.repository.get_by_reset_token(token)
        if not user:
            raise ValidationError("Invalid reset token")
        
        if not user.is_reset_token_valid(token):
            raise ValidationError("Reset token has expired")
        
        # Set new password
        user.set_password(new_password)
        user.clear_reset_token()
        
        self.log_operation('password_reset', {'user_id': user.id})
        return user

    def change_password(self, user: User, old_password: str, new_password: str) -> User:
        """
        Change a user's password while authenticated.

        Ensures the current password matches, the new password passes Django's
        password validators, and performs the operation atomically.

        Raises:
            ValidationError: If the old password is incorrect or the new password
                             fails validation or is the same as the old password.
        """
        # Verify current password using Django's secure check (constant-time)
        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect")

        # Prevent reusing the same password
        if user.check_password(new_password):
            raise ValidationError("New password must be different from the old password")

        # Validate the new password using Django validators
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError as DjangoValidationError
        from django.db import transaction

        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as e:
            # Normalize Django ValidationError to service ValidationError
            raise ValidationError(" ".join([str(x) for x in e.messages]))

        # Perform password set inside a transaction to ensure atomicity
        with transaction.atomic():
            user.set_password(new_password)
            # Record the time of password change
            from django.utils import timezone
            user.last_password_change = timezone.now()
            user.save()

        self.log_operation('password_changed', {'user_id': user.id})
        return user
    
    def change_role(self, user: User, new_role: str) -> User:
        """
        Change user role (admin only operation).
        
        Args:
            user: User instance
            new_role: New role (ADMIN, SELLER, CUSTOMER)
            
        Returns:
            Updated user instance
            
        Raises:
            ValidationError: If role is invalid
        """
        valid_roles = ['ADMIN', 'SELLER', 'CUSTOMER']
        if new_role not in valid_roles:
            raise ValidationError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        user = self.repository.update(user, role=new_role)
        self.log_operation('role_changed', {'user_id': user.id, 'new_role': new_role})
        return user

    def start_two_factor(self, user: User, ttl_minutes: int = 10) -> str | None:
        """
        Start an email-based OTP flow for the given user.

        Returns the plaintext OTP only when settings.DEBUG is True (useful for tests).
        Otherwise returns None.
        """
        import secrets
        from django.utils import timezone
        from datetime import timedelta
        from django.contrib.auth.hashers import make_password
        from django.conf import settings

        # Create 6-digit numeric OTP
        otp = f"{secrets.randbelow(10**6):06d}"
        expires_at = timezone.now() + timedelta(minutes=ttl_minutes)
        otp_hash = make_password(otp)

        # Save the OTP record
        from users.models import TwoFactor
        TwoFactor.objects.create(
            user=user,
            otp_hash=otp_hash,
            expires_at=expires_at
        )

        # Send email (in production use an email template)
        subject = "Your Shopina verification code"
        message = f"Your verification code is {otp}. It expires in {ttl_minutes} minutes."
        if settings.DEBUG or getattr(settings, 'TESTING', False):
            # In debug/test mode we print the OTP and return it for tests
            print(f"[DEBUG] OTP for {user.email}: {otp}")
            return otp
        else:
            try:
                from django.core.mail import send_mail
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            except Exception as e:
                # Do not reveal internal errors to caller
                raise ValidationError("Failed to send OTP email")
            return None

    def verify_two_factor(self, user: User, otp: str) -> bool:
        """
        Verify the provided OTP for the user. Raises ValidationError on failure.
        Uses constant-time hash checking and transaction for atomic update.
        """
        from django.utils import timezone
        from django.db import transaction
        from django.contrib.auth.hashers import check_password
        from users.models import TwoFactor

        # Get the most recent unverified OTP for this user
        tf = TwoFactor.objects.filter(user=user, verified=False, expires_at__gt=timezone.now()).order_by('-created_at').first()
        if not tf:
            raise ValidationError("No active verification code found. Please request a new code.")

        # Prevent too many attempts
        if tf.attempts >= 5:
            raise ValidationError("Too many verification attempts. Request a new code.")

        # Check OTP (constant-time)
        if not check_password(otp, tf.otp_hash):
            tf.attempts += 1
            tf.save(update_fields=['attempts'])
            raise ValidationError("Invalid verification code")

        # Mark verified atomically
        with transaction.atomic():
            tf.verified = True
            tf.attempts += 1
            tf.save(update_fields=['verified', 'attempts'])
            # Optional: record last 2fa time on user
            from django.utils import timezone
            user.last_password_change = getattr(user, 'last_password_change', None)
        return True    
    def get_user_statistics(self) -> Dict[str, Any]:
        """
        Get user statistics for admin dashboard.
        
        Returns:
            Dictionary with user statistics
        """
        return self.repository.get_user_statistics()
    
    def _send_password_reset_email(self, user: User, token: str):
        """
        Send password reset email to user.
        
        Args:
            user: User instance
            token: Reset token
        """
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        
        subject = "Password Reset Request"
        message = f"""
        Hello {user.username},
        
        You requested a password reset. Click the link below to reset your password:
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Shopina Team
        """
        
        # In development, just print the token
        if settings.DEBUG:
            print(f"Password reset token for {user.email}: {token}")
            print(f"Reset URL: {reset_url}")
        else:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
