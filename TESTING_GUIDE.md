# Guide de Test - Boutons et Fonctions

## 🔐 Page d'Authentification

### LoginPage (/login)
- [ ] **Email Input** - Accepte email ou username
- [ ] **Password Input** - Masque le mot de passe par défaut
- [ ] **Show Password Toggle** - Affiche/masque le mot de passe
- [ ] **Remember Me Checkbox** - Sauvegarde la session
- [ ] **Sign In Button** - Vérifie les identifiants via /api/users/token/
- [ ] **Forgot Password Link** - (À implémenter si nécessaire)
- [ ] **Social Login (Google/GitHub)** - (À configurer)
- [ ] **Sign Up Link** - Redirige vers /signup

### SignupPage (/signup)
- [ ] **Name Input** - Accepte texte
- [ ] **Email Input** - Valide format email
- [ ] **Password Input** - Minimum 8 caractères (à vérifier backend)
- [ ] **Confirm Password** - Doit correspondre au mot de passe
- [ ] **Show Password Toggle** - Affiche/masque
- [ ] **Create Account Button** - Crée compte via /api/users/register/
- [ ] **Validation d'erreurs** - Affiche messages appropriés
- [ ] **Login Link** - Redirige vers /login

## 🛍️ Page Boutique (Shop)

### ShopPage (/shop)
- [ ] **Search Bar** - Filtre les produits par nom
- [ ] **Filter Button** - (À implémenter - placeholder)
- [ ] **Cart Button** - Affiche le nombre d'articles
  - [ ] Clique → Redirige vers /checkout
- [ ] **Category Buttons** - Filtre par catégorie
  - [ ] "Tous les produits" - Affiche tous
  - [ ] Autres catégories - Filtre par catégorie
- [ ] **Product Cards**
  - [ ] Image - Clique → Affiche /product/{id}
  - [ ] Nom - Clique → Affiche /product/{id}
  - [ ] Note (stars) - Affiche avis
  - [ ] Prix - Affiche le tarif
  - [ ] Stock - Affiche quantité disponible
  - [ ] Add Button - Ajoute au panier (localStorage)
- [ ] **Loading State** - Affiche spinner durant chargement
- [ ] **Empty State** - Message si aucun produit
- [ ] **Sticky Search** - Reste visible en scrollant

### ProductDetailsPage (/product/:id)
- [ ] **Image Gallery**
  - [ ] Image principale - Affiche produit
  - [ ] Thumbnails - Permettent de changer image
- [ ] **Product Info**
  - [ ] Nom produit
  - [ ] Catégorie badge
  - [ ] Prix - Affiche en grand
  - [ ] Prix barré (original) - Si applicable
  - [ ] Stock status - Disponible/Rupture
- [ ] **Rating**
  - [ ] Stars - Basé sur avis
  - [ ] Nombre d'avis
- [ ] **Quantity Controls**
  - [ ] Minus Button - Réduit de 1
  - [ ] Input field - Accepte nombre
  - [ ] Plus Button - Augmente de 1
- [ ] **Add to Cart Button** - Ajoute au panier
- [ ] **Wishlist Button** - (À implémenter)
- [ ] **Share Button** - (À implémenter)
- [ ] **Reviews Section**
  - [ ] Liste des avis
  - [ ] Stars par avis
  - [ ] Commentaires
  - [ ] Date de publication

## 🛒 Page Panier (Checkout)

### CheckoutPage (/checkout)
- [ ] **Cart Items Display**
  - [ ] Image produit
  - [ ] Nom produit
  - [ ] Prix unitaire et quantité
  - [ ] Total par article
  - [ ] Minus/Plus Buttons - Modifie quantité
  - [ ] Delete Button - Supprime du panier
- [ ] **Shipping Form**
  - [ ] Firstname Input
  - [ ] Lastname Input
  - [ ] Email Input
  - [ ] Phone Input
  - [ ] Address Input
  - [ ] Postal Code Input
  - [ ] City Input
  - [ ] Country Input
- [ ] **Order Summary**
  - [ ] Sous-total - Calcul correct
  - [ ] TVA (20%) - Calcul correct
  - [ ] Livraison - "Gratuit"
  - [ ] Total - Calcul correct (sous-total + TVA)
- [ ] **Confirm Order Button**
  - [ ] Valide formulaire
  - [ ] POST /api/orders/
  - [ ] Redirige vers /order-confirmation/{id}
- [ ] **Continue Shopping Button** - Redirige vers /shop

### OrderConfirmationPage (/order-confirmation/:id)
- [ ] **Success Message** - Affiche "Commande confirmée"
- [ ] **Order Number** - Affiche ID commande
- [ ] **Order Status** - Affiche statut
- [ ] **Order Statistics**
  - [ ] Nombre d'articles
  - [ ] Date création
  - [ ] Total
