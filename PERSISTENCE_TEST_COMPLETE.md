# 🧪 Guide de Test - Persistance Complète de la Sauvegarde

## 📋 Test Suite Complète

### ✅ Test 1: Sauvegarde Simple

**Objectif:** Vérifier que les modifications sont sauvegardées

**Étapes:**

1. Accéder à `/customize-shop`
2. Modifier la **Primary Color** de `#0077FF` → `#FF0000`
3. Cliquer le bouton "**Sauvegarder**"

**Résultats Attendus:**
```
Console (F12):
✅ Envoi de la sauvegarde: { name: "...", customization: { primaryColor: "#FF0000" } }
✅ Vérification de synchronisation: { sent: {...}, received: {...}, match: true }
✅ Données persistées en base de données: { shopId: 1, updatedAt: "2024-..." }

UI:
✅ Toast vert: "✅ Customization sauvegardée avec succès!"
✅ Redirection vers /my-shop après 1.5s

Network (F12 → Network):
✅ PATCH /shop/api/my-shop/
✅ Status: 200 OK
✅ Response: { id: 1, customization: { primaryColor: "#FF0000" }, ... }
```

---

### ✅ Test 2: Refresh Page (Persistence)

**Objectif:** Vérifier que les données persistent après refresh

**Étapes:**

1. Compléter Test 1
2. **Rafraîchir la page** (Ctrl+R ou F5)
3. Attendre le chargement complètement

**Résultats Attendus:**
```
Console (F12):
✅ 📥 Chargement des données du serveur...
✅ ✅ Customization chargée du serveur: { primaryColor: "#FF0000", ... }
✅ ✅ États restaurés du serveur pour: { shopId: 1, updatedAt: "..." }

UI:
✅ Primary Color affiche #FF0000 (SAUVEGARDÉE)
✅ Live preview montre la couleur rouge
✅ Tous les changements sont présents

Database:
✅ Données toujours en base de données
```

**❌ ÉCHEC si:**
- Primary Color revient à `#0077FF` → Données non sauvegardées
- Console affiche des erreurs

---

### ✅ Test 3: Logout/Login

**Objectif:** Vérifier que les données persistent après déconnexion/reconnexion

**Étapes:**

1. Compléter Test 1 (Sauvegarde avec `primaryColor: "#FF0000"`)
2. Aller à `/logout` ou cliquer le bouton Logout
3. **Se reconnecter** avec les mêmes identifiants
4. Aller à `/customize-shop`

**Résultats Attendus:**
```
Console (F12):
✅ 📥 Chargement des données du serveur...
✅ ✅ Customization chargée du serveur: { primaryColor: "#FF0000", ... }

UI:
✅ Primary Color = #FF0000 (PERSISTÉ)
✅ Description = valeur sauvegardée
✅ Tous les changements présents

Network:
✅ GET /shop/api/my-shop/ → Récupère depuis DB
✅ Status: 200 OK
✅ Les données retournées sont exactement ce qui a été sauvegardé
```

**❌ ÉCHEC si:**
- Affiche les valeurs par défaut
- Console affiche "Aucune customization trouvée"

---

### ✅ Test 4: Fermer et Rouvrir le Navigateur

**Objectif:** Vérifier la persistance complète (pas juste localStorage)

**Étapes:**

1. Compléter Test 1 (Sauvegarde)
2. **Fermer le navigateur complètement** (Cmd+Q ou Alt+F4)
3. Rouvrir le navigateur
4. Se reconnecter si nécessaire
5. Aller à `/customize-shop`

**Résultats Attendus:**
```
Console:
✅ ✅ Customization chargée du serveur: { primaryColor: "#FF0000", ... }

UI:
✅ Toutes les modifications sont TOUJOURS présentes
✅ Primary Color = #FF0000

Raison:
✅ Les données viennent du SERVEUR (DB)
✅ Pas du localStorage (qui aurait été supprimé)
```

**❌ ÉCHEC si:**
- Données perdues
- Console affiche une erreur lors du fetch

---

### ✅ Test 5: Multiple Modifications - Save

**Objectif:** Vérifier que TOUS les changements sont sauvegardés

**Étapes:**

