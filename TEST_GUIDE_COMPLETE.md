# 🧪 Guide de Test Complet - Workflow Boutique Personnalisée

## ✅ Statut: PRÊT À TESTER

Tous les systèmes sont en place pour que le workflow complet fonctionne de bout en bout.

---

## 🔧 Pré-requis

1. **Backend en cours d'exécution:**
   ```bash
   cd "d:\Shopina Project\code source\shopina-env\backend"
   python manage.py runserver
   ```

2. **Frontend en cours d'exécution:**
   ```bash
   cd "d:\Shopina Project\code source\front"
   npm run dev
   ```

3. **URL Frontend:** `http://localhost:3001` (ou `http://localhost:3000`)

---

## 📝 Scénario de Test Étape par Étape

### **Étape 1: Créer un Compte**

1. Allez à `http://localhost:3001/register`
2. Remplissez:
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `SecurePass123!`
   - Confirm Password: `SecurePass123!`
3. Cliquez "S'inscrire"
4. ✅ Devriez être redirigé au dashboard

**Attendus:**
- ✅ Compte créé dans la base de données
- ✅ Tokens sauvegardés dans `localStorage`
- ✅ Redirect vers `/dashboard`

---

### **Étape 2: Créer une Boutique**

1. Vous êtes redirigé automatiquement vers `/create-shop`
2. Remplissez:
   - Shop Name: `Ma Boutique Premium`
   - Description: `Une boutique de produits premium`
   - Email: `shop@example.com`
   - Phone: `+33612345678`
3. Cliquez "Créer la boutique"
4. ✅ Devriez être redirigé au dashboard de la boutique

**Attendus:**
- ✅ Boutique créée dans la base de données
- ✅ `Shop` avec `owner = request.user`
- ✅ Slug généré: `ma-boutique-premium`
- ✅ Redirect vers `/shop/ma-boutique-premium/dashboard/`

**Vérification Backend:**
```bash
# Dans Django shell
Shop.objects.filter(owner__username='testuser').first()
# Devrait retourner: <Shop: Ma Boutique Premium>
```

---

### **Étape 3: Accéder au Templates**

1. Allez à `http://localhost:3001/templates`
2. Vous devriez voir **7 templates:**
   - Modern Blue
   - Eco Green
   - Food Delight
   - Sports Active
   - Beauty Glow
   - Et d'autres...

3. Chaque template affiche:
   - ✅ Aperçu visuel
   - ✅ Bouton "Preview"
   - ✅ Bouton "Variants"
   - ✅ Bouton "Customize"

**Attendus:**
- ✅ Tous les templates chargent correctement
- ✅ Images preview s'affichent
- ✅ Boutons cliquables

---

### **Étape 4: Personnaliser le Template**

1. Cliquez sur "Customize" d'un template (par ex. "Modern Blue")
2. ✅ Redirect vers `/templates/template-1/customize`

#### **Page de Customization - Navbar (Vérifier dimensions)**

La navbar en haut devrait avoir 2 lignes:
- **Ligne 1:** 
  - ✅ Back button (icône)
  - ✅ "Customize Modern Blue" (titre)
  - ✅ "Advanced customization options" (sous-titre)
  
- **Ligne 2:**
  - ✅ "Preview:" avec sélecteur Device (Desktop/Tablet/Mobile)
  - ✅ Boutons d'action: Reset, Draft, Apply
  - ✅ Responsive: icônes sans texte sur mobile

#### **4 Onglets de Customization**

1. **Branding Tab (Palette icon)**
   - ✅ Shop Name input: `Ma Boutique Premium`
   - ✅ Logo Upload button
   - ✅ Featured Products preview avec 6 produits réels

2. **Design Tab (Palette icon)**
   - ✅ Color Palettes: ~3 options
   - ✅ Custom Color Picker:
     - Primary color picker + hex input
     - Secondary color picker + hex input
     - Accent color picker + hex input
   - ✅ Typography: 4 styles disponibles
   - ✅ Preview met à jour en temps réel

3. **Layout Tab (Layout icon)**
   - ✅ Main Layout: 3 variantes
   - ✅ Header Style: minimal/standard/sticky
   - ✅ Product Grid Columns: 2-4 (slider)
   - ✅ Image Ratio: 1:1, 4:3, 16:9
   - ✅ Footer Columns: 2-5 (slider)

4. **Features Tab (Settings icon)**
   - ✅ Search toggle
   - ✅ Filters toggle
   - ✅ Badges toggle
   - ✅ Wishlist toggle
   - ✅ Quick View toggle

#### **Live Preview**

- ✅ Desktop view (pleine largeur)
- ✅ Tablet view (max-width 768px)
- ✅ Mobile view (max-width 384px)

**Prévu dans l'aperçu:**
- ✅ Hero section avec couleurs personnalisées
- ✅ Produits du store avec images réelles
- ✅ Header avec le nom de la boutique
- ✅ Footer avec les 4 colonnes (Shop, About, Help, Follow)

---

### **Étape 5: Modifier les Paramètres**

