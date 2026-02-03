# 💾 Système de Sauvegarde - Store Customization

## 📋 Vue d'ensemble

Le système de sauvegarde des customizations a été amélioré pour garantir que:
- ✅ Toutes les modifications sont correctement envoyées au backend
- ✅ Les anciennes valeurs sont remplacées par les nouvelles
- ✅ Les données sont persistées en base de données
- ✅ La réponse du serveur est vérifiée et traitée
- ✅ Les messages d'erreur sont affichés clairement

## 🔄 Flux de Sauvegarde

### 1. Préparation des données
```typescript
const customizationData = {
  primaryColor,      // ex: "#0077FF"
  secondaryColor,    // ex: "#5AC8FA"
  accentColor,       // ex: "#FFD43B"
  fontFamily,        // ex: "Inter"
  headingFont,       // ex: "Poppins"
  layoutStyle,       // ex: "modern"
  headerStyle,       // ex: "sticky"
  footerColumns,     // ex: "4"
  gridColumns,       // ex: "3"
  imageRatio,        // ex: "1:1"
  borderRadius,      // ex: "12"
  shadows,           // ex: "medium"
  spacing,           // ex: "comfortable"
  features: {        // Options activées/désactivées
    search: true,
    filters: true,
    wishlist: true,
    quickView: true,
    reviews: true,
    newsletter: true,
  }
};
```

### 2. Envoi au serveur
```typescript
PATCH /shop/api/my-shop/
Headers:
  Content-Type: application/json
  Authorization: Bearer {token}

Body:
{
  name: "Ma Boutique",
  description: "Description de la boutique",
  customization: customizationData
}
```

### 3. Traitement de la réponse
```typescript
if (!res.ok) {
  // Erreur: afficher le message d'erreur du serveur
  const errorData = await res.json();
  throw new Error(errorData.detail || 'Erreur lors de la sauvegarde');
}

// Succès: mettre à jour l'état du shop
const updatedData = await res.json();
setShop(updatedData);

// Afficher le message de succès
toast.success('✅ Customization sauvegardée avec succès!');

// Enregistrer dans la console pour debug
console.log('✅ Données sauvegardées:', {
  name,
  description,
  customization: customizationData
});

// Rediriger après 1.5 secondes
setTimeout(() => onBack(), 1500);
```

## 🔍 Garanties de Persistance

### Garantie 1: Vérification de la réponse
```typescript
if (!res.ok) {
  throw new Error('Erreur lors de la sauvegarde');
}
```
**But:** S'assurer que la requête a réussi avant de considérer les données comme sauvegardées.

### Garantie 2: Mise à jour de l'état local
```typescript
const updatedData = await res.json();
setShop(updatedData);
```
**But:** Mettre à jour le shop local avec les données renvoyées par le serveur pour garantir la synchronisation.

### Garantie 3: Messages de confirmation
```typescript
toast.success('✅ Customization sauvegardée avec succès!');
console.log('✅ Données sauvegardées:', { ... });
```
**But:** Informer l'utilisateur que la sauvegarde a réussi et enregistrer les données pour le debugging.

### Garantie 4: Gestion des erreurs
```typescript
catch (err: any) {
  console.error('Erreur sauvegarde:', err);
  toast.error(err?.message || 'Erreur lors de la sauvegarde');
}
```
**But:** Capturer et afficher les erreurs à l'utilisateur.

## 📝 Processus de Remplacement des Valeurs

### Avant (valeurs anciennes)
```json
{
  "customization": {
    "primaryColor": "#FF0000",
    "fontFamily": "Arial"
  }
}
```

### Après clic sur "Sauvegarder"
```
L'utilisateur modifie:
- primaryColor: "#FF0000" → "#0077FF"
- fontFamily: "Arial" → "Inter"
```

### Lors de la sauvegarde
```typescript
// Les nouvelles valeurs sont envoyées au serveur
{
  "customization": {
    "primaryColor": "#0077FF",      // ← NOUVELLE valeur
    "fontFamily": "Inter"           // ← NOUVELLE valeur
  }
}
```

### Backend remplace les anciennes valeurs
```
Le serveur Django reçoit la requête PATCH et:
1. Charge le shop existant
2. Remplace les valeurs de customization avec les nouvelles
3. Sauvegarde en base de données
4. Renvoie le shop mis à jour
```

### Frontend met à jour l'état
```typescript
// La réponse du serveur est reçue et met à jour l'état
const updatedData = await res.json();
setShop(updatedData);  // ← Les anciennes valeurs sont maintenant remplacées
```

## ✅ Checklist de Vérification

Quand vous cliquez sur "Sauvegarder":

- [ ] Les données modifiées sont préparées correctement
- [ ] La requête PATCH est envoyée au serveur
- [ ] Le serveur répond avec un statut 200/204
- [ ] L'état du shop est mis à jour avec `setShop(updatedData)`
- [ ] Le toast affiche "✅ Customization sauvegardée avec succès!"
- [ ] La console affiche les données sauvegardées
- [ ] Après 1.5 secondes, vous êtes redirigé vers `/my-shop`
- [ ] Au retour sur la page de customization, les nouvelles valeurs s'affichent

## 🔧 Debugging

Si la sauvegarde ne fonctionne pas:

### 1. Vérifier la console du navigateur
```
Chercher: "✅ Données sauvegardées:" et "Erreur sauvegarde:"
```

### 2. Vérifier la requête réseau (DevTools → Network)
```
Requête: PATCH /shop/api/my-shop/
Status: 200 ou 204 (succès)
Body: Vérifier que les données sont correctes
Response: Vérifier que le serveur retourne les données mises à jour
```

### 3. Vérifier le backend
```
Log Django: Voir si la requête PATCH est reçue
Base de données: Vérifier que les modifications sont persistées
```

## 📱 API Endpoint

### Endpoint
```
PATCH /shop/api/my-shop/
```

### Headers
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

### Request Body
```json
{
  "name": "string",
  "description": "string",
  "customization": {
    "primaryColor": "string",
    "secondaryColor": "string",
    "accentColor": "string",
    "fontFamily": "string",
    "headingFont": "string",
    "layoutStyle": "string",
    "headerStyle": "string",
    "footerColumns": "string",
    "gridColumns": "string",
    "imageRatio": "string",
    "borderRadius": "string",
    "shadows": "string",
    "spacing": "string",
    "features": {
      "search": boolean,
      "filters": boolean,
      "wishlist": boolean,
      "quickView": boolean,
      "reviews": boolean,
      "newsletter": boolean
    }
  }
}
```

### Response (Succès)
```json
{
  "id": 1,
  "name": "Ma Boutique",
  "description": "Description",
  "customization": {
    "primaryColor": "#0077FF",
    ...
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:30:00Z"
}
```

### Response (Erreur)
```json
{
  "detail": "Message d'erreur du serveur"
}
```

## 🎯 Résumé

La sauvegarde fonctionne maintenant en 4 étapes:

1. **Préparation** → Tous les états (couleurs, fonts, layout, etc.) sont collectés
2. **Envoi** → Une requête PATCH est envoyée au serveur avec les nouvelles valeurs
3. **Traitement Backend** → Le serveur remplace les anciennes valeurs dans la base de données
4. **Confirmation Frontend** → L'état local est mis à jour avec la réponse du serveur

**Résultat:** Les anciennes valeurs sont complètement remplacées par les nouvelles ✅