1. Accéder à `/customize-shop`
2. Modifier **5 paramètres différents:**
   - Primary Color: `#0077FF` → `#FF0000`
   - Secondary Color: `#5AC8FA` → `#00FF00`
   - Font Family: `Inter` → `Poppins`
   - Layout Style: `modern` → `classic`
   - Border Radius: `12` → `20`
3. Cliquer **"Sauvegarder"**
4. **Rafraîchir la page**

**Résultats Attendus:**
```
Console (après refresh):
✅ ✅ Customization chargée du serveur: {
    primaryColor: "#FF0000",
    secondaryColor: "#00FF00",
    fontFamily: "Poppins",
    layoutStyle: "classic",
    borderRadius: "20",
    ... (tous les autres changements)
}

UI (après refresh):
✅ Primary Color = #FF0000
✅ Secondary Color = #00FF00
✅ Font Family = Poppins
✅ Layout Style = classic
✅ Border Radius = 20

✅ TOUS les changements sont sauvegardés
```

---

### ✅ Test 6: Vérifier la Synchronisation DB

**Objectif:** Confirmer que les données sont réellement en base de données

**Étapes (Backend):**

1. Compléter Test 1
2. Accéder au terminal du serveur Django
3. Exécuter:
   ```bash
   python manage.py shell
   >>> from shop.models import Shop
   >>> shop = Shop.objects.get(user_id=1)
   >>> import json
   >>> print(json.dumps(shop.customization, indent=2))
   ```

**Résultats Attendus:**
```json
{
  "primaryColor": "#FF0000",
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
  "features": {...}
}
```

✅ Les données sont **RÉELLEMENT** en base de données

---

### ✅ Test 7: Erreur Réseau Simulée

**Objectif:** Vérifier le comportement en cas d'erreur

**Étapes:**

1. Ouvrir DevTools (F12 → Network)
2. **Désactiver le réseau** (Offline mode)
3. Modifier une valeur
4. Cliquer "Sauvegarder"
5. Vérifier les messages d'erreur

**Résultats Attendus:**
```
Console:
❌ Erreur lors de la sauvegarde: Network request failed

UI:
❌ Toast rouge: "❌ Erreur réseau - Impossible de sauvegarder"
❌ Pas de redirection (reste sur la page)
❌ Les modifications restent en mémoire

Réactivation du réseau:
1. Réactiver le réseau
2. Cliquer "Sauvegarder" à nouveau
3. Succès ✅

Les données n'ont pas été perdues, juste pas sauvegardées temporairement
```

---

### ✅ Test 8: Validation des Données

**Objectif:** Vérifier que le formulaire valide les données

**Étapes:**

1. Accéder à `/customize-shop`
2. **Effacer le nom** de la boutique (laisser vide)
3. Cliquer "Sauvegarder"

**Résultats Attendus:**
```
Console:
❌ Erreur: Le nom de la boutique est requis

UI:
❌ Toast rouge: "❌ Le nom de la boutique est requis"
❌ Pas d'envoi au serveur
❌ Reste sur la page de customization

Correction:
1. Entrer un nom
2. Cliquer "Sauvegarder"
3. Succès ✅
```

---

### ✅ Test 9: État Local vs Serveur

**Objectif:** Vérifier la synchronisation exacte

**Étapes:**

1. Ouvrir DevTools Console (F12)
2. Modifier une couleur et cliquer "Sauvegarder"
3. Vérifier le message de synchronisation

**Résultats Attendus:**
```
Console (après save):
✅ Vérification de synchronisation: {
  sent: {
    "primaryColor": "#FF0000",
    ... (données envoyées)
  },
  received: {
    "primaryColor": "#FF0000",
    ... (données reçues du serveur)
  },
  match: true  ← SYNCHRONISÉ PARFAITEMENT
}
```

**❌ ÉCHEC si:**
- `match: false` → Les données envoyées ≠ données reçues
- Valeurs différentes

---

### ✅ Test 10: Scénario Complet (E2E)

**Objectif:** Simuler un workflow utilisateur complet

**Étapes:**

1. **Jour 1 - Session 1:**
   - Accéder à `/customize-shop`
   - Modifier: Primary Color → `#FF0000`
   - Cliquer "Sauvegarder"
   - Vérifier: Toast de succès ✅

2. **Jour 1 - Session 2 (même jour, après quelques heures):**
   - Navigateur toujours ouvert
   - Aller à `/my-shop` puis revenir à `/customize-shop`
   - Résultat: Couleur rouge persiste ✅

