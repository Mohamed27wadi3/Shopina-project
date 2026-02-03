# 🧪 Guide de Test - My Store Navigation

## 🚀 Démarrage rapide

### 1. Vérifier que les serveurs tournent
```bash
# Terminal 1: Frontend
cd "d:\Shopina Project\code source\front"
npm run dev
# → http://localhost:3001

# Terminal 2: Backend (si nécessaire)
cd "d:\Shopina Project\code source\shopina-env\backend"
.\.venv\Scripts\Activate.ps1
python manage.py runserver
# → http://127.0.0.1:8000
```

### 2. Ouvrir le navigateur
- Frontend: http://localhost:3001
- Backend: http://127.0.0.1:8000

---

## 🧑‍🔬 Scénarios de test

### TEST 1️⃣: Utilisateur NEW (Sans boutique)

#### Étapes:
1. ✅ Créer un compte utilisateur
   - Email: `test_no_store@example.com`
   - Password: `TestPass123!`
   - Signup complet

2. ✅ Être redirigé au Dashboard
   - Vérifier authentification OK

3. ✅ Clicker sur "My Store" dans la navbar
   - Vérifier navigation vers `/my-shop`

4. ✅ Vérifier l'empty state affiche
   - [ ] Titre: "Pas encore de boutique ?"
   - [ ] Illustration ShoppingBag animée
   - [ ] Description visible
   - [ ] Bouton primaire: "Créer ma boutique"
   - [ ] Bouton secondaire: "Découvrir les templates"
   - [ ] 4 cartes de bénéfices visibles
   - [ ] Section "3 étapes" visible
   - [ ] CTA en bas: "Créer ma boutique maintenant"

5. ✅ Clicker "Créer ma boutique" (primary button)
   - [ ] Modal de création s'ouvre
   - [ ] Formulaire visible
   - [ ] Champs: Nom, Description, Email, Téléphone
   - [ ] X de fermeture en haut-droit

6. ✅ Remplir le formulaire
   - Nom: `Ma Boutique Test`
   - Description: `Description test complète`
   - Email: `test_no_store@example.com`
   - Téléphone: `0600000000`

7. ✅ Clicker "Créer ma boutique"
   - [ ] Bouton devient "Création…"
   - [ ] Spinner visible
   - [ ] Bouton disabled

8. ✅ Attendre la réponse API
   - [ ] Toast vert: "🎊 Boutique créée avec succès !"
   - [ ] Modal se ferme
   - [ ] Page recharge

9. ✅ Vérifier le dashboard affiche
   - [ ] Hero section avec "Ma Boutique Test"
   - [ ] Performance panel visible
   - [ ] Boutons d'action: Voir la boutique, Commandes, etc.
   - [ ] 4 stat cards visibles
   - [ ] Section produits vide (avec message)
   - [ ] Formulaire d'ajout de produit

#### ✅ Résultat attendu:
- Empty state → Modale → Toast → Dashboard
- **PASS**: ✅ Tous les états affichés correctement

---

### TEST 2️⃣: Utilisateur EXISTANT (Avec boutique)

#### Étapes:
1. ✅ Créer un compte utilisateur
   - Email: `test_with_store@example.com`
   - Password: `TestPass123!`
   - Signup complet

2. ✅ Créer une boutique (test 1 ou via API directe)
   - Nom: `Ma Boutique Existante`
   - Description: `Description de test`

3. ✅ Recharger la page et aller à `/my-shop`
   - Dashboard doit s'afficher directement

4. ✅ Vérifier tous les éléments du dashboard
   - [ ] Hero section: Nom boutique + description
   - [ ] Badge "Boutique active"
   - [ ] Performance panel avec stats
   - [ ] 4 boutons d'action
   - [ ] 4 stat cards
   - [ ] Section produits (vide au départ)
   - [ ] Formulaire d'ajout produit
   - [ ] Sélecteur de template (3 templates)

5. ✅ Tester les boutons d'action
   - [ ] "Voir la boutique" → `/shop/{slug}`
   - [ ] "Commandes" → `/orders`
   - [ ] "Paramètres boutique" → `/shop/settings`
   - [ ] "Ajouter un produit" → Scroll jusqu'au formulaire

6. ✅ Ajouter un produit
   - Nom: `Hoodie Test`
   - Prix: `5000`
   - Catégorie: `Vêtement`
   - Description: `Un beau hoodie`
   - Image: (uploader une image)
   - Clicker "Publier le produit"
   - [ ] Toast de succès
   - [ ] Produit apparaît dans la liste
   - [ ] Stats "Produits actifs" = 1

7. ✅ Éditer le produit
   - Clicker "Éditer"
   - [ ] Modal d'édition s'ouvre
   - [ ] Champs pré-remplis
   - Modifier le nom: `Hoodie Test V2`
   - Clicker "Sauvegarder"
   - [ ] Toast de succès
   - [ ] Produit mis à jour dans la liste

8. ✅ Supprimer le produit
   - Clicker "Supprimer"
   - [ ] Confirmation dialog
   - Confirmer la suppression
   - [ ] Toast de succès
   - [ ] Produit disparaît
   - [ ] Stats "Produits actifs" = 0

9. ✅ Choisir un template
   - Clicker "Choisir" sur un template
   - [ ] Template devient "Sélectionné"
   - [ ] Toast: "Template appliqué à la boutique"
   - [ ] Changement immédiat

#### ✅ Résultat attendu:
- Dashboard → Tous les éléments fonctionnels
- CRUD produits → OK
- Navigation → OK
- **PASS**: ✅ Dashboard complet et fonctionnel

