# ⚡ Quick Checklist - Shopina Integration

## 🚀 AVANT DE TESTER

```bash
# 1. Backend
cd backend
python manage.py runserver 0.0.0.0:8000
✅ http://localhost:8000

# 2. Frontend  
cd front
npm run dev
✅ http://localhost:5173
```

## 🧪 TESTS ESSENTIELS

### 1️⃣ Authentification (5 min)
- [ ] Accédez à `/signup`
- [ ] Créez un compte
- [ ] Vérifiez la redirection `/dashboard`
- [ ] Déconnexion
- [ ] Connexion avec email/username

### 2️⃣ Boutique (5 min)
- [ ] Accédez à `/shop`
- [ ] Vérifiez les produits charger
- [ ] Testez la recherche
- [ ] Testez les filtres de catégorie
- [ ] Cliquez sur un produit

### 3️⃣ Détails Produit (3 min)
- [ ] Vérifiez `/product/{id}`
- [ ] Regardez les images
- [ ] Lisez les infos
- [ ] Regardez les avis
- [ ] Cliquez "Ajouter au panier"

### 4️⃣ Panier (3 min)
- [ ] Accédez à `/checkout`
- [ ] Vérifiez les articles
- [ ] Testez +/- quantité
- [ ] Testez supprimer article
- [ ] Vérifiez le total (sous-total + TVA)

### 5️⃣ Commande (5 min)
- [ ] Remplissez le formulaire livraison
- [ ] Cliquez "Confirmer"
- [ ] Vérifiez `/order-confirmation/{id}`
- [ ] Vérifiez le résumé

### 6️⃣ Profil (3 min)
- [ ] Accédez à `/profile`
- [ ] Cliquez "Edit"
- [ ] Modifiez infos
- [ ] Cliquez "Save"
- [ ] Vérifiez les modifications

### 7️⃣ Dashboard (3 min)
- [ ] Accédez à `/dashboard`
- [ ] Vérifiez les stats
- [ ] Vérifiez commandes récentes
- [ ] Vérifiez produits vendus

**Total temps**: ~30 minutes ⏱️

---

## 🐛 COMMON ISSUES & FIXES

### ❌ "Cannot GET /api/..."
```
→ Backend pas lancé
→ Vérifier port 8000
→ Vérifier CORS
```

### ❌ "Product not found"
```
→ Pas de produits en DB
→ Charger fixtures: python manage.py loaddata
```

### ❌ Images ne chargent pas
```
→ Vérifier chemins images
→ Vérifier URL dans DB
→ Vérifier MediaRoot
```

### ❌ Login échoue
```
→ Vérifier username/email
→ Vérifier password
→ Vérifier user existe
```

### ❌ Token expiré
```
→ Éffacer localStorage
→ Reconnecter
→ Vérifier JWT_EXPIRE
```

---

## 📊 VERIFICATION RAPIDE

```
✅ Backend started?        → http://localhost:8000
✅ Frontend started?       → http://localhost:5173
✅ Can signup?             → Try /signup
✅ Can login?              → Try /login
✅ Products loading?       → Check /shop
✅ Can add to cart?        → Try /product/{id}
✅ Can checkout?           → Try /checkout
✅ Order confirmation?     → After checkout
✅ No console errors?      → F12 → Console
✅ Responsive?             → Try mobile view
```

---

## 📝 QUICK COMMANDS

```bash
# Terminal 1: Backend
cd "d:\Shopina Project\code source\shopina-env\backend"
.\Scripts\Activate.ps1
python manage.py runserver

# Terminal 2: Frontend
cd "d:\Shopina Project\code source\front"
npm run dev
```

---

## 📖 DOCUMENTATION

| Document | Quand le lire |
|----------|---------------|
| QUICKSTART.md | Première fois / Setup |
| TESTING_GUIDE.md | Avant de tester |
| BUGS_FIXED.md | Problèmes rencontrés |
| INTEGRATION_NOTES.md | Comprendre architecture |
| SUMMARY.md | Vue d'ensemble travail |

---

## 🎯 FLOW UTILISATEUR COMPLET

```
[Home] 
  ↓
[SignUp/Login] ← TESTER ✅
  ↓
[Dashboard] ← TESTER ✅
  ↓
[Shop] ← TESTER ✅
  ↓
[Product Details] ← TESTER ✅
  ↓
[Add to Cart] ← TESTER ✅
  ↓
[Checkout] ← TESTER ✅
  ↓
[Order Confirmation] ← TESTER ✅
  ↓
[Profile] ← TESTER ✅
```

---

## ⚠️ CHOSES IMPORTANTES

1. **JWT Tokens** - Stockés en localStorage
   - Vérifier en F12 → Application → LocalStorage
   - Doivent contenir `access_token` et `refresh_token`

2. **CORS** - Configuré
   - Backend accepte requêtes de http://localhost:5173
   - Vérifier settings.py CORS_ALLOWED_ORIGINS

3. **API Base** - http://localhost:8000
   - Vérifier .env.local: VITE_API_BASE=http://localhost:8000

4. **Database** - SQLite (dev)
   - File: `db.sqlite3`
   - Migrations nécessaires: `python manage.py migrate`

5. **Stripe** (optionnel)
   - Non requis pour tester le site
   - Configurable avec VITE_STRIPE_PUBLISHABLE_KEY

---

## 🔒 SECURITY CHECKS

- [ ] Tokens en localStorage (améliorer pour prod)
- [ ] CORS configured
- [ ] CSRF protection active
- [ ] Password hashed
- [ ] No secrets in code
- [ ] HTTPS ready (pour prod)

---

## 📱 BROWSER COMPAT

Testé sur:
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile (iOS/Android)

---

## 🚨 MUST-FIX AVANT PROD

- [ ] Configurer HTTPS
- [ ] Activer CSRF cookies
- [ ] Mettre tokens en httpOnly
- [ ] Configurer email backend
- [ ] Tester paiements réels
- [ ] Backup database
- [ ] Configurer logging
- [ ] Configurer monitoring

---

## ✨ NICE-TO-HAVE

- [ ] Email confirmations
- [ ] SMS notifications
- [ ] Wishlist/Favorites
- [ ] Product reviews
- [ ] Coupon codes
- [ ] Multi-language
- [ ] Analytics
- [ ] Chatbot

---

## 🏁 VERDICT

```
Status: 🟢 READY TO TEST

Prochaine étape:
1. Faire la checklist de tests
2. Reporter les bugs
3. Fixer et itérer
4. Préparer production
5. Lancer! 🚀
```

---

**Last Updated**: Décembre 2025
**Status**: ✅ UP-TO-DATE
