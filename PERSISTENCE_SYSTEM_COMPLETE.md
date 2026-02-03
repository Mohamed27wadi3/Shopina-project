# 🔐 Système de Persistance - Sauvegarde Permanente

## 📋 Architecture de Persistance

### 1. Flux de Sauvegarde (Permanent)

```
┌─────────────────────────────────────────────────────────────┐
│  UTILISATEUR CLIQUE "SAVE"                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  1. VALIDATION                                               │
│  ├─ Vérifier que shop existe                                 │
│  ├─ Vérifier que customization n'est pas vide               │
│  └─ Vérifier le token d'authentification                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. PRÉPARATION                                              │
│  Collecter TOUS les états:                                   │
│  ├─ name, description                                        │
│  ├─ Couleurs (primary, secondary, accent)                   │
│  ├─ Fonts (body, heading)                                    │
│  ├─ Layout (style, header, footer)                          │
│  ├─ Grid (columns, imageRatio)                              │
│  ├─ Visual (borderRadius, shadows, spacing)                 │
│  └─ Features (search, filters, wishlist, etc.)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. ENVOI PATCH REQUEST                                      │
│  PATCH /shop/api/my-shop/                                    │
│  Headers: Authorization Bearer {token}                      │
│  Body: {                                                     │
│    "name": "...",                                            │
│    "description": "...",                                     │
│    "customization": { ... }                                  │
│  }                                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  4. BACKEND TRAITEMENT                                       │
│  Django:                                                     │
│  ├─ Reçoit PATCH request                                     │
│  ├─ Valide les données                                       │
│  ├─ Récupère le Shop existant (UPDATE mode)                 │
│  ├─ Remplace customization                                   │
│  ├─ Valide les changements                                   │
│  ├─ SAUVEGARDE EN BASE DE DONNÉES                            │
│  └─ Retourne le Shop mis à jour (JSON)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  5. VÉRIFICATION RÉPONSE                                     │
│  if (res.ok)                                                 │
│  ├─ const updatedData = await res.json()                    │
│  ├─ setShop(updatedData)  ← ÉTAT LOCAL = DB                │
│  └─ Succès confirmé ✅                                       │
│  else                                                        │
│  ├─ Afficher erreur                                          │
│  └─ Ne pas rediriger                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  6. CONFIRMATION UTILISATEUR                                 │
│  ├─ Toast: "✅ Saved successfully!"                          │
│  ├─ Console: Log des données sauvegardées                   │
│  └─ Redirection: Vers /my-shop après 1.5s                   │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flux de Chargement (Récupération)

```
┌─────────────────────────────────────────────────────────────┐
│  UTILISATEUR OUVRE /customize-shop                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  1. COMPONENT MOUNT (useEffect)                              │
│  → Appel loadStore()                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. FETCH FROM DATABASE                                      │
│  GET /shop/api/my-shop/                                      │
│  Headers: Authorization Bearer {token}                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. BACKEND RETOURNE LES DONNÉES                             │
│  {                                                           │
│    "id": 1,                                                  │
│    "name": "...",                                            │
│    "description": "...",                                     │
│    "customization": {                                        │
│      "primaryColor": "#0077FF",  ← SAUVEGARDÉ PRÉCÉDEMMENT  │
│      "secondaryColor": "#5AC8FA",                           │
│      ... (tous les changements précédents)                   │
│    },                                                        │
│    "updated_at": "2024-..."                                  │
│  }                                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  4. FRONTEND RESTAURE L'ÉTAT                                 │
│  ├─ setShop(data)                                            │
│  ├─ setName(data.name)                                       │
│  ├─ setDescription(data.description)                        │
│  ├─ Charger customization:                                   │
│  │  ├─ setPrimaryColor(custom.primaryColor)                 │
│  │  ├─ setSecondaryColor(custom.secondaryColor)             │
│  │  ├─ ... (tous les États)                                 │
│  │  └─ setFeatures(custom.features)                         │
│  └─ EXACT MÊME ÉTAT QU'AVANT ✅                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  5. LIVE PREVIEW MIS À JOUR                                  │
│  L'interface affiche les saved customizations                │
│  L'utilisateur voit exactement ce qu'il a sauvegardé        │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Garanties de Persistance

### Garantie 1: Sauvegarde en Base de Données

```typescript
// ✅ RÉEL
PATCH /shop/api/my-shop/
→ Django UPDATE Shop SET customization = ...
→ SQL: UPDATE shop_shop SET customization = '...' WHERE id = 1
→ POSTGRESQL/MYSQL: Enregistré en base
```

❌ **PAS**: localStorage uniquement (volatile, supprimé au clear cache)
❌ **PAS**: State uniquement (perdu au refresh)

### Garantie 2: Récupération Authentifiée

```typescript
// ✅ SÉCURISÉ
GET /shop/api/my-shop/
Headers: Authorization Bearer {token}
→ Backend vérifie le token
→ Retourne ONLY les données de l'utilisateur actuel
→ Protection CSRF activée
```

### Garantie 3: Validation des Données

```typescript
// ✅ VALIDÉ
Backend valide:
├─ User authentifié
├─ Shop appartient à l'utilisateur
├─ Customization format valide
├─ Pas d'injection SQL
├─ Pas de données corrompues
└─ SAUVEGARDE SÛRE
```

### Garantie 4: Synchronisation État-DB

```typescript
// ✅ SYNCHRONISÉ
Frontend:
const updatedData = await res.json();
setShop(updatedData);  // ← État = Database exactement

Backend:
return {
  ...shop,
  customization: new_customization,
  updated_at: now()
}
```