---

### TEST 3️⃣: Erreurs et edge cases

#### 3a: Erreur de validation
1. Ouvrir le formulaire de création
2. Clicker "Créer" sans remplir "Nom"
   - [ ] Message d'erreur: "Nom requis"
   - [ ] Toast rouge

#### 3b: Erreur réseau
1. Débrancher internet (ou dev tools: offline)
2. Tenter de créer une boutique
   - [ ] Toast rouge: "Erreur réseau"
   - [ ] Modale reste ouverte
   - [ ] Peut réessayer

#### 3c: Annuler la création
1. Ouvrir le formulaire
2. Remplir le formulaire partiellement
3. Clicker "Annuler"
   - [ ] Modal se ferme
   - [ ] Revient à l'empty state
   - [ ] Données NOT sauvegardées

#### 3d: Déconnexion
1. Être authentifié avec boutique
2. Clicker "Logout"
3. Tenter d'accéder `/my-shop`
   - [ ] Redirect vers `/login`
   - [ ] Pas d'accès à My Store

---

### TEST 4️⃣: Responsive Design

#### 4a: Mobile (< 640px)
- Ouvrir sur smartphone/dev tools (375px)
- [ ] Empty state: Single column
- [ ] Modal: Full screen
- [ ] Cards: Stack vertical
- [ ] Images: Responsive
- [ ] Buttons: Full width
- [ ] Pas de scroll horizontal

#### 4b: Tablet (768px)
- Ouvrir sur iPad/dev tools (768px)
- [ ] Empty state: 2 colonnes
- [ ] Modal: Centré
- [ ] Cards: 2 colonnes
- [ ] Layout: Balanced

#### 4c: Desktop (1440px)
- Ouvrir sur desktop/dev tools (1440px)
- [ ] Empty state: Optimal layout
- [ ] Modal: Max-width respected
- [ ] Cards: 4 colonnes
- [ ] Tous les éléments visibles

---

### TEST 5️⃣: Dark Mode

#### 5a: Mode clair (light)
1. Aller à `/my-shop` (no store)
2. Vérifier couleurs light
   - [ ] Fond blanc
   - [ ] Texte noir
   - [ ] Buttons: Bleu

#### 5b: Mode sombre (dark)
1. Activer dark mode (dev settings ou système)
2. Aller à `/my-shop` (no store)
3. Vérifier couleurs dark
   - [ ] Fond sombre (#gray-950)
   - [ ] Texte blanc
   - [ ] Buttons: Cyan visible
   - [ ] Contraste OK (> 4.5:1)

---

### TEST 6️⃣: Performances

#### 6a: Time to Interactive
1. DevTools → Performance tab
2. Charger `/my-shop` (no store)
3. Mesurer TTI (Time to Interactive)
   - Target: < 2s
   - Mesurer: Paint, Largest Contentful Paint (LCP)

#### 6b: Bundle Size
1. DevTools → Network tab
2. Recharger page
3. Vérifier tailles:
   - HTML: < 50KB
   - CSS: < 200KB
   - JS: < 300KB
   - Images: < 100KB
   - Total: < 500KB

---

## 📋 Checklist de test rapide

```
BASIC FLOW
☐ User sans boutique voit empty state
☐ Clicker "Créer" ouvre modal
☐ Remplir formulaire
☐ Créer boutique fonctionne
☐ Dashboard affiche après création
☐ User avec boutique voit dashboard direct

EMPTY STATE
☐ Titre visible
☐ Description visible
☐ CTA primaire: "Créer ma boutique"
☐ CTA secondaire: "Découvrir les templates"
☐ 4 cartes de bénéfices
☐ Section "3 étapes"
☐ Bottom CTA visible

DASHBOARD
☐ Hero section avec shop name
☐ Performance panel
☐ 4 stat cards
☐ Products section
☐ Add product form
☐ Template chooser
☐ All CTA buttons work

MODAL
☐ Ouvre quand on clique "Créer"
☐ Champs: Nom, Description, Email, Phone
☐ X button ferme modal
☐ "Annuler" ferme modal
☐ "Créer" envoie API

RESPONSIVE
☐ Mobile (< 640px) OK
☐ Tablet (640-1024px) OK
☐ Desktop (> 1024px) OK
☐ Pas de horizontal scroll

DARK MODE
☐ Light mode: OK
☐ Dark mode: OK
☐ Contraste: OK

PERFORMANCE
☐ Time to Interactive < 2s
☐ Bundle size < 500KB
☐ No console errors
☐ No memory leaks
```

---

## 🐛 Rapport de bugs

Si vous trouvez un bug:

### Template de rapport:
```
**Titre**: Brève description du bug

**Reproduction**:
1. Étape 1
2. Étape 2
3. Étape 3

**Comportement attendu**: ...

**Comportement actuel**: ...

**Screenshots/Logs**: (si applicable)

**Environnement**:
- Browser: Chrome/Firefox/Safari
- OS: Windows/Mac/Linux
- Responsive: Mobile/Tablet/Desktop
- Mode: Light/Dark
```

### Où rapporter:
- Ouvrir une issue sur GitHub
- Slack channel #bugs
- Email: support@shopina.com

---

## ✅ Test Complete!

Quand tous les tests passent:

1. ✅ Marquer comme "VALIDÉ"
2. ✅ Documenter les résultats
3. ✅ Créer un pull request si applicable
4. ✅ Assigner pour review
5. ✅ Merger vers main
6. ✅ Déployer en production

---

**Version**: 1.0
**Date**: 3 février 2026
**Statut**: Ready for QA

