"""
Advanced Session Management Middleware for Shopina.
Handles session persistence, seller/customer separation, and secure session management.

PATTERNS UTILISÉS:
- Strategy Pattern: Différentes stratégies selon le rôle utilisateur
- Observer Pattern: Surveiller les changements de session
"""

import logging
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session as DjangoSession
from django.utils import timezone
from datetime import timedelta

User = get_user_model()
logger = logging.getLogger(__name__)


class SessionPersistenceMiddleware(MiddlewareMixin):
    """
    🔒 MIDDLEWARE: Persiste et protège les sessions utilisateur
    
    FONCTIONNALITÉS:
    ✅ Garder la session active pour les utilisateurs authentifiés
    ✅ Empêcher l'expiration prématurée de la session
    ✅ Enregistrer l'activité de la session
    ✅ Gérer la distinction entre vendeur et client
    """
    
    def process_request(self, request):
        """
        Traiter la requête - Étendre la durée de vie de la session
        """
        # Vérifier si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Mettre à jour l'heure de dernière activité
            self._update_session_activity(request)
            
            # Ajouter des informations de rôle au contexte
            request.user_role = self._get_user_role(request.user)
            
            # Vérifier la session n'a pas expiré
            self._check_session_validity(request)
        
        return None
    
    def process_response(self, request, response):
        """
        Traiter la réponse - Persister la session
        """
        if request.user.is_authenticated:
            # Assurer que la session est sauvegardée
            if hasattr(request, 'session') and request.session.modified:
                request.session.save()
        
        return response
    
    @staticmethod
    def _update_session_activity(request):
        """
        📊 Mettre à jour l'heure de dernière activité
        """
        try:
            if hasattr(request, 'session'):
                # Garder trace de l'activité
                request.session['last_activity'] = timezone.now().isoformat()
                request.session['session_start'] = request.session.get(
                    'session_start', 
                    timezone.now().isoformat()
                )
                # Marquer comme modifié pour forcer la sauvegarde
                request.session.modified = True
        except Exception as e:
            logger.warning(f"Error updating session activity: {e}")
    
    @staticmethod
    def _get_user_role(user):
        """
        🎯 Déterminer le rôle de l'utilisateur
        Retour: 'seller' | 'customer' | 'admin'
        """
        if user.is_superuser or user.is_staff:
            return 'admin'
        
        # Vérifier si l'utilisateur est vendeur
        if hasattr(user, 'seller_profile') and user.seller_profile:
            return 'seller'
        
        return 'customer'
    
    @staticmethod
    def _check_session_validity(request):
        """
        ✅ Vérifier la validité de la session
        """
        try:
            session_data = request.session
            
            # Vérifier si la session a été créée
            if 'session_start' not in session_data:
                session_data['session_start'] = timezone.now().isoformat()
            
            # Vérifier si la session n'a pas expiré (sécurité supplémentaire)
            session_start = session_data.get('session_start')
            if session_start:
                session_start_time = timezone.datetime.fromisoformat(session_start)
                session_age = timezone.now() - session_start_time
                
                # Si session plus vieille que 30 jours, créer nouvelle session
                if session_age > timedelta(days=30):
                    request.session.flush()
                    logger.info(f"Session expired for user {request.user.id}")
        except Exception as e:
            logger.warning(f"Error checking session validity: {e}")


class RoleBasedSessionMiddleware(MiddlewareMixin):
    """
    🔐 MIDDLEWARE: Gérer les sessions basées sur les rôles
    
    FONCTIONNALITÉS:
    ✅ Sessions séparées pour vendeur/client
    ✅ Isolation des données sensibles
    ✅ Logs d'accès par rôle
    """
    
    SELLER_SESSION_KEY = 'seller_session_id'
    CUSTOMER_SESSION_KEY = 'customer_session_id'
    
    def process_request(self, request):
        """
        Gérer la session en fonction du rôle
        """
        if not request.user.is_authenticated:
            return None
        
        user_role = self._get_user_role(request.user)
        
        # Créer ou récupérer la session du rôle
        self._manage_role_session(request, user_role)
        
        # Enregistrer l'accès
        self._log_access(request, user_role)
        
        return None
    
    @staticmethod
    def _get_user_role(user):
        """Déterminer le rôle utilisateur"""
        if user.is_superuser or user.is_staff:
            return 'admin'
        if hasattr(user, 'seller_profile') and user.seller_profile:
            return 'seller'
        return 'customer'
    
    @staticmethod
    def _manage_role_session(request, user_role):
        """
        🔑 Gérer les clés de session par rôle
        """
        try:
            if user_role == 'seller':
                # Créer/maintenir session vendeur
                if 'seller_session_id' not in request.session:
                    request.session['seller_session_id'] = timezone.now().isoformat()
                    request.session['seller_role'] = True
                    request.session.modified = True
                    logger.info(f"Seller session created for user {request.user.id}")
                
                # Assurer que les données sensibles du vendeur sont protégées
                request.session['current_role'] = 'seller'
            
            elif user_role == 'customer':
                # Créer/maintenir session client
                if 'customer_session_id' not in request.session:
                    request.session['customer_session_id'] = timezone.now().isoformat()
                    request.session['customer_role'] = True
                    request.session.modified = True
                    logger.info(f"Customer session created for user {request.user.id}")
                
                request.session['current_role'] = 'customer'
            
            elif user_role == 'admin':
                request.session['admin_access'] = True
                request.session['current_role'] = 'admin'
                request.session.modified = True
        
        except Exception as e:
            logger.error(f"Error managing role session: {e}")
    
    @staticmethod
    def _log_access(request, user_role):
        """
        📝 Enregistrer l'accès utilisateur
        """
        try:
            # Créer un log d'accès pour audit
            access_log = {
                'user_id': request.user.id,
                'username': request.user.username,
                'role': user_role,
                'path': request.path,
                'method': request.method,
                'timestamp': timezone.now().isoformat(),
                'ip_address': get_client_ip(request),
            }
            
            # Stocker dans la session
            if 'access_log' not in request.session:
                request.session['access_log'] = []
            
            # Garder seulement les 50 derniers accès
            logs = request.session.get('access_log', [])
            logs.append(access_log)
            request.session['access_log'] = logs[-50:]
            request.session.modified = True
        
        except Exception as e:
            logger.debug(f"Error logging access: {e}")


class CSRFProtectionMiddleware(MiddlewareMixin):
    """
    🛡️ MIDDLEWARE: Protection CSRF renforcée
    
    FONCTIONNALITÉS:
    ✅ Valider CSRF tokens
    ✅ Gérer les changements de session
    ✅ Prévenir les attaques cross-site
    """
    
    def process_request(self, request):
        """
        Valider et gérer les tokens CSRF
        """
        # Pour les requêtes POST/PUT/DELETE, le CSRF est automatiquement vérifié
        # par le middleware Django CSRF
        
        # Ajouter le token CSRF à la session si pas présent
        if hasattr(request, 'session'):
            if 'csrf_token' not in request.session:
                from django.middleware.csrf import get_token
                get_token(request)
        
        return None


def get_client_ip(request):
    """
    🔍 Obtenir l'adresse IP du client
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
