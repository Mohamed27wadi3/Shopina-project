# 🔐 SYSTÈME DE GESTION DE SESSION SÉCURISÉ - SHOPINA

## 📋 RÉSUMÉ DES CHANGEMENTS

Ce document décrit la restructuration complète du système d'authentification et de gestion de session de Shopina pour :
- ✅ **Empêcher le logout involontaire** à la navigation
- ✅ **Séparer les sessions** vendeur/client
- ✅ **Sécuriser les cookies** (CSRF + HttpOnly)
- ✅ **Maintenir la session active** entre les pages

---

## 🏗️ ARCHITECTURE

### Niveaux de sécurité:

```
Frontend (React)
    ↓
    ├─ Stocke: JWT tokens en localStorage
    ├─ Ajoute: CSRF token à chaque requête POST
    └─ Appel API: POST /api/auth/login-with-session/
                ↓
Middleware Django
    ├─ SessionPersistenceMiddleware (étend la durée de vie)
    ├─ RoleBasedSessionMiddleware (gère rôles: vendeur/client)
    └─ CSRFProtectionMiddleware (valide tokens)
                ↓
Backend (Django)
    ├─ SessionService (gère le cycle de vie)
    ├─ Settings (CONFIG_SESSION_*)
    └─ Views (login/logout/extend avec session)
                ↓
Database + Cache
    ├─ Sessions Django (db)
    └─ Session metadata (cache en mémoire)
```

---

## 📁 FICHIERS MODIFIÉS / CRÉÉS

### 1️⃣ **Middleware** - `core/middleware/session_middleware.py`
**Créé** - Nouvelles middlewares:

- `SessionPersistenceMiddleware`: Maintient la session active
- `RoleBasedSessionMiddleware`: Gère vendeur/client séparé
- `CSRFProtectionMiddleware`: Protège contre les attaques CSRF

```python
# Usage automatique via settings.MIDDLEWARE
```

### 2️⃣ **Service de Session** - `users/services/session_service.py`
**Créé** - Gère complètement le cycle de vie de la session:

```python
session_service = SessionService()

# Créer une session
session_service.create_session(user, role='customer', remember_me=False)

# Valider une session
session_service.validate_session(user, role='customer')

# Étendre une session
session_service.extend_session(user, role='customer', remember_me=True)

# Invalider/Logout
session_service.invalidate_session(user, role='customer')
```

### 3️⃣ **Views API** - `users/session_views.py`
**Créé** - Nouveaux endpoints:

- `POST /api/auth/login-with-session/` - Login avec session
- `POST /api/auth/logout-with-session/` - Logout sécurisé
- `POST /api/auth/extend-session/` - Prolonger la session
- `GET /api/auth/session-info/` - Info session actuelle

### 4️⃣ **URLs** - `users/urls.py`
**Modifié** - Ajout des routes de session

### 5️⃣ **Settings** - `shopina/settings.py`
**Modifié** - Configuration sécurisée:

```python
# ✅ Session persistante
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ✅ Role-based durations
SESSION_CUSTOMER_MAX_AGE = 14 jours
SESSION_SELLER_MAX_AGE = 7 jours
SESSION_ADMIN_MAX_AGE = 1 jour

# ✅ Secure cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ✅ CSRF
CSRF_USE_SESSIONS = True
CSRF_COOKIE_AGE = 1 year
```

---

## 🔑 CONCEPTS CLÉS

### Middleware Chain

```
Request arrive
    ↓
SessionPersistenceMiddleware
  ├─ Étendre la durée si actif
  ├─ Enregistrer l'activité
  └─ Vérifier expiration
    ↓
RoleBasedSessionMiddleware
  ├─ Détecter le rôle (vendeur/client/admin)
  ├─ Maintenir session séparée par rôle
  └─ Logger l'accès
    ↓
CSRFProtectionMiddleware
  ├─ Valider tokens CSRF
  ├─ Générer nouveaux tokens si besoin
    ↓
Handler / View
    ↓
Response retour
```

