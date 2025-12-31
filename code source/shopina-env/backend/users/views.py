from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Count, DecimalField, Q, Sum, Value
from django.db.models.functions import Coalesce
from core.permissions.custom_permissions import IsAdmin, IsOwnerOrAdmin, IsSeller
from core.utils.exceptions import ValidationError as CustomValidationError
from users.services.user_service import UserService
from .serializers import (
    UserSerializer, 
    UserDetailSerializer,
    UserUpdateSerializer,
    CustomerListSerializer,
    RegisterSerializer, 
    EmailOrUsernameTokenObtainSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    TwoFactorStartSerializer,
    TwoFactorVerifySerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    Creates a new user and returns JWT tokens.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    def create(self, request, *args, **kwargs):
        """Create user and return tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update current user profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    def get_serializer_class(self):
        """Return appropriate serializer based on request method."""
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserUpdateSerializer

    def get_object(self):
        """Return current user."""
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """Update user profile using service layer."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Use service layer for update
        updated_user = self.user_service.update_profile(
            instance, 
            **serializer.validated_data
        )
        
        return Response(UserDetailSerializer(updated_user).data)


class PasswordResetRequestView(APIView):
    """
    Request password reset.
    Sends reset token to user's email.
    """
    permission_classes = [permissions.AllowAny]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
    
    def post(self, request):
        """Request password reset."""
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.user_service.request_password_reset(
                serializer.validated_data['email']
            )
            return Response({
                'message': 'Password reset email sent. Please check your inbox.'
            }, status=status.HTTP_200_OK)
        except CustomValidationError as e:
            # Don't reveal if email exists or not (security)
            return Response({
                'message': 'If this email exists, a reset link has been sent.'
            }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with token.
    """
    permission_classes = [permissions.AllowAny]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
    
    def post(self, request):
        """Reset password with token."""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.user_service.reset_password(
                serializer.validated_data['token'],
                serializer.validated_data['new_password']
            )
            return Response({
                'message': 'Password has been reset successfully.'
            }, status=status.HTTP_200_OK)
        except CustomValidationError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class TwoFactorStartView(APIView):
    """Start a two-factor flow by sending an OTP to the user's email."""
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    def post(self, request):
        serializer = TwoFactorStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            otp_debug = self.user_service.start_two_factor(user)
            # For security we don't return otp normally, but tests may rely on debug/test behavior
            resp = {'message': 'OTP sent to your email.'}
            from django.conf import settings
            # Allow returning the OTP in DEBUG or TESTING modes to make tests deterministic
            if (getattr(settings, 'DEBUG', False) or getattr(settings, 'TESTING', False)) and otp_debug:
                resp['debug_otp'] = otp_debug
            return Response(resp, status=status.HTTP_200_OK)
        except CustomValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TwoFactorVerifyView(APIView):
    """Verify an OTP and mark the session as 2FA-verified."""
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    def post(self, request):
        serializer = TwoFactorVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        otp = serializer.validated_data['otp']
        try:
            self.user_service.verify_two_factor(user, otp)
            # mark session as verified for this user id
            key = f'2fa_verified_{user.id}'
            request.session[key] = True
            # Keep short-lived verification (e.g., 5 minutes)
            request.session.set_expiry(5 * 60)

            # Optionally enable 2FA on the user's account if requested
            if serializer.validated_data.get('enable'):
                user.two_factor_enabled = True
                user.save()

            return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
        except CustomValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Change password for authenticated user.
    Uses the UserService to encapsulate validation and transaction handling.
    Requires 2FA verification when the user has it enabled.
    """
    permission_classes = [permissions.IsAuthenticated,]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
    
    def post(self, request):
        """Change user password."""
        # Enforce 2FA for sensitive operations
        from core.permissions.twofactor import Is2FAVerified
        perm = Is2FAVerified()
        if not perm.has_permission(request, self):
            return Response({'error': 'Two-factor authentication required.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        try:
            updated_user = self.user_service.change_password(user, old_password, new_password)
            return Response({
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        except CustomValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Prevent leaking internal error details
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(generics.ListAPIView):
    """
    List all users (admin only).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete a specific user (admin only).
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdmin]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()


class UserStatisticsView(APIView):
    """
    Get user statistics for admin dashboard.
    """
    permission_classes = [IsAdmin]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
    
    def get(self, request):
        """Get user statistics."""
        stats = self.user_service.get_user_statistics()
        return Response(stats, status=status.HTTP_200_OK)


class CustomerListView(generics.ListAPIView):
    """Expose customer data with aggregated order stats for the dashboard."""

    serializer_class = CustomerListSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def get_queryset(self):
        queryset = User.objects.filter(role='CUSTOMER')
        search = (self.request.query_params.get('search') or '').strip()
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        return (
            queryset
            .annotate(
                total_orders=Count('orders', distinct=True),
                total_spent=Coalesce(
                    Sum('orders__total'),
                    Value(0, output_field=DecimalField(max_digits=12, decimal_places=2))
                ),
            )
            .order_by('-date_joined')
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view that allows email, username, or phone number login.
    """
    serializer_class = EmailOrUsernameTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        """Issue JWT tokens and also create a Django session for template views."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create Django session so HTML views (admin/Django templates) recognize the user
        try:
            from django.contrib.auth import login
            # DRF wraps the HttpRequest; use underlying request for session operations
            http_request = getattr(request, '_request', request)
            user = getattr(serializer, 'user', None)
            if user is not None:
                login(http_request, user)
        except Exception:
            # Do not break JWT issuance if session creation fails
            pass

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