3. **Jour 2 - Nouveau jour:**
   - Fermer navigateur
   - Rouvrir navigateur
   - Se reconnecter
   - Aller à `/customize-shop`
   - Résultat: Couleur rouge toujours présente ✅

4. **Jour 3 - Autre changement:**
   - Modifier: Secondary Color → `#00FF00`
   - Cliquer "Sauvegarder"
   - Rafraîchir
   - Résultat: Les DEUX couleurs sont sauvegardées ✅

**Résultats Attendus:**
```
✅ Toutes les données persistent indéfiniment
✅ Pas de perte de données
✅ Tous les changements accumulés sont sauvegardés
✅ Le système fonctionne en production
```

---

## 🔍 Checklist de Vérification Console

Quand vous cliquez "Sauvegarder", vous devez voir dans la console (F12):

### ✅ Logs Attendus (Save)

```javascript
// 1. Avant l'envoi
📤 Envoi de la sauvegarde: { ... }

// 2. Vérification après réponse
✅ Vérification de synchronisation: { 
  sent: {...}, 
  received: {...}, 
  match: true 
}

// 3. Confirmation finale
✅ Données persistées en base de données: { 
  shopId: 1, 
  name: "...", 
  updatedAt: "2024-..." 
}
```

### ✅ Logs Attendus (Load)

```javascript
// 1. Début du chargement
📥 Chargement des données du serveur...

// 2. Réception des données
✅ Customization chargée du serveur: { ... }

// 3. Confirmation de restauration
✅ États restaurés du serveur pour: { 
  shopId: 1, 
  shopName: "...", 
  updatedAt: "..." 
}
```

---

## 🛠️ Debugging

### Si la sauvegarde échoue:

1. **Vérifier la console:**
   ```
   F12 → Console
   Chercher: "❌ Erreur" ou "Erreur lors de la sauvegarde"
   Lire le message d'erreur
   ```

2. **Vérifier Network:**
   ```
   F12 → Network
   Chercher la requête "my-shop"
   Vérifier Status (doit être 200)
   Vérifier Response Body
   ```

3. **Vérifier le token:**
   ```
   F12 → Application
   Local Storage → access_token
   Vérifier qu'il existe et n'est pas vide
   ```

4. **Vérifier le serveur:**
   ```
   Terminal Django
   Vérifier qu'aucune erreur 500 n'apparaît
   ```

### Si le chargement échoue:

1. **Vérifier l'URL:**
   ```
   Doit être: http://localhost:5173/customize-shop
   Avec token valide
   ```

2. **Vérifier la réponse du serveur:**
   ```
   F12 → Network
   GET /shop/api/my-shop/
   Status doit être 200
   Response contient les données
   ```

3. **Vérifier la base de données:**
   ```
   Backend shell:
   >>> Shop.objects.get(id=1).customization
   Doit contenir les données sauvegardées
   ```

---

## 📊 Résumé des Tests

| Test | Objectif | Résultat |
|------|----------|----------|
| 1 | Sauvegarde simple | ✅ Les modifications sont envoyées au serveur |
| 2 | Refresh page | ✅ Les données persistent après refresh |
| 3 | Logout/Login | ✅ Les données persistent après déconnexion |
| 4 | Fermer navigateur | ✅ Les données persistent sans localStorage |
| 5 | Multiple modifications | ✅ Tous les changements sont sauvegardés |
| 6 | Vérifier DB | ✅ Les données sont en base de données |
| 7 | Erreur réseau | ✅ Les erreurs sont gérées correctement |
| 8 | Validation | ✅ Les données sont validées |
| 9 | Synchronisation | ✅ État local = Serveur exactement |
| 10 | E2E complet | ✅ Le système fonctionne en production |

---

## ✅ Critères de Succès

La persistance fonctionne **CORRECTEMENT** si:

- ✅ Les modifications sont sauvegardées en base de données
- ✅ Les données persistent après refresh
- ✅ Les données persistent après logout/login
- ✅ Les données persistent après fermer le navigateur
- ✅ Les logs console affichent les messages attendus
- ✅ Le Network tab affiche les requêtes correctes
- ✅ Aucune erreur ne s'affiche
- ✅ Les données en DB correspondent aux données envoyées

🎉 **Si tous ces tests passent, la persistance est garantie!**
