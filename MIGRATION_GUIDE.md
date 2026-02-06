# 📋 GUIDE DE MIGRATION - Session Management System

## 🎯 Objectif
Migrer de l'authentification JWT pure vers un système hybride JWT + Session persistante pour éviter les logouts involontaires.

---

## 📊 État Avant → Après

### AVANT: JWT Pur
```
┌─────────────────┐
│   Frontend      │
│   React/Vite    │
└────────┬────────┘
         │
    POST /api/auth/login/
    ├─ Retourne: JWT tokens
    ├─ Stockage: localStorage
    └─ Problème: ⚠️ Logout sur navigation
```

### APRÈS: JWT + Session
```
┌─────────────────────────────┐
│   Frontend React/Vite       │
│  ├─ sessionApi.ts (NEW)     │
│  ├─ SessionManager.tsx (NEW)│
│  └─ Modified: pages/login   │
└──────────────┬──────────────┘
               │
    POST /api/auth/login-with-session/
    ├─ Retourne: JWT + Session Data
    ├─ Stockage: localStorage + sessionStorage + Cookies
    ├─ Extension: Auto-refresh toutes les 5 min
    └─ ✅ Session persiste entre navigations
```

---

## 🛠️ Étapes de Migration

### Phase 1: Backend (DÉJÀ COMPLÉTÉE ✅)

#### ✅ 1.1 Middleware créés
- `core/middleware/session_middleware.py` - SessionPersistenceMiddleware, RoleBasedSessionMiddleware
- Ajoutés à `shopina/settings.py` MIDDLEWARE

#### ✅ 1.2 Service créé
- `users/services/session_service.py` - SessionService avec lifecycle complet

#### ✅ 1.3 Endpoints créés
- `users/session_views.py` - 4 endpoints:
  - POST /api/auth/login-with-session/
  - POST /api/auth/logout-with-session/
  - POST /api/auth/extend-session/
  - GET /api/auth/session-info/

#### ✅ 1.4 Settings mis à jour
- SESSION_SAVE_EVERY_REQUEST = True
- SESSION_EXPIRE_AT_BROWSER_CLOSE = False
- CSRF_USE_SESSIONS = True
- Role-based max ages (customer: 14d, seller: 7d, admin: 1d)

### Phase 2: Frontend (À FAIRE)

#### 2.1 Ajouter le service sessionApi.ts
```bash
# Copier le fichier créé
# Fichier: code source/front/src/services/sessionApi.ts
```

**Contenu clé:**
```typescript
// ✅ Créé: sessionApi.ts
- loginWithSession(email, password, rememberMe)
- logout()
- getSessionInfo()
- extendSession(rememberMe)
- startSessionRefresh() - Auto-refresh toutes les 5 minutes
- isLoggedIn()
- getUserRole()
- getSessionTimeRemaining()
```

#### 2.2 Ajouter le composant SessionManager.tsx
```bash
# Copier le fichier créé
# Fichier: code source/front/src/components/SessionManager.tsx
```

**Contenu clé:**
```typescript
// ✅ Créé: SessionManager.tsx
- <SessionManager /> - Affiche temps restant + avertissement
- <LoginForm /> - Formulaire de login avec remember_me
- <SessionStats /> - Affiche les statistiques
- useSession() - Hook personnalisé
```

#### 2.3 Mettre à jour les imports existants

**Avant (à remplacer dans api.ts):**
```typescript
// OLD: import { handleResponse } from './api';
const handleResponse = (response) => { ... };
const login = async (email, password) => {
  return fetch('/api/auth/login/', { ... });
};
```

**Après (nouveau style):**
```typescript
// NEW: import { sessionApi } from './sessionApi';
// Utiliser directement sessionApi.loginWithSession()
```

### Phase 3: Mise à Jour des Pages

#### 3.1 Page de Login

**Fichier:** `code source/front/src/pages/Login.tsx` ou `code source/front/src/pages/login.tsx`

**Avant:**
```typescript
import { handleResponse } from '../services/api';

export default function Login() {
  const handleSubmit = async (email, password) => {
    const response = await fetch('/api/auth/login/', { ... });
    const data = await handleResponse(response);
    localStorage.setItem('token', data.access);
    // ❌ Problème: Session expirée après quelques minutes
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" ... />
      <input type="password" ... />
      <button>Login</button>
    </form>
  );
}
```

**Après:**
```typescript
import { LoginForm } from '../components/SessionManager';

export default function Login() {
  const handleLoginSuccess = () => {
    // ✅ Session automatiquement créée et persistée
    window.location.href = '/dashboard';
  };

  return (
    <div className="login-page">
      <LoginForm onLoginSuccess={handleLoginSuccess} />
    </div>
  );
}
```

#### 3.2 Layout Principal (App.tsx ou _app.tsx)

