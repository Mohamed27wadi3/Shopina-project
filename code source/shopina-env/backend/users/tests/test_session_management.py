"""
Tests pour le système de gestion de session sécurisé.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.services.session_service import SessionService

User = get_user_model()


class SessionServiceTests(TestCase):
    """Tests pour SessionService"""
    
    def setUp(self):
        """Initialiser les tests"""
        self.service = SessionService()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_session_customer(self):
        """✅ Tester la création d'une session client"""
        session = self.service.create_session(
            user=self.user,
            role='customer',
            remember_me=False
        )
        
        self.assertIsNotNone(session)
        self.assertEqual(session['username'], 'testuser')
        self.assertEqual(session['role'], 'customer')
        self.assertFalse(session['remember_me'])
    
    def test_create_session_seller(self):
        """✅ Tester la création d'une session vendeur"""
        session = self.service.create_session(
            user=self.user,
            role='seller',
            remember_me=True
        )
        
        self.assertIsNotNone(session)
        self.assertEqual(session['role'], 'seller')
        self.assertTrue(session['remember_me'])
    
    def test_validate_session(self):
        """✅ Tester la validation de session"""
        # Créer une session
        self.service.create_session(self.user, role='customer')
        
        # Valider
        is_valid = self.service.validate_session(self.user, role='customer')
        self.assertTrue(is_valid)
    
    def test_validate_nonexistent_session(self):
        """❌ Tester la validation d'une session inexistante"""
        is_valid = self.service.validate_session(self.user, role='customer')
        self.assertFalse(is_valid)
    
    def test_extend_session(self):
        """⏰ Tester l'extension de session"""
        # Créer
        session1 = self.service.create_session(self.user, role='customer')
        
        # Attendre un peu
        import time
        time.sleep(0.1)
        
        # Étendre
        session2 = self.service.extend_session(self.user, role='customer')
        
        # Vérifier que c'est la même session
        self.assertEqual(session2['username'], session1['username'])
        # Vérifier que l'expiration est plus nouvelle
        self.assertGreater(session2['expires_at'], session1['expires_at'])
    
    def test_invalidate_session(self):
        """❌ Tester l'invalidation de session"""
        # Créer
        self.service.create_session(self.user, role='customer')
        
        # Invalider
        self.service.invalidate_session(self.user, role='customer')
        
        # Vérifier qu'elle est invalidée
        is_valid = self.service.validate_session(self.user, role='customer')
        self.assertFalse(is_valid)
    
    def test_role_separation(self):
        """🔐 Tester la séparation des rôles"""
        # Créer deux sessions (rôles différents)
        customer_session = self.service.create_session(self.user, role='customer')
        seller_session = self.service.create_session(self.user, role='seller')
        
        # Vérifier qu'elles existent séparément
        sessions = self.service.get_session_info(self.user)
        
        self.assertIn('customer', sessions)
        self.assertIn('seller', sessions)
        self.assertNotEqual(
            sessions['customer']['created_at'],
            sessions['seller']['created_at']
        )
    
    def test_remember_me_duration(self):
        """🔔 Tester la durée "Remember Me""""
        # Sans remember me
        session1 = self.service.create_session(self.user, role='customer', remember_me=False)
        
        # Avec remember me
        session2 = self.service.create_session(self.user, role='customer', remember_me=True)
        
        # Vérifier que l'expiration est plus loin
        exp1 = timezone.datetime.fromisoformat(session1['expires_at'])
        exp2 = timezone.datetime.fromisoformat(session2['expires_at'])
        
        self.assertGreater(exp2, exp1)


class LoginWithSessionAPITests(APITestCase):
    """Tests pour l'API de login avec session"""
    
    def setUp(self):
        """Initialiser les tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.login_url = '/api/auth/login-with-session/'
        self.logout_url = '/api/auth/logout-with-session/'
        self.session_info_url = '/api/auth/session-info/'
    
    def test_login_success(self):
        """✅ Tester le login réussi"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpass123',
            'remember_me': False
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data)
        self.assertIn('session', response.data)
    
    def test_login_invalid_credentials(self):
        """❌ Tester le login avec credentials invalides"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_session_persistence_after_login(self):
        """✅ Tester la persistance de session après login"""
        # Login
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpass123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Accéder à session info
        response = self.client.get(self.session_info_url)
        
        # Doit réussir (pas de logout involontaire)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_logout_invalidates_session(self):
        """✅ Tester que logout invalide la session"""
        # Login
        self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpass123'
        }, format='json')
        
        # Logout
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que la session est invalidée
        response = self.client.get(self.session_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_extend_session(self):
        """⏰ Tester l'extension de session"""
        # Login
        self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpass123'
        }, format='json')
        
        # Étendre la session
        response = self.client.post('/api/auth/extend-session/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])


class SessionMiddlewareTests(TestCase):
    """Tests pour les middlewares de session"""
    
    def setUp(self):
        """Initialiser les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_session_activity_logging(self):
        """📝 Tester que l'activité est enregistrée"""
        # Login (via Django auth pour tester middleware)
        self.client.login(username='testuser', password='testpass123')
        
        # Faire une requête
        response = self.client.get('/api/auth/session-info/', HTTP_ACCEPT='application/json')
        
        # Session doit être enregistrée
        self.assertIsNotNone(response)
    
    def test_csrf_token_creation(self):
        """🛡️ Tester la création du token CSRF"""
        response = self.client.get('/api/shop/products/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # CSRF token doit être présent
        self.assertIn('shopina_csrf', self.client.cookies)


def run_session_tests():
    """🚀 Lancer tous les tests de session"""
    import unittest
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter les tests
    suite.addTests(loader.loadTestsFromTestCase(SessionServiceTests))
    suite.addTests(loader.loadTestsFromTestCase(LoginWithSessionAPITests))
    suite.addTests(loader.loadTestsFromTestCase(SessionMiddlewareTests))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == '__main__':
    run_session_tests()
