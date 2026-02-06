"""
Session Management Views and APIs.
Handles session lifecycle from login to logout.

PATTERNS UTILISÉS:
- Facade Pattern: Interface simple pour gestion de session
- Factory Pattern: Créer les sessions selon le rôle
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from users.services.session_service import SessionService
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class SessionSerializer:
    """Simple serializer for session data"""
    
    @staticmethod
    def serialize(session_data):
        """Sérialiser les données de session"""
        return {
            'user_id': session_data.get('user_id'),
            'username': session_data.get('username'),
            'role': session_data.get('role'),
            'created_at': session_data.get('created_at'),
            'last_activity': session_data.get('last_activity'),
            'expires_at': session_data.get('expires_at'),
            'remember_me': session_data.get('remember_me', False),
        }


class LoginWithSessionView(APIView):
    """
    🔐 LOGIN VIEW: Créer une session après authentification
    
    POST /api/auth/login-with-session/
    {
        "email": "user@example.com",
        "password": "password123",
        "remember_me": false  # Optionnel
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_service = SessionService()
    
    def post(self, request):
        """
        Authentifier l'utilisateur et créer une session
        """
        try:
            from users.serializers import EmailOrUsernameTokenObtainSerializer
            
            # Authentifier l'utilisateur (logique standard JWT)
            serializer = EmailOrUsernameTokenObtainSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            user = serializer.user
            remember_me = request.data.get('remember_me', False)
            
            # ✅ Créer une session personne
            role = self._determine_user_role(user)
            session_data = self.session_service.create_session(
                user=user,
                role=role,
                remember_me=remember_me
            )
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            
            # ✅ Sauvegarder dans la session Django
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['user_role'] = role
            request.session['remember_me'] = remember_me
            request.session.modified = True
            
            logger.info(f"User {user.username} logged in with session (role: {role})")
            
            return Response({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': role,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'session': SessionSerializer.serialize(session_data),
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error logging in: {e}")
            return Response(
                {'error': 'Login failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @staticmethod
    def _determine_user_role(user):
        """🎯 Déterminer le rôle de l'utilisateur"""
        if user.is_superuser or user.is_staff:
            return 'admin'
        if hasattr(user, 'seller_profile') and user.seller_profile:
            return 'seller'
        return 'customer'


class LogoutWithSessionView(APIView):
    """
    ❌ LOGOUT VIEW: Invalider la session en toute sécurité
    
    POST /api/auth/logout-with-session/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_service = SessionService()
    
    def post(self, request):
        """
        Déconnecter l'utilisateur et invalider la session
        """
        try:
            user = request.user
            role = request.session.get('user_role', 'customer')
            
            # ✅ Invalider la session
            self.session_service.invalidate_session(user, role)
            
            # ✅ Nettoyer la session Django
            request.session.flush()
            
            logger.info(f"User {user.username} logged out")
            
            return Response({
                'success': True,
                'message': 'Logout successful',
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error logging out: {e}")
            return Response(
                {'error': 'Logout failed'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ExtendSessionView(APIView):
    """
    ⏰ EXTEND SESSION VIEW: Prolonger la durée de session
    
    POST /api/auth/extend-session/
    {
        "remember_me": false  # Optionnel
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_service = SessionService()
    
    def post(self, request):
        """
        Prolonger la durée de la session
        """
        try:
            user = request.user
            role = request.session.get('user_role', 'customer')
            remember_me = request.data.get('remember_me', False)
            
            # ✅ Étendre la session
            session_data = self.session_service.extend_session(
                user=user,
                role=role,
                remember_me=remember_me
            )
            
            # ✅ Mettre à jour la session Django
            request.session['last_activity'] = timezone.now().isoformat()
            request.session['remember_me'] = remember_me
            request.session.modified = True
            
            logger.info(f"Session extended for user {user.username}")
            
            return Response({
                'success': True,
                'message': 'Session extended',
                'session': SessionSerializer.serialize(session_data),
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error extending session: {e}")
            return Response(
                {'error': 'Failed to extend session'},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetSessionInfoView(APIView):
    """
    📊 GET SESSION INFO VIEW: Récupérer les informations de session
    
    GET /api/auth/session-info/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_service = SessionService()
    
    def get(self, request):
        """
        Obtenir les informations de session actuelles
        """
        try:
            user = request.user
            sessions = self.session_service.get_session_info(user)
            
            return Response({
                'success': True,
                'user_id': user.id,
                'username': user.username,
                'current_role': request.session.get('user_role', 'customer'),
                'sessions': {
                    role: SessionSerializer.serialize(data)
                    for role, data in sessions.items()
                },
                'request_session': {
                    'last_activity': request.session.get('last_activity'),
                    'created_at': request.session.get('session_start'),
                },
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error getting session info: {e}")
            return Response(
                {'error': 'Failed to get session info'},
                status=status.HTTP_400_BAD_REQUEST
            )


def csrf_failure(request, reason=""):
    """
    🛡️ CSRF FAILURE HANDLER: Custom CSRF failure response
    """
    logger.warning(f"CSRF failure: {reason}")
    return JsonResponse({
        'error': 'CSRF validation failed',
        'reason': reason,
    }, status=status.HTTP_403_FORBIDDEN)