- [ ] **Order Items List** - Récapitulatif détaillé
- [ ] **Shipping Address** - Affiche adresse de livraison
- [ ] **Continue Shopping Button** - Redirige /shop
- [ ] **View Orders Button** - Redirige /dashboard

## 👤 Profil Utilisateur

### ProfilePage (/profile)
- [ ] **Avatar Display** - Affiche initiales/photo
- [ ] **Change Photo Button** - (À implémenter)
- [ ] **Edit Button** - Passe en mode édition
- [ ] **Personal Info Section**
  - [ ] Firstname field
  - [ ] Lastname field
  - [ ] Email field
  - [ ] Phone field
  - [ ] Address field
  - [ ] City field
  - [ ] Country field
  - [ ] Bio textarea
- [ ] **Shop Section**
  - [ ] Shop Name field
  - [ ] Shop URL field
- [ ] **Save Button** - PATCH /api/users/profile/
- [ ] **Cancel Button** - Abandonne édition

## 📊 Tableau de Bord

### DashboardPage (/dashboard)
- [ ] **Welcome Message** - Affiche "Bienvenue, {nom}"
- [ ] **Stats Cards**
  - [ ] Total Sales - Affiche montant
  - [ ] Orders - Affiche nombre
  - [ ] Customers - Affiche nombre
  - [ ] Products - Affiche nombre
  - [ ] Trend arrows - ↑ ou ↓
- [ ] **Recent Orders Table**
  - [ ] Order ID clickable
  - [ ] Customer name
  - [ ] Amount
  - [ ] Status badge
  - [ ] Date/time
- [ ] **Top Products Section**
  - [ ] Product rank (1-4)
  - [ ] Product name
  - [ ] Sales count
  - [ ] Revenue

## 🏠 Pages Générales

### HomePage (/)
- [ ] **Hero Section** - Affiche call-to-action
- [ ] **Features Section** - Affiche avantages
- [ ] **Testimonials** - Affiche témoignages (si données)
- [ ] **CTA Buttons** - Redirigent vers /shop ou /signup
- [ ] **Pricing** - Affiche plans (si applicable)
- [ ] **Navigation Links**
  - [ ] Home
  - [ ] Shop
  - [ ] Pricing
  - [ ] Templates
  - [ ] Dashboard
  - [ ] Profile
  - [ ] Support

### PricingPage (/pricing)
- [ ] **Price Cards** - Affiche plans
- [ ] **Features List** - Par plan
- [ ] **Select Button** - (À implémenter)

### TemplatesPage (/templates)
- [ ] **Template Grid** - Affiche templates
- [ ] **Preview Button** - (À implémenter)

### SupportPage (/support)
- [ ] **FAQ Section** - Accordéons
- [ ] **Contact Form** - (À implémenter)

## 🔧 Fonctionnalités de Base

### Navigation
- [ ] **Header** - Visible sur toutes les pages
- [ ] **Logo** - Clique → /
- [ ] **Navigation Menu**
  - [ ] Links appropriés selon authentification
  - [ ] Responsive mobile menu
- [ ] **User Menu** - Si connecté
  - [ ] Profil
  - [ ] Dashboard
  - [ ] Logout
- [ ] **Footer** - Visible sur toutes les pages
  - [ ] Links de base
  - [ ] Réseaux sociaux (si configurés)

### Notifications
- [ ] **Toast Notifications** - Affiche succès/erreurs
  - [ ] Login success ✓
  - [ ] Cart item added ✓
  - [ ] Order confirmed ✓
  - [ ] Error messages ✓

### Authentication State
- [ ] **Token Storage** - localStorage
  - [ ] access_token sauvegardé
  - [ ] refresh_token sauvegardé
- [ ] **Auto-login** - Restaure session
- [ ] **Logout** - Nettoie tokens et redirige /

## 📝 Checklist de Test Complète

- [ ] Toutes les routes marchent
- [ ] Tous les endpoints répondent correctement
- [ ] Les images chargent
- [ ] Les calculs sont corrects
- [ ] Les messages d'erreur sont clairs
- [ ] L'UX est cohérente
- [ ] Responsive design fonctionne
- [ ] Dark mode fonctionne (si implémenté)
- [ ] Pas d'erreurs console
- [ ] Performance acceptable

## 🐛 Bugs Connus à Corriger

1. **Images de produits** - Vérifier les chemins/URLs
2. **Validation formulaires** - Ajouter côté frontend
3. **Gestion des erreurs réseau** - Améliorer les messages
4. **Cache produits** - Implémenter pour performance
5. **Pagination** - Ajouter si > 50 produits

---

**Dernière mise à jour**: Décembre 2025
