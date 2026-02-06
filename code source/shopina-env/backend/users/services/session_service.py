"""
Session Management Service.
Handles session lifecycle, validation, and persistence.

PATTERNS UTILISÉS:
- Service Layer Pattern: Centraliser la logique de gestion de session
- Repository Pattern: Accès aux données de session
"""

import logging
from django.contrib.sessions.models import Session as DjangoSession
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
import json

User = get_user_model()
logger = logging.getLogger(__name__)


class SessionService:
    """
    🔐 SERVICE: Gérer les sessions utilisateur
    
    FONCTIONNALITÉS:
    ✅ Créer et valider les sessions
    ✅ Gérer les sessions par rôle (vendeur/client)
    ✅ Prévenir l'expiration prématurée
    ✅ Enregistrer l'activité
    """
    
    # Configuration des durées de session par rôle
    SESSION_CONFIG = {
        'customer': {
            'max_age': 14 * 24 * 60 * 60,  # 14 jours
            'remember_me_age': 30 * 24 * 60 * 60,  # 30 jours
        },
        'seller': {
            'max_age': 7 * 24 * 60 * 60,  # 7 jours
            'remember_me_age': 14 * 24 * 60 * 60,  # 14 jours
        },
        'admin': {
            'max_age': 24 * 60 * 60,  # 1 jour
            'remember_me_age': 7 * 24 * 60 * 60,  # 7 jours
        },
    }
    
    def __init__(self):
        """Initialiser le service"""
        self.cache_prefix = 'session:'
    
    def create_session(self, user, role='customer', remember_me=False):
        """
        ✅ Créer une nouvelle session
        
        Args:
            user: Instance User
            role: 'customer', 'seller', ou 'admin'
            remember_me: Prolonger la durée de session
        
        Returns:
            dict: Informations de session
        """
        try:
            session_data = {
                'user_id': user.id,
                'username': user.username,
                'role': role,
                'created_at': timezone.now().isoformat(),
                'last_activity': timezone.now().isoformat(),
                'remember_me': remember_me,
                'session_key': None,  # Sera défini par Django
            }
            
            # Déterminer l'âge de la session
            if remember_me:
                max_age = self.SESSION_CONFIG[role]['remember_me_age']
            else:
                max_age = self.SESSION_CONFIG[role]['max_age']
            
            # Stocker les métadonnées en cache
            session_metadata = {
                **session_data,
                'expires_at': (timezone.now() + timedelta(seconds=max_age)).isoformat(),
            }
            
            cache_key = f"{self.cache_prefix}{user.id}:{role}"
            cache.set(cache_key, session_metadata, max_age)
            
            logger.info(f"Session created for user {user.id} (role: {role})")
            
            return session_metadata
        
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    def validate_session(self, user, role='customer'):
        """
        ✅ Valider une session existante
        
        Returns:
            bool: True si la session est valide
        """
        try:
            cache_key = f"{self.cache_prefix}{user.id}:{role}"
            session_data = cache.get(cache_key)
            
            if not session_data:
                logger.warning(f"Session not found for user {user.id}")
                return False
            
            # Vérifier l'expiration
            expires_at = timezone.datetime.fromisoformat(session_data['expires_at'])
            if timezone.now() > expires_at:
                logger.warning(f"Session expired for user {user.id}")
                cache.delete(cache_key)
                return False
            
            # Mettre à jour l'activité
            session_data['last_activity'] = timezone.now().isoformat()
            cache.set(cache_key, session_data, 
                     int((expires_at - timezone.now()).total_seconds()))
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating session: {e}")
            return False
    
    def extend_session(self, user, role='customer', remember_me=False):
        """
        ⏰ Étendre la durée d'une session
        """
        try:
            cache_key = f"{self.cache_prefix}{user.id}:{role}"
            session_data = cache.get(cache_key)
            
            if not session_data:
                # Créer une nouvelle session si elle n'existe pas
                return self.create_session(user, role, remember_me)
            
            # Calculer la nouvelle expiration
            if remember_me:
                new_max_age = self.SESSION_CONFIG[role]['remember_me_age']
            else:
                new_max_age = self.SESSION_CONFIG[role]['max_age']
            
            new_expires_at = timezone.now() + timedelta(seconds=new_max_age)
            session_data['expires_at'] = new_expires_at.isoformat()
            session_data['last_activity'] = timezone.now().isoformat()
            session_data['remember_me'] = remember_me
            
            cache.set(cache_key, session_data, new_max_age)
            
            logger.info(f"Session extended for user {user.id}")
            return session_data
        
        except Exception as e:
            logger.error(f"Error extending session: {e}")
            raise
    
    def invalidate_session(self, user, role=None):
        """
        ❌ Invalider une session (logout)
        
        Args:
            user: Instance User
            role: Rôle spécifique à invalider, None pour tous
        """
        try:
            if role:
                # Invalider une session spécifique
                cache_key = f"{self.cache_prefix}{user.id}:{role}"
                cache.delete(cache_key)
                logger.info(f"Session invalidated for user {user.id} (role: {role})")
            else:
                # Invalider toutes les sessions de l'utilisateur
                for r in ['customer', 'seller', 'admin']:
                    cache_key = f"{self.cache_prefix}{user.id}:{r}"
                    cache.delete(cache_key)
                logger.info(f"All sessions invalidated for user {user.id}")
        
        except Exception as e:
            logger.error(f"Error invalidating session: {e}")
            raise
    
    def get_session_info(self, user):
        """
        📊 Obtenir les informations de session d'un utilisateur
        """
        try:
            sessions = {}
            for role in ['customer', 'seller', 'admin']:
                cache_key = f"{self.cache_prefix}{user.id}:{role}"
                session_data = cache.get(cache_key)
                if session_data:
                    sessions[role] = session_data
            
            return sessions
        
        except Exception as e:
            logger.error(f"Error getting session info: {e}")
            return {}
    
    def cleanup_expired_sessions(self):
        """
        🧹 Nettoyer les sessions expirées
        (Peut être appelé via une tâche Celery)
        """
        try:
            # Nettoyer les sessions Django expirées
            DjangoSession.objects.filter(
                expire_date__lt=timezone.now()
            ).delete()
            
            logger.info("Expired sessions cleaned up")
        
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