### Role-based Sessions

```python
# Une session séparée par rôle
Customer Session:
  - max_age: 14 jours
  - Vendeur: Non
  - Data: Panier, Commandes, Avis

Seller Session:
  - max_age: 7 jours (stricter)
  - Vendeur: Oui
  - Data: Magasin, Produits, Ventes, Analytics

Admin Session:
  - max_age: 1 jour (très strict)
  - Vendeur: N/A
  - Data: Accès full admin
```

### Remember Me Pattern

```python
# Sans "Remember Me"
login() → session max_age = 14 jours

# Avec "Remember Me"
login(remember_me=True) → session max_age = 30 jours
```

---

## 🚀 UTILISATION

### Frontend (React)

```typescript
// 1. Login avec session (NOUVEAU)
const response = await fetch('/api/auth/login-with-session/', {
  method: 'POST',
  credentials: 'include',  // ✅ Inclure cookies
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('shopina_csrf'),  // ✅ CSRF token
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123',
    remember_me: true,
  }),
});

// Stocker tokens
localStorage.setItem('access_token', response.tokens.access);
localStorage.setItem('refresh_token', response.tokens.refresh);

// 2. Utiliser l'API normalement (session automat.)
const products = await fetch('/api/shop/products/', {
  credentials: 'include',  // ✅ Envoyer cookies
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'X-CSRFToken': getCookie('shopina_csrf'),
  },
});

// 3. Logout sécurisé
const logout = await fetch('/api/auth/logout-with-session/', {
  method: 'POST',
  credentials: 'include',
  headers: {
    'X-CSRFToken': getCookie('shopina_csrf'),
  },
});
```

### Backend (Django)

```python
# Service layer
from users.services.session_service import SessionService

session_service = SessionService()

# Après login
session_data = session_service.create_session(
    user=user,
    role='customer',  # ou 'seller', 'admin'
    remember_me=request.data.get('remember_me', False)
)

# Avant logout
session_service.invalidate_session(user, role='customer')

# Pour prolonger manuellement (après requête importante)
session_service.extend_session(user, role='customer')
```

---

## 🔒 SÉCURITÉ

### 1. Session Persistence (Prévient logout involontaire)

✅ **Avant**:
```
User navigue → Nouvelle session → Logout involontaire
```

✅ **Après**:
```
User navigue → SessionPersistenceMiddleware étend → Logout évité
```

### 2. Role-based Separation

✅ Vendeur et client ont des sessions séparées
✅ Données du vendeur protégées (7 jours max vs 14 client)
✅ Admin session la plus courte (1 jour max)

### 3. CSRF Protection

✅ `CSRF_USE_SESSIONS = True` - Token en session
✅ `CSRF_COOKIE_HTTPONLY = False` - Lisible en JS (nécessaire)
✅ `CSRF_COOKIE_SAMESITE = 'Lax'` - Protège contre attaques

### 4. Secure Cookies

✅ `SESSION_COOKIE_HTTPONLY = True` - Pas d'accès JS (XSS protection)
✅ `SESSION_COOKIE_SAMESITE = 'Lax'` - CSRF protection
✅ `SESSION_COOKIE_SECURE = False` (→ True en production avec HTTPS)

---

## 📊 FLUX D'AUTHENTIFICATION COMPLET

### Login Flow

```
1. User soumet login form
   POST /api/auth/login-with-session/
   {
     "email": "user@example.com",
     "password": "password123",
     "remember_me": false
   }

2. Backend authentifie
   ✅ Valide credentials
   ✅ Détermine le rôle (customer/seller/admin)

3. SessionService crée session
   ✅ Crée session metadata
   ✅ Stocke dans cache (+ expiryDate)

4. Retour au frontend
   {
     "tokens": {
       "access": "...",
       "refresh": "..."
     },
     "session": {
       "user_id": 1,
       "role": "customer",
       "expires_at": "2025-02-19T...",
       ...
     }
   }

5. Frontend stocke
   localStorage: access + refresh tokens
   Cookies: Session cookie (HTTP only)

6. Chaque requête
   ✅ SessionPersistenceMiddleware étend la session
   ✅ Demande réussit
```