**Fichier:** `code source/front/src/App.tsx` ou `code source/front/src/pages/_app.tsx`

**Avant:**
```typescript
// Pas de gestion de session
export default function App() {
  return (
    <div>
      <Header />
      <Routes>...</Routes>
    </div>
  );
}
```

**Après:**
```typescript
import { SessionManager } from './components/SessionManager';

export default function App() {
  return (
    <div>
      {/* 🆕 Afficher la barre de session en haut */}
      <SessionManager 
        showTimeRemaining={true}
        onSessionExpired={() => {
          alert('Votre session a expiré. Veuillez vous reconnecter.');
          window.location.href = '/login';
        }}
      />
      
      <Header />
      <Routes>...</Routes>
    </div>
  );
}
```

#### 3.3 Service d'API Existant (api.ts)

**Fichier:** `code source/front/src/services/api.ts`

**Ajouter:**
```typescript
// 🆕 Ajouter après les imports existants
import { sessionApi } from './sessionApi';

// 🆕 Fonction helper pour les appels API avec session
export const apiWithSession = {
  get: (url) => sessionApi.client.get(url),
  post: (url, data) => sessionApi.client.post(url, data),
  put: (url, data) => sessionApi.client.put(url, data),
  delete: (url) => sessionApi.client.delete(url),
};

// Utiliser apiWithSession au lieu de fetch() pour les requêtes protégées
```

---

## 🔄 Checklist de Migration

### Backend
- [x] ✅ SessionPersistenceMiddleware créé
- [x] ✅ RoleBasedSessionMiddleware créé
- [x] ✅ SessionService créé
- [x] ✅ Endpoints API créés
- [x] ✅ settings.py mis à jour
- [x] ✅ urls.py mis à jour
- [ ] Tests manuels (voir TEST_GUIDE_SESSION_MANAGEMENT.md)
- [ ] Tests unitaires (voir test_session_management.py)

### Frontend
- [ ] Copier `sessionApi.ts` vers `code source/front/src/services/`
- [ ] Copier `SessionManager.tsx` vers `code source/front/src/components/`
- [ ] Mettre à jour `pages/Login.tsx` (utiliser <LoginForm />)
- [ ] Mettre à jour `App.tsx` (ajouter <SessionManager />)
- [ ] Mettre à jour `services/api.ts` (ajouter sessionApi)
- [ ] Tests manuels des nouveaux endpoints
- [ ] Tests d'intégration frontend-backend

### Testing
- [ ] Run: `python manage.py test users.tests.test_session_management`
- [ ] Test manual: curl vs endpoints (voir TEST_GUIDE.md)
- [ ] Test E2E: Playwright (optionnel)

### Déploiement
- [ ] Code review des changements
- [ ] Merge vers main
- [ ] Déployer backend
- [ ] Déployer frontend
- [ ] Vérifier les logs en production

---

## 📝 Modifications Fichier par Fichier

### 1. Backend: `core/middleware/session_middleware.py` (NEW)
```
✅ CRÉÉ: 245 lignes
- SessionPersistenceMiddleware: Étend session toutes les requêtes
- RoleBasedSessionMiddleware: Détecte rôle et session séparée
- CSRFProtectionMiddleware: Validation CSRF améliorée
```

### 2. Backend: `users/services/session_service.py` (NEW)
```
✅ CRÉÉ: 195 lignes
- SessionService.create_session()
- SessionService.validate_session()
- SessionService.extend_session()
- SessionService.invalidate_session()
- SessionService.get_session_info()
```

### 3. Backend: `users/session_views.py` (NEW)
```
✅ CRÉÉ: 215 lignes
- LoginWithSessionView (POST /api/auth/login-with-session/)
- LogoutWithSessionView (POST /api/auth/logout-with-session/)
- ExtendSessionView (POST /api/auth/extend-session/)
- GetSessionInfoView (GET /api/auth/session-info/)
```

### 4. Backend: `shopina/settings.py` (MODIFIED)
```
✅ 3 modifications:
1. MIDDLEWARE: +3 middlewares custom (lignes 70-85)
2. SESSION config: +9 settings (lignes 230-240)
3. CSRF config: +6 settings (lignes 245-250)
```

### 5. Backend: `users/urls.py` (MODIFIED)
```
✅ 2 modifications:
1. Imports: +4 session views
2. URL patterns: +4 endpoints
```

### 6. Frontend: `src/services/sessionApi.ts` (NEW)
```
🆕 À CRÉER: 350+ lignes
- SessionApiService class
- Login/logout/extend/getSession methods
- Auto-refresh timer (5 minutes)
- Auth token management
```

### 7. Frontend: `src/components/SessionManager.tsx` (NEW)
```
🆕 À CRÉER: 400+ lignes
- <SessionManager /> component
- <LoginForm /> component
- <SessionStats /> component
- useSession() hook
```