1. **Changer la couleur primaire:**
   - Cliquez sur le color picker "Primary"
   - Changez à une couleur différente (ex: rouge #FF0000)
   - ✅ L'aperçu met à jour en temps réel

2. **Changer le style de header:**
   - Sélectionnez "minimal" au lieu de "sticky"
   - ✅ L'aperçu met à jour

3. **Changer les colonnes de produits:**
   - Ajustez le slider "Product Grid Columns" à 2 ou 4
   - ✅ La grille de produits s'ajuste

---

### **Étape 6: Tester les Boutons**

#### **Reset All Button**
1. Cliquez "Reset" (haut droit)
2. ✅ Confirmation dialog: "Reset all changes? This cannot be undone."
3. Confirmez "OK"
4. ✅ Tous les paramètres reviennent aux valeurs par défaut
5. ✅ Notification verte: "All changes reset!"

#### **Save Draft Button**
1. Personnalisez quelques paramètres
2. Cliquez "Save Draft" (haut droit)
3. ✅ Notification verte: "Draft saved successfully!"
4. ✅ Bouton a icône Loader animée pendant l'appel API

**Vérification Backend:**
```bash
# Dans Django shell
from shops.models import ShopTheme
ShopTheme.objects.filter(shop__slug='ma-boutique-premium').first()
# Devrait retourner: <ShopTheme: Theme for ma-boutique-premium (template template-1)>
# Vérifier: theme.options contient la customization sauvegardée
```

#### **Apply to Shop Button**
1. Personnalisez quelques paramètres
2. Cliquez "Apply" (haut droit)
3. ✅ Notification verte: "Template applied to your shop successfully!"
4. ✅ Bouton a icône Loader animée pendant l'appel API
5. ✅ Après 2 secondes: Redirect vers `/dashboard`

**Vérification Backend:**
```bash
# Dans Django shell
shop = Shop.objects.get(slug='ma-boutique-premium')
shop.theme.options  # Contient la customization appliquée
shop.theme.is_active  # True
```

---

### **Étape 7: Accéder au Store Public**

1. Allez à `http://localhost:3001/shop/ma-boutique-premium`
2. ✅ La page s'affiche avec:
   - Titre: "Ma Boutique Premium"
   - Description: "Une boutique de produits premium"
   - Couleurs personnalisées appliquées (si utilisé dans le hero)
   - Liste de produits

#### **Vérification de la Personnalisation Appliquée**

- ✅ **Hero Section:**
  - Couleur primaire personnalisée utilisée (gradient)
  - Layout du hero s'affiche correctement

- ✅ **Produits:**
  - 12 produits réels avec images Unsplash
  - Affichage correct des prix, ratings, badges
  - Quick Add button fonctionnel

- ✅ **Footer:**
  - 4 colonnes: Shop, About, Help, Follow
  - Chaque colonne avec 3 liens

- ✅ **Responsive:**
  - Desktop: Layout normal
  - Tablet: Colonnes réduites
  - Mobile: Layout mobile optimisé

---

### **Étape 8: Retourner et Re-Personnaliser**

1. Allez à `http://localhost:3001/templates`
2. Cliquez "Customize" d'un autre template (ex. "Eco Green")
3. Changez les paramètres
4. Cliquez "Apply to Shop"
5. Allez à `http://localhost:3001/shop/ma-boutique-premium`
6. ✅ La page affiche le nouveau template personnalisé

---

## 🔍 Points de Vérification

### **Frontend:**
- ✅ Navbar dimensions correctes (2 lignes, responsive)
- ✅ Tous les 4 onglets accessibles et fonctionnels
- ✅ Live preview met à jour en temps réel
- ✅ Notification toasts affichent les messages
- ✅ Boutons disabled pendant les appels API
- ✅ Icônes Loader animées pendant le loading
- ✅ Redirection correcte après Apply

### **Backend API Calls:**

1. **POST /api/shop/theme/** (Save Draft)
   ```
   Status: 200 OK
   Body: {
     "message": "Theme saved",
     "template_id": "template-1",
     "options": {...},
     "updated_at": "2026-02-03T..."
   }
   ```

2. **POST /api/shop/theme/** (Apply)
   ```
   Status: 200 OK
   Body: {
     "message": "Theme saved",
     "template_id": "template-1",
     "options": {...},
     "updated_at": "2026-02-03T..."
   }
   ```

3. **GET /shop/api/public/ma-boutique-premium/**
   ```
   Status: 200 OK
   Body: {
     "id": 1,
     "name": "Ma Boutique Premium",
     "slug": "ma-boutique-premium",
     "theme": {
       "template_id": "template-1",
       "options": {...},
       "is_active": true,
       "updated_at": "..."
     },
     ...
   }
   ```

---

## 🐛 Troubleshooting

| Problème | Cause | Solution |
|----------|-------|----------|
| Navbar trop grande | CSS padding/hauteur | Vérifier `py-2.5` et `px-6` |
| Couleurs non appliquées | Thème pas chargé | Vérifier `applyThemeStyles()` appelée |
| Notification pas visible | Z-index | Vérifier `z-[100]` sur toast |
| Bouton désactivé après Apply | Navigation trop rapide | Augmenter délai avant redirect |
| Produits pas affichés | API error | Vérifier `/shop/api/public/:slug/products/` |
| Erreur 404 sur shop public | Shop slug incorrect | Vérifier slug généré lors de création |

---

## ✅ Checklist Finale

- [ ] Compte créé avec succès
- [ ] Boutique créée avec succès
- [ ] Templates page charge tous les templates
- [ ] Customization page affiche les 4 onglets
- [ ] Navbar dimensions correctes
- [ ] Live preview fonctionne
- [ ] Reset All réinitialise les paramètres
- [ ] Save Draft sauvegarde en brouillon
- [ ] Apply to Shop applique et redirige
- [ ] Store public affiche la personnalisation
- [ ] Tous les produits s'affichent
- [ ] Responsive design fonctionne sur mobile

---

## 🚀 Status: PRÊT POUR TEST COMPLET

Tous les systèmes de frontend et backend sont en place et testés.
Veuillez suivre ce guide pour tester le workflow complet.
