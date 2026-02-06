# 🧪 Guide de Test - Système de Gestion de Session

## 1️⃣ Tests Unitaires avec Django

```powershell
# Naviguer au répertoire backend
cd "d:\Shopina Project\code source\shopina-env\backend"

# Exécuter tous les tests de session
python manage.py test users.tests.test_session_management -v 2

# Tester un cas spécifique
python manage.py test users.tests.test_session_management.SessionServiceTests.test_create_session_customer -v 2

# Tester avec couverture de code
pip install coverage
coverage run --source='users' manage.py test users.tests.test_session_management
coverage report
coverage html
```

## 2️⃣ Tests Manuels via cURL

### A. Login avec Session

```bash
# 📝 Étape 1: Login et créer une session
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "remember_me": false
  }' \
  -c cookies.txt \
  -v

# ✅ Réponse attendue:
# {
#   "success": true,
#   "user": {"id": 1, "username": "test", ...},
#   "tokens": {
#     "access": "eyJ0eXAi...",
#     "refresh": "eyJ0eXAi..."
#   },
#   "session": {
#     "username": "test",
#     "role": "customer",
#     "created_at": "2024-01-15T10:30:00Z",
#     "expires_at": "2024-01-29T10:30:00Z"
#   }
# }
```

### B. Vérifier Info de Session

```bash
# 📌 Étape 2: Vérifier les infos de session
curl -X GET http://localhost:8000/api/auth/session-info/ \
  -b cookies.txt \
  -v

# ✅ Réponse attendue:
# {
#   "success": true,
#   "username": "test",
#   "role": "customer",
#   "created_at": "2024-01-15T10:30:00Z",
#   "expires_at": "2024-01-29T10:30:00Z",
#   "is_valid": true
# }
```

### C. Étendre la Session

```bash
# ⏰ Étape 3: Étendre la session (simule naviguer entre pages)
curl -X POST http://localhost:8000/api/auth/extend-session/ \
  -H "Content-Type: application/json" \
  -d '{"remember_me": false}' \
  -b cookies.txt \
  -v

# ✅ Session doit être étendue
# Le timestamp "expires_at" doit être plus loin
```

### D. Logout

```bash
# 🚪 Étape 4: Logout et invalider la session
curl -X POST http://localhost:8000/api/auth/logout-with-session/ \
  -b cookies.txt \
  -v

# ✅ Réponse attendue:
# {"success": true, "message": "Logged out successfully"}

# ❌ Vérifier que la session est invalidée
curl -X GET http://localhost:8000/api/auth/session-info/ \
  -b cookies.txt

# Doit retourner 401 Unauthorized
```

## 3️⃣ Tests Postman/Insomnia

### Collection JSON

```json
{
  "info": {
    "name": "Session Management",
    "description": "Tests pour le système de session"
  },
  "item": [
    {
      "name": "Login avec Session",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/auth/login-with-session/",
        "body": {
          "mode": "raw",
          "raw": "{\"email\": \"test@example.com\", \"password\": \"testpass123\", \"remember_me\": false}"
        }
      }
    },
    {
      "name": "Info de Session",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/auth/session-info/"
      }
    },
    {
      "name": "Étendre Session",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/auth/extend-session/",
        "body": {
          "mode": "raw",
          "raw": "{\"remember_me\": false}"
        }
      }
    },
    {
      "name": "Logout",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/auth/logout-with-session/"
      }
    }
  ]
}
```

## 4️⃣ Scénarios de Test End-to-End

### 📍 Scénario 1: Pas de Logout Involontaire

```bash
# Étape 1: Login
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}' \
  -c cookies.txt

# Étape 2: Attendre 10 secondes (simuler navigation lente)
timeout 10

# Étape 3: Accéder à une ressource protégée
curl -X GET http://localhost:8000/api/auth/session-info/ \
  -b cookies.txt

# ✅ RÉSULTAT ATTENDU: Session valide, pas de logout
```

### 🔑 Scénario 2: Séparation Client/Vendeur

```bash
# ===== CLIENT =====
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{"email": "customer@example.com", "password": "pass123"}' \
  -c customer_cookies.txt

curl -X GET http://localhost:8000/api/auth/session-info/ \
  -b customer_cookies.txt
# ✅ expires_at: 14 jours à partir de maintenant

# ===== VENDEUR =====
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{"email": "seller@example.com", "password": "pass123"}' \
  -c seller_cookies.txt

curl -X GET http://localhost:8000/api/auth/session-info/ \
  -b seller_cookies.txt
# ✅ expires_at: 7 jours à partir de maintenant (plus court)
```

### 💾 Scénario 3: Remember Me

```bash
# SANS remember me (durée normal)
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "remember_me": false}' \
  -c cookies1.txt

curl -X GET http://localhost:8000/api/auth/session-info/ \
  -b cookies1.txt | grep expires_at
# ✅ Expires dans 14 jours

# AVEC remember me (durée prolongée)
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "remember_me": true}' \
  -c cookies2.txt

curl -X GET http://localhost:8000/api/auth/session-info/ \
  -b cookies2.txt | grep expires_at
# ✅ Expires dans 30 jours (plus long)
```

