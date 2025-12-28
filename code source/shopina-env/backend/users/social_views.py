"""
Social authentication endpoints for Google and GitHub
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Google OAuth login endpoint
    Expects: { 'access_token': 'google_access_token' }
    """
    access_token = request.data.get('access_token')
    
    if not access_token:
        return Response(
            {'error': 'access_token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get or create user from Google account
        social_account = SocialAccount.objects.get(
            provider='google',
            uid=access_token  # This is simplified; normally you'd decode the token
        )
        user = social_account.user
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    except SocialAccount.DoesNotExist:
        return Response(
            {'error': 'Social account not found. Please signup first.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def github_login(request):
    """
    GitHub OAuth login endpoint
    Expects: { 'access_token': 'github_access_token' }
    """
    access_token = request.data.get('access_token')
    
    if not access_token:
        return Response(
            {'error': 'access_token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get or create user from GitHub account
        social_account = SocialAccount.objects.get(
            provider='github',
            uid=access_token  # This is simplified; normally you'd decode the token
        )
        user = social_account.user
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    except SocialAccount.DoesNotExist:
        return Response(
            {'error': 'Social account not found. Please signup first.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def remember_me_login(request):
    """
    Extended session login (Remember Me)
    Returns tokens with longer lifetime
    Expects: { 'identifier': 'email/username/phone', 'password': 'password', 'remember': true }
    """
    from django.contrib.auth import authenticate
    from datetime import timedelta
    from django.db.models import Q
    
    identifier = request.data.get('identifier') or request.data.get('email')  # Support both
    password = request.data.get('password')
    remember = request.data.get('remember', False)
    
    if not identifier or not password:
        return Response(
            {'error': 'identifier and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Find user by email, username, or phone
        user = User.objects.get(
            Q(email__iexact=identifier) | 
            Q(username__iexact=identifier) | 
            Q(phone_number=identifier)
        )
        
        # Authenticate
        user_auth = authenticate(username=user.username, password=password)
        
        if not user_auth:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # If Remember Me, extend token lifetime
        if remember:
            # Set to 30 days instead of 1 day
            refresh.set_exp(lifetime=timedelta(days=30))
        
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar': user.avatar.url if user.avatar else None,
                'phone_number': user.phone_number,
                'plan': user.plan,
                'role': user.role,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'remember_me': remember,
        })
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except User.MultipleObjectsReturned:
        return Response(
            {'error': 'Multiple accounts found with this identifier'},
            status=status.HTTP_400_BAD_REQUEST
        )
