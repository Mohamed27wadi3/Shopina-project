# 🔄 Workflow Complet - Sauvegarde des Customizations

## 📊 Diagramme du Flux

```
┌─────────────────────────────────────────────────────────────┐
│  UTILISATEUR MODIFIE LES CUSTOMIZATIONS                      │
│  (Couleurs, Fonts, Layout, etc.)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  CLIC SUR "SAUVEGARDER"                                      │
│  → handleSave() est appelée                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  PRÉPARATION DES DONNÉES                                     │
│  ├─ name: "Ma Boutique"                                      │
│  ├─ description: "Description"                              │
│  └─ customization: {                                         │
│      primaryColor: "#0077FF" (NOUVELLE)                     │
│      secondaryColor: "#5AC8FA"                              │
│      ... (tous les états)                                    │
│    }                                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  ENVOI DE LA REQUÊTE                                         │
│  PATCH /shop/api/my-shop/                                    │
│  Headers:                                                    │
│    Content-Type: application/json                           │
│    Authorization: Bearer {token}                            │
│  Body: { name, description, customization }                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  SERVEUR REÇOIT LA REQUÊTE                                   │
│  Django Backend:                                             │
│  ├─ Récupère le shop existant                               │
│  ├─ Remplace les anciennes valeurs                          │
│  ├─ Valide les données                                       │
│  ├─ Sauvegarde en base de données                           │
│  └─ Retourne le shop mis à jour                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  VÉRIFICATION DE LA RÉPONSE                                  │
│  if (!res.ok)                                                │
│  ├─ Afficher: ❌ Toast d'erreur                              │
│  ├─ Log: Erreur dans la console                             │
│  └─ Rester: Sur la page de customization                    │
│  else                                                        │
│  ├─ Mettre à jour: setShop(updatedData)                     │
│  ├─ Afficher: ✅ Toast de succès                             │
│  ├─ Log: Données sauvegardées                               │
│  └─ Rediriger: Vers /my-shop après 1.5s                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  CONFIRMATION À L'UTILISATEUR                                │
│  ✅ "Customization sauvegardée avec succès!"                │
│  → Redirection vers le dashboard                            │
└─────────────────────────────────────────────────────────────┘
```

## 💻 Code Détaillé

### Étape 1: Clic sur Sauvegarder
```typescript
<Button
  onClick={handleSave}
  disabled={saving}
  className="bg-gradient-to-r from-[#0077FF]..."
>
  {saving ? (
    <>
      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
      Sauvegarde...
    </>
  ) : (
    <>
      <Save className="w-4 h-4 mr-2" />
      Sauvegarder
    </>
  )}
</Button>
```

### Étape 2: Fonction handleSave()
```typescript
const handleSave = async () => {
  // 1. Vérification du shop
  if (!shop) return;
  
  // 2. Début du chargement
  setSaving(true);
  
  try {
    // 3. Récupération du token
    const token = localStorage.getItem('access_token');
    
    // 4. Préparation des données
    const customizationData = {
      primaryColor,        // Ex: "#0077FF"
      secondaryColor,      // Ex: "#5AC8FA"
      accentColor,         // Ex: "#FFD43B"
      // ... tous les autres états
      features: {
        search: true,
        filters: true,
        // ...
      },
    };

    // 5. Envoi au serveur
    const res = await fetch(`${API_BASE}/shop/api/my-shop/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({
        name,
        description,
        customization: customizationData,
      }),
      credentials: 'include',
    });

    // 6. Vérification de la réponse
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || 'Erreur lors de la sauvegarde');
    }

    // 7. Mise à jour de l'état avec la réponse du serveur
    const updatedData = await res.json();
    setShop(updatedData);  // ← LES ANCIENNES VALEURS SONT REMPLACÉES
    
    // 8. Confirmation à l'utilisateur
    toast.success('✅ Customization sauvegardée avec succès!');
    
    // 9. Logging pour le debugging
    console.log('✅ Données sauvegardées:', {
      name,
      description,
      customization: customizationData
    });
    
    // 10. Redirection après 1.5 secondes
    setTimeout(() => onBack(), 1500);
    
  } catch (err: any) {
    console.error('Erreur sauvegarde:', err);
    toast.error(err?.message || 'Erreur lors de la sauvegarde');
  } finally {
    setSaving(false);
  }
};
```

## 🎯 Points Clés de la Sauvegarde

### ✅ Les Nouvelles Valeurs Remplacent les Anciennes

Avant la sauvegarde (état local):
```
primaryColor: "#FF0000"  (ancienne)
```

Après modification par l'utilisateur:
```
primaryColor: "#0077FF"  (nouvelle)
```

Lors du clic "Sauvegarder":
```typescript
// Les NOUVELLES valeurs sont envoyées au serveur
customizationData = {
  primaryColor: "#0077FF",  // ← NOUVELLE valeur
  // ...
}
```

Le serveur remplace:
```
SELECT shop WHERE id=1
  ├─ customization.primaryColor = "#0077FF"  ← REMPLACÉE
  ├─ customization.secondaryColor = "#5AC8FA"
  └─ ... autres customizations