## 5️⃣ Tests de Sécurité CSRF

### Vérifier le Token CSRF

```bash
# Obtenir le token CSRF
curl -X GET http://localhost:8000/api/shop/products/ \
  -H "X-Requested-With: XMLHttpRequest" \
  -c csrf_cookies.txt \
  -v

# ✅ Header: Set-Cookie: shopina_csrf=...

# Utiliser le token pour POST
CSRF_TOKEN=$(grep shopina_csrf csrf_cookies.txt | awk '{print $7}')

curl -X POST http://localhost:8000/api/auth/logout-with-session/ \
  -H "X-CSRFToken: $CSRF_TOKEN" \
  -b csrf_cookies.txt \
  -v

# ✅ Doit accepter la requête (200 OK)
```

## 6️⃣ Tests de Performance

### Tester l'extension de session rapidement

```powershell
# PowerShell: Boucle rapide pour tester l'extension
$headers = @{"Content-Type" = "application/json"}
$body = @{remember_me = $false} | ConvertTo-Json

# 100 requêtes d'extension
for ($i = 1; $i -le 100; $i++) {
    $response = Invoke-WebRequest `
        -Uri "http://localhost:8000/api/auth/extend-session/" `
        -Method POST `
        -Headers $headers `
        -Body $body `
        -WebSession $session
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Requête $i réussie"
    } else {
        Write-Host "❌ Requête $i échouée: $($response.StatusCode)"
        break
    }
}
```

## 7️⃣ Vérifier les Logs

### Logs de Session

```bash
# Voir les derniers logs
tail -f "d:\Shopina Project\code source\shopina-env\backend\logs\session.log"

# 📝 Format attendu:
# [2024-01-15 10:30:00] INFO    Session created: user=1, role=customer, expires_at=2024-01-29 10:30:00
# [2024-01-15 10:30:05] INFO    Session extended: user=1, role=customer, new_expires_at=2024-01-29 10:30:05
# [2024-01-15 10:30:10] INFO    Session validated: user=1, role=customer, valid=True
# [2024-01-15 10:31:00] INFO    Session invalidated: user=1, role=customer
```

### Accès Django Session DB

```bash
# Voir toutes les sessions actives
python manage.py dbshell
SELECT * FROM django_session;

# Voir une session spécifique
SELECT session_key, session_data FROM django_session WHERE session_key='abc123...';
```

## 8️⃣ Checklist de Validation ✅

### Backend
- [x] SessionService crée/valide/étend les sessions
- [x] RoleBasedSessionMiddleware détecte le rôle
- [x] SessionPersistenceMiddleware étend sur chaque requête
- [x] URLs mappées correctement
- [x] Logs enregistrés

### Frontend
- [ ] Utilise POST /api/auth/login-with-session/ au lieu de /api/auth/login/
- [ ] Appelle POST /api/auth/extend-session/ toutes les 5 minutes
- [ ] Gère 401 Unauthorized pour logout involontaire
- [ ] Affiche l'heure d'expiration à l'utilisateur

### Sécurité
- [x] SESSION_COOKIE_HTTPONLY = True (XSS protection)
- [x] SESSION_COOKIE_SAMESITE = 'Lax' (CSRF protection)
- [x] CSRF_USE_SESSIONS = True
- [x] Passwords hachés
- [ ] HTTPS en production (SESSION_COOKIE_SECURE = True)

## 9️⃣ Dépannage Courant

### Problème: Session expirée trop vite
**Solution:**
```python
# Vérifier dans settings.py
SESSION_SAVE_EVERY_REQUEST = True  # Doit être True
SESSION_COOKIE_AGE = 14 * 24 * 60 * 60  # 14 jours
```

### Problème: Token CSRF invalide
**Solution:**
```python
# Vérifier dans settings.py
CSRF_USE_SESSIONS = True  # Doit être True
CSRF_COOKIE_HTTPONLY = False  # JS doit pouvoir lire
```

### Problème: Middleware non exécuté
**Solution:**
```python
# Vérifier l'ordre dans MIDDLEWARE
# SessionPersistenceMiddleware doit être AVANT les vues
# RoleBasedSessionMiddleware doit être APRÈS SessionPersistenceMiddleware
```

## 🔟 Prochaines Étapes

1. ✅ Exécuter les tests unitaires
2. ✅ Tester les endpoints manuellement
3. ✅ Tester les scénarios end-to-end
4. ✅ Vérifier les logs
5. 📝 Mettre à jour le frontend (voir SESSION_MANAGEMENT_GUIDE.md)
6. 🚀 Déployer en production

---

**📊 Résumé des Tests:**
- Tests unitaires: 10 cas
- Tests manuels: 5 scénarios
- Tests de sécurité: 2 cas
- Tests de performance: 1 benchmark
- **Total: 18 tests**

**🎯 Objectif:** Validez que:
1. ✅ Session persiste après login
2. ✅ Pas de logout involontaire
3. ✅ Rôles séparés (client/vendeur/admin)
4. ✅ Remember me fonctionne
5. ✅ CSRF tokens valides
