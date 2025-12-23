# Configuration OAuth - Guide Rapide

## Pourquoi les boutons Google/GitHub ne fonctionnent pas actuellement ?

Les boutons sociaux sont **désactivés temporairement** car ils nécessitent :
1. ✅ Backend configuré (déjà fait)
2. ❌ Credentials OAuth de Google (à créer)
3. ❌ Credentials OAuth de GitHub (à créer)
4. ❌ Ajout des credentials dans Django Admin

---

## Solution Rapide : Activer OAuth en 15 minutes

### Étape 1 : Créer Google OAuth (5 minutes)

1. Aller sur https://console.cloud.google.com/
2. Créer un nouveau projet : "Shopina"
3. Aller dans "APIs & Services" > "Credentials"
4. Cliquer "Create Credentials" > "OAuth 2.0 Client ID"
5. Type: "Web application"
6. Authorized redirect URIs:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
7. Copier le **Client ID** et **Client Secret**

### Étape 2 : Créer GitHub OAuth (3 minutes)

1. Aller sur https://github.com/settings/applications/new
2. Remplir :
   - Application name: `Shopina`
   - Homepage URL: `http://localhost:3003`
   - Authorization callback URL: `http://localhost:8000/accounts/github/login/callback/`
3. Cliquer "Register application"
4. Copier le **Client ID** et générer un **Client Secret**

### Étape 3 : Ajouter dans Django Admin (5 minutes)

1. Démarrer le backend :
   ```bash
   cd "d:\Shopina Project\code source\shopina-env\backend"
   python manage.py runserver
   ```

2. Aller sur http://localhost:8000/admin/

3. Se connecter avec :
   - Email: admin@shopina.com
   - Password: admin123

4. Dans "Sites" > Cliquer sur "example.com"
   - Domain name: `localhost:3003`
   - Display name: `Shopina Local`
   - Sauvegarder

5. Dans "Social applications" > "Add social application"
   
   **Pour Google :**
   - Provider: Google
   - Name: Google
   - Client id: (coller le Client ID de Google)
   - Secret key: (coller le Client Secret de Google)
   - Sites: Sélectionner "localhost:3003"
   - Sauvegarder

   **Pour GitHub :**
   - Provider: GitHub
   - Name: GitHub
   - Client id: (coller le Client ID de GitHub)
   - Secret key: (coller le Client Secret de GitHub)
   - Sites: Sélectionner "localhost:3003"
   - Sauvegarder

### Étape 4 : Activer les boutons dans le code (2 minutes)

1. Ouvrir `LoginPage.tsx`
2. Dans `handleGoogleLogin()`, décommenter la ligne :
   ```typescript
   window.location.href = `http://localhost:8000/accounts/google/login/?next=${encodeURIComponent('http://localhost:3003/dashboard')}`;
   ```
3. Retirer/commenter le `toast.info()`

4. Dans `handleGitHubLogin()`, décommenter la ligne :
   ```typescript
   window.location.href = `http://localhost:8000/accounts/github/login/?next=${encodeURIComponent('http://localhost:3003/dashboard')}`;
   ```
5. Retirer/commenter le `toast.info()`

6. Faire pareil dans `SignupPage.tsx`

### Étape 5 : Tester

1. Redémarrer le frontend :
   ```bash
   cd "d:\Shopina Project\code source\front"
   npm run dev
   ```

2. Aller sur http://localhost:3003/login

3. Cliquer "Google" ou "GitHub"

4. S'authentifier avec votre compte

5. Vous serez redirigé vers le dashboard après connexion ✅

---

## Dépannage

### "Page blanche" après clic sur Google/GitHub
- ✅ **Solution actuelle** : Messages informatifs affichés
- ✅ **Solution permanente** : Suivre les étapes ci-dessus

### "Site not found" après OAuth
- Vérifier que le Site dans Django Admin a le bon domaine : `localhost:3003`

### "Invalid client" erreur
- Vérifier que les Client ID et Secret sont corrects
- Vérifier que les redirect URIs matchent exactement

### Redirect vers mauvaise page
- Vérifier `LOGIN_REDIRECT_URL` dans settings.py : `http://localhost:3003/dashboard`

---

## Alternative : Utiliser seulement Email/Password

Si vous ne voulez pas configurer OAuth maintenant, vous pouvez :

1. Masquer les boutons sociaux dans `LoginPage.tsx` et `SignupPage.tsx`
2. Ou les laisser avec les messages informatifs actuels
3. Utiliser uniquement l'authentification email/password (qui fonctionne parfaitement)

---

## Statut Actuel

- ✅ Email/Password login : **Fonctionne**
- ✅ Remember Me : **Fonctionne**
- ✅ User registration : **Fonctionne**
- ⏳ Google OAuth : **Prêt, attend credentials**
- ⏳ GitHub OAuth : **Prêt, attend credentials**

---

**Temps total pour activer OAuth** : ~15 minutes
**Difficulté** : Facile (copier-coller de credentials)