UPDATE shop SET customization = { ... }
SAVE TO DATABASE
```

Frontend met à jour:
```typescript
const updatedData = await res.json();
setShop(updatedData);  // ← État local = nouvelles valeurs du serveur
```

### ✅ Synchronisation Frontend-Backend

```
FRONTEND (Local)           BACKEND (Database)
═════════════════════     ══════════════════════
primaryColor: "#FF0000"   primaryColor: "#FF0000"
                                  │
                          [Utilisateur change]
                                  │
primaryColor: "#0077FF"   primaryColor: "#FF0000"
[État local changé]       [Base de données inchangée]
                                  │
            [Clic "Sauvegarder"]   │
                                  │
                    [PATCH request]│
                                  ▼
primaryColor: "#0077FF"   primaryColor: "#0077FF"
[État local]              [Base de données mise à jour]
                                  │
                    [Réponse avec données mises à jour]
                                  │
                    [setShop(updatedData)]
                                  │
                                  ▼
primaryColor: "#0077FF"   primaryColor: "#0077FF"
[État local = nouvelles]  [Base de données = nouvelles]
```

## 🔍 Vérification de la Sauvegarde

### Dans la Console du Navigateur (F12)

Après clic "Sauvegarder":

✅ **Message de succès:**
```
✅ Données sauvegardées: {
  name: "Ma Boutique",
  description: "...",
  customization: {
    primaryColor: "#0077FF",
    ...
  }
}
```

❌ **Message d'erreur (si problème):**
```
Erreur sauvegarde: Error: Erreur lors de la sauvegarde
```

### Dans l'onglet Network (DevTools)

Chercher la requête `my-shop`:

```
Method: PATCH
Status: 200 (succès) ou 4xx/5xx (erreur)
Request Body: Les nouvelles valeurs
Response: {
  "id": 1,
  "name": "Ma Boutique",
  "customization": { ... },
  "updated_at": "2024-...(date/heure actuelle)"
}
```

## 🚀 Test Complet

### Scénario de Test

1. **Accéder à la page**
   ```
   http://localhost:5173/customize-shop
   ```

2. **Modifier une valeur**
   ```
   Changer Primary Color: #0077FF → #FF0000
   ```

3. **Cliquer "Sauvegarder"**
   ```
   Button "Sauvegarder" cliqué
   ```

4. **Vérifier la console**
   ```
   F12 → Console
   Voir: "✅ Données sauvegardées: ..."
   ```

5. **Vérifier Network**
   ```
   F12 → Network
   Chercher: "my-shop" (PATCH)
   Status: 200
   ```

6. **Vérifier la redirection**
   ```
   Après 1.5s → http://localhost:5173/my-shop
   ```

7. **Retour à la page de customization**
   ```
   Cliquer "Personnaliser"
   Vérifier: Primary Color = #FF0000 (nouvelle valeur)
   ```

## ✅ Résumé

**La sauvegarde fonctionne quand:**

✅ Les données modifiées sont correctement collectées  
✅ La requête PATCH est envoyée au serveur  
✅ Le serveur répond avec le shop mis à jour  
✅ L'état local est synchronisé avec la réponse du serveur  
✅ L'utilisateur voit le message de succès  
✅ La redirection se fait vers le dashboard  
✅ Au retour, les nouvelles valeurs s'affichent  

**Les anciennes valeurs sont remplacées quand:**

1. L'utilisateur modifie une valeur
2. Clique sur "Sauvegarder"
3. Le serveur reçoit et valide les données
4. La base de données est mise à jour
5. Le frontend reçoit la réponse avec les données mises à jour
6. `setShop(updatedData)` remplace l'état local complet