## 🧪 Test de Persistance

### Scénario 1: Sauvegarde Basique

```
1. Aller à /customize-shop
2. Changer Primary Color: #0077FF → #FF0000
3. Cliquer "SAVE"
   ✅ Toast: "Saved successfully!"
   ✅ Redirect to /my-shop
4. Revenir à /customize-shop
   ✅ Primary Color = #FF0000 (SAUVEGARDÉ)
```

### Scénario 2: Refresh Page

```
1. Customizer la boutique
2. Cliquer "SAVE"
3. **Refresh la page** (Ctrl+R)
4. Ouvrir /customize-shop
   ✅ Tous les changements sont là
   ✅ Pas de perte de données
```

### Scénario 3: Logout/Login

```
1. Customizer et SAVE
2. Logout (/logout)
3. Login à nouveau
4. Aller à /customize-shop
   ✅ Toutes les modifications persistent
   ✅ Les données sont du serveur, pas du cache
```

### Scénario 4: Reload Complet

```
1. Customizer et SAVE
2. Fermer le navigateur complètement
3. Rouvrir le navigateur
4. Aller à /customize-shop
   ✅ Modifications sont toujours là
   ✅ Récupérées du serveur
```

### Scénario 5: Multiple Sessions

```
Session A:
1. Customizer: Primary Color = #FF0000
2. SAVE
3. Modifier: Primary Color = #00FF00
4. SAVE

Session B (onglet différent):
1. Ouvrir /customize-shop
   ✅ Voir les changements de Session A
   ✅ Données synchronisées en temps réel
```

## 🔍 Vérification en Console

### Vérifier la Sauvegarde

```javascript
// F12 → Console

// 1. Voir les données sauvegardées
✅ Données sauvegardées: {
  name: "Ma Boutique",
  description: "...",
  customization: {
    primaryColor: "#0077FF",
    ...
  }
}

// 2. Vérifier Network
F12 → Network
Chercher: "my-shop" (PATCH)
Status: 200 OK
Response Body: Les données mises à jour
```

### Vérifier le Chargement

```javascript
// Quand la page charge:
✅ Customization loaded from DB: {
  primaryColor: "#0077FF",
  secondaryColor: "#5AC8FA",
  ...
}
```

## 📊 Structure de Données Sauvegardée

### Base de Données (PostgreSQL/MySQL)

```sql
-- Table: shop_shop
CREATE TABLE shop_shop (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  name VARCHAR(255),
  description TEXT,
  customization JSON,  -- ← TOUTES les modifications ici
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

-- Exemple de données:
{
  "id": 1,
  "user_id": 5,
  "name": "Ma Boutique",
  "description": "Description",
  "customization": {
    "primaryColor": "#0077FF",
    "secondaryColor": "#5AC8FA",
    "accentColor": "#FFD43B",
    "fontFamily": "Inter",
    "headingFont": "Poppins",
    "layoutStyle": "modern",
    "headerStyle": "sticky",
    "footerColumns": "4",
    "gridColumns": "3",
    "imageRatio": "1:1",
    "borderRadius": "12",
    "shadows": "medium",
    "spacing": "comfortable",
    "features": {
      "search": true,
      "filters": true,
      "wishlist": true,
      "quickView": true,
      "reviews": true,
      "newsletter": true
    }
  },
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-02-03T14:30:00Z"
}
```

## 🛡️ Sécurité de la Persistance

### Authentification
```typescript
✅ Token Bearer vérifié
✅ User ID check (user_id = current_user)
✅ Pas d'accès aux données d'autres utilisateurs
```

### Validation
```typescript
✅ Customization JSON valide
✅ Pas d'injection SQL
✅ Pas de XSS
✅ CSRF protection activée
```

### Confidentialité
```typescript
✅ Données encryptées en transit (HTTPS)
✅ Données stockées sécurisées en DB
✅ Backups réguliers
✅ Audit trail (created_at, updated_at)
```

## 🎯 Checklist de Fonctionnement

- [x] Save action envoie PATCH request
- [x] Backend reçoit et valide
- [x] Données sauvegardées en DB
- [x] Réponse retourne les données
- [x] Frontend met à jour state
- [x] Toast de succès affiché
- [x] Redirection vers /my-shop
- [x] Load action fetch GET request
- [x] Données du DB sont chargées
- [x] États sont restaurés
- [x] Live preview mis à jour
- [x] Refresh page = données persistent
- [x] Logout/login = données persistent
- [x] Fermer navigateur = données persistent
- [x] Pas de localStorage seul
- [x] Authentification vérifiée

## ✅ Résumé de la Persistance

**La sauvegarde est permanente quand:**

1. ✅ Toutes les modifications sont collectées dans `customizationData`
2. ✅ Requête PATCH envoie les données au serveur
3. ✅ Backend Django reçoit, valide et SAUVEGARDE EN DB
4. ✅ Réponse contient les données mises à jour
5. ✅ Frontend met à jour `setShop(updatedData)`
6. ✅ Toast confirme la sauvegarde
7. ✅ Au chargement suivant: `loadStore()` fetch depuis DB
8. ✅ États restaurés exactement comme sauvegardés

**Les données persistent après:**

✅ Page refresh (Ctrl+R)
✅ Logout/login
✅ Fermer navigateur
✅ Onglets multiples
✅ Sessions multiples
✅ Redémarrage du serveur

**À cause de:**

✅ Stockage permanent en base de données
✅ Pas de dépendance localStorage
✅ Authentification vérifiée
✅ Données validées
✅ Synchronisation d'état frontend-backend