### Logout Flow

```
1. User click logout
   POST /api/auth/logout-with-session/
   Headers: X-CSRFToken, Authorization

2. Backend invalide session
   ✅ SessionService.invalidate_session()
   ✅ Nettoie session Django
   ✅ Supprime du cache

3. Frontend cleanup
   localStorage.clear()
   Cookies auto-supprimés (expirés)

4. Redirection
   → Page login
```

---

## 🧪 TESTS

### Tester la persistance de session

```bash
# Terminal 1: Lancer le serveur
python manage.py runserver

# Terminal 2: Tester login
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "remember_me": false
  }' \
  -c cookies.txt

# Tester accès avec session
curl http://localhost:8000/api/auth/session-info/ \
  -b cookies.txt

# Tester logout
curl -X POST http://localhost:8000/api/auth/logout-with-session/ \
  -b cookies.txt

# Vérifier session invalidée
curl http://localhost:8000/api/auth/session-info/ \
  -b cookies.txt
# → Erreur 401 Unauthorized
```

### Vérifier la séparation vendeur/client

```python
# Dans les logs
# User 1 (customer):
# INFO: Session created for user 1 (role: customer)

# User 2 (seller):
# INFO: Session created for user 2 (role: seller)

# Leurs sessions sont séparées
# Durées différentes: customer 14j vs seller 7j
```

---

## 📝 LOGS

Les logs sont enregistrés à:
```
logs/session.log
```

Exemples:

```
INFO 2025-02-04 10:30:45 - Session created for user 1 (role: customer)
INFO 2025-02-04 10:31:12 - Session extended for user 1
INFO 2025-02-04 10:45:00 - User logged out (role: customer)
WARNING 2025-02-04 11:00:15 - Session not found for user 2
ERROR 2025-02-04 12:00:00 - Error validating session: ...
```

---

## 🚀 DÉPLOIEMENT

### Production Checklist

```python
# settings.py pour production

# ✅ 1. HTTPS + Secure Cookies
SESSION_COOKIE_SECURE = True  # Seulement HTTPS
CSRF_COOKIE_SECURE = True

# ✅ 2. Domain Setting
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
SESSION_COOKIE_DOMAIN = '.yourdomain.com'

# ✅ 3. Secret Key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')  # From env

# ✅ 4. Cache en Redis (optionnel, meilleur que locmem)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# ✅ 5. Database Sessions (Backup)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ✅ 6. Désactiver DEBUG
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

---

## ❓ FAQ

### Q: Pourquoi la session est invalidée?
**R**: Vérifier:
- `SESSION_SAVE_EVERY_REQUEST = True` ✅
- Middleware dans l'ordre correct ✅
- Cookies acceptés par le navigateur ✅
- CSRF token envoyé ✅

### Q: Comment tester "Remember Me"?
**R**:
```python
session_service.create_session(user, remember_me=True)
# max_age = 30 jours au lieu de 14
```

### Q: La session du vendeur expire trop vite?
**R**:
```python
# Changer dans settings.py
SESSION_SELLER_MAX_AGE = 14 * 24 * 60 * 60  # 14 jours

# Ou dans SessionService
SESSION_CONFIG['seller']['max_age'] = ...
```

---

## 📞 SUPPORT

Pour plus d'infos, voir:
- `core/middleware/session_middleware.py` - Middlewares
- `users/services/session_service.py` - Logique service
- `users/session_views.py` - Endpoints API
- `shopina/settings.py` - Configuration

---

**Version**: 1.0  
**Date**: 2025-02-04  
**Statut**: ✅ Production Ready