### 8. Frontend: `src/pages/Login.tsx` (MODIFY)
```
📝 Remplacer la logique:
OLD: Direct fetch + JWT storage
NEW: Utiliser <LoginForm /> composant
```

### 9. Frontend: `src/App.tsx` (MODIFY)
```
📝 Ajouter en haut du layout:
- <SessionManager /> component
- Gérer onSessionExpired callback
```

### 10. Frontend: `src/services/api.ts` (MODIFY)
```
📝 Ajouter:
- Import sessionApi
- Exporter apiWithSession helper
```

---

## 🚀 Commandes de Déploiement

### Backend
```bash
# 1. Naviguer au répertoire backend
cd "d:\Shopina Project\code source\shopina-env\backend"

# 2. Appliquer les migrations (si nécessaire)
python manage.py migrate

# 3. Tester localement
python manage.py runserver

# 4. Tester l'endpoint
curl -X POST http://localhost:8000/api/auth/login-with-session/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Frontend
```bash
# 1. Naviguer au répertoire frontend
cd "d:\Shopina Project\code source\front"

# 2. Installer les dépendances (si nécessaire)
npm install

# 3. Tester localement
npm run dev

# 4. Build pour production
npm run build

# 5. Preview du build
npm run preview
```

---

## ⚠️ Points Critiques

### Session Cookie
```python
# settings.py
SESSION_COOKIE_HTTPONLY = True  # 🔐 Sécurité XSS
SESSION_COOKIE_SAMESITE = 'Lax'  # 🔐 CSRF protection
SESSION_SAVE_EVERY_REQUEST = True  # 🔑 Clé: Étend à chaque requête
```

### Frontend: Inclure les Cookies
```typescript
// sessionApi.ts
const client = axios.create({
  ...
  withCredentials: true,  // 🔑 Clé: Inclure les cookies
});
```

### Auto-Refresh
```typescript
// sessionApi.ts: Appelé toutes les 5 minutes
this.startSessionRefresh();
```

---

## 🔧 Dépannage

### Problème: "Session invalide" après login
**Solution:**
1. Vérifier `SESSION_SAVE_EVERY_REQUEST = True` dans settings.py
2. Vérifier `withCredentials: true` dans axios
3. Vérifier les logs: `tail -f logs/session.log`

### Problème: Token CSRF manquant
**Solution:**
1. Vérifier `CSRF_USE_SESSIONS = True` dans settings.py
2. Vérifier `CSRF_COOKIE_HTTPONLY = False` (pour JS)
3. Ajouter le header: `X-CSRFToken: <token>` dans les POST

### Problème: Session expirée trop vite
**Solution:**
1. Augmenter `SESSION_CUSTOMER_MAX_AGE` dans settings.py
2. Vérifier que `extendSession()` est appelée
3. Vérifier les logs pour voir les timestamps

---

## 📚 Ressources

- 📖 Guide complet: [SESSION_MANAGEMENT_GUIDE.md](SESSION_MANAGEMENT_GUIDE.md)
- 🧪 Guide de test: [TEST_GUIDE_SESSION_MANAGEMENT.md](TEST_GUIDE_SESSION_MANAGEMENT.md)
- 🔧 Tests unitaires: [backend/users/tests/test_session_management.py](code%20source/shopina-env/backend/users/tests/test_session_management.py)

---

## 📊 Bénéfices Après Migration

| Aspect | Avant | Après |
|--------|-------|-------|
| **Logout involontaire** | ❌ Oui | ✅ Non |
| **Persistance** | ❌ JWT expires | ✅ 14 jours (client) |
| **Auto-refresh** | ❌ Non | ✅ Toutes les 5 min |
| **Remember Me** | ❌ Non | ✅ 30 jours |
| **Séparation rôles** | ❌ Non | ✅ Oui (client/seller/admin) |
| **CSRF protection** | ⚠️ Basique | ✅ Complète |
| **Session display** | ❌ Non | ✅ Affichage temps restant |

---

## 🎯 Prochaines Étapes

1. **Aujourd'hui:**
   - [ ] Créer/copier les fichiers frontend
   - [ ] Tester les endpoints manuellement
   - [ ] Exécuter les tests unitaires

2. **Demain:**
   - [ ] Intégrer dans l'app React
   - [ ] Tester end-to-end
   - [ ] Code review

3. **Cette semaine:**
   - [ ] Déployer en production
   - [ ] Monitorer les logs
   - [ ] Collecter le feedback utilisateur

---

**Durée estimée:** 2-3 heures (frontend) + 1 heure (tests) + 1 heure (déploiement) = **4-5 heures totales**

**Risque:** 🟢 BAS (Backward compatible, pas breaking changes)

**Rollback:** 🟢 FACILE (Revert les changements UI/services, gardez les endpoints)
