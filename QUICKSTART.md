# Guide de Démarrage - Shopina Front-Back Integration

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8+
- Node.js 16+
- pip et npm installés

---

## Backend Setup

### 1. Accéder au répertoire backend
```bash
cd "d:\Shopina Project\code source\shopina-env\backend"
```

### 2. Activer l'environnement virtuel (Windows)
```bash
# Avec PowerShell
.\Scripts\Activate.ps1

# Avec CMD
Scripts\activate.bat
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations
```bash
python manage.py migrate
```

### 5. Créer un utilisateur admin (optionnel)
```bash
python manage.py createsuperuser
# Email: admin@example.com
# Password: admin123
```

### 6. Charger les données de test (si disponibles)
```bash
python manage.py loaddata fixtures/*.json
```

### 7. Démarrer le serveur
```bash
python manage.py runserver 0.0.0.0:8000
```

✅ Backend accessible: http://localhost:8000
- API Docs: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

---

## Frontend Setup

### 1. Accéder au répertoire frontend
```bash
cd "d:\Shopina Project\code source\front"
```

### 2. Installer les dépendances
```bash
npm install
```

### 3. Configurer les variables d'environnement
Créer un fichier `.env.local` à la racine du frontend:
```env
VITE_API_BASE=http://localhost:8000
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx  # Si vous utilisez Stripe
```

### 4. Démarrer le serveur de développement
```bash
npm run dev
```

✅ Frontend accessible: http://localhost:5173

---

## 🧪 Tests d'Intégration

### Test 1: Authentication Flow
```bash
# 1. Aller à http://localhost:5173/signup
# 2. Remplir le formulaire:
#    - Email: test@example.com
#    - Username: testuser
#    - Password: Test@1234
# 3. Cliquer "Create Account"
# 4. Vérifier redirection vers /dashboard
```

### Test 2: Product Listing
```bash
# 1. Aller à http://localhost:5173/shop
# 2. Vérifier que les produits chargent
# 3. Tester la recherche
# 4. Tester les filtres de catégorie
```

### Test 3: Product Details
```bash
# 1. Cliquer sur un produit
# 2. Vérifier /product/{id} charge
# 3. Vérifier les images, infos, et avis
# 4. Tester ajouter au panier
```

### Test 4: Shopping Cart
```bash
# 1. Ajouter plusieurs produits au panier
# 2. Cliquer sur le bouton Panier
# 3. Vérifier /checkout charge
# 4. Vérifier quantités, totaux, TVA
```

### Test 5: Checkout
```bash
# 1. Remplir formulaire de livraison
# 2. Cliquer "Confirm Order"
# 3. Vérifier /order-confirmation/{id} s'affiche
# 4. Vérifier résumé de la commande
```

### Test 6: Profile
```bash
# 1. Aller à /profile
# 2. Cliquer "Edit"
# 3. Modifier les informations
# 4. Cliquer "Save"
# 5. Vérifier mise à jour
```

### Test 7: Dashboard
```bash
# 1. Aller à /dashboard
# 2. Vérifier affichage des stats
# 3. Vérifier liste des commandes récentes
# 4. Vérifier produits les plus vendus
```

---

## 🔍 Vérifications de Débogage

### Logs Backend
```bash
# Regarder les logs en direct
tail -f db.sqlite3  # Ou directement dans la console

# Vérifier les erreurs Django
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> get_user_model().objects.all()
```

### Logs Frontend
```bash
# Voir la console navigateur: F12 → Console
# Tous les logs API y seront affichés

# Ou vérifier le terminal npm run dev
```

### API Testing
```bash
# Tester avec curl
curl -X GET http://localhost:8000/api/shop/products/
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## ⚙️ Configuration

### Base de Données
- **Backend**: SQLite (`db.sqlite3`)
- **Pour Production**: Utiliser PostgreSQL
- **Migrations**: `python manage.py makemigrations && migrate`

### CORS
- Configuré dans `settings.py`
- Frontend: `http://localhost:5173`
- Adapter domaine pour production

### API Keys
- **Stripe**: À configurer dans `.env`
- **Email**: À configurer dans `settings.py`
- **JWT**: Clés auto-générées

---

## 📦 Détails des Endpoints

### Authentification
```
POST   /api/users/register/        - Créer compte
POST   /api/users/token/           - Login (JWT)
POST   /api/users/token/refresh/   - Refresh token
GET    /api/users/profile/         - Profil utilisateur
PATCH  /api/users/profile/         - Modifier profil
```

### Produits
```
GET    /api/shop/products/         - Liste produits
GET    /api/shop/products/{id}/    - Détail produit
GET    /api/shop/categories/       - Catégories
```

### Commandes
```
GET    /api/orders/                - Mes commandes
POST   /api/orders/                - Créer commande
GET    /api/orders/{id}/           - Détail commande
```

### Paiements
```
POST   /api/payments/create-intent/ - Créer intent Stripe
POST   /api/payments/webhook/      - Webhook Stripe
```

### Avis
```
GET    /api/reviews/               - Avis produit
POST   /api/reviews/               - Ajouter avis
PATCH  /api/reviews/{id}/          - Modifier avis
DELETE /api/reviews/{id}/          - Supprimer avis
```

---

## 🐛 Troubleshooting

### Frontend ne se connecte pas au backend
```bash
# Vérifier que le backend est lancé
curl http://localhost:8000

# Vérifier VITE_API_BASE dans .env.local
# Doit être: http://localhost:8000

# Vérifier CORS dans Django settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### "Product not found" 
```bash
# Vérifier que les produits existent
python manage.py shell
>>> from shop.models import Product
>>> Product.objects.count()

# Si 0, charger fixtures
python manage.py loaddata initial_data.json
```

### Erreur "JWT token invalid"
```bash
# Vérifier le token dans localStorage (F12 → Application)
# Doit contenir access_token et refresh_token

# Vérifier l'expiration du token (défaut: 1 heure)
```

### Images ne chargent pas
```bash
# Vérifier le chemin des images
# Django doit servir les fichiers media

# En développement, Django le fait automatiquement
# En production, utiliser Nginx ou S3
```

---

## 📊 Base de Données - Structure

### Modèles Principaux
```
User
├── Profile
├── Orders
│   └── OrderItem
│       └── Product
├── Cart
│   └── CartItem
│       └── Product
└── Reviews
    └── Product

Product
├── Category
├── Reviews
└── Images

Order
├── OrderItems
├── Payment
└── Notifications
```

---

## 🚀 Déploiement (Production)

### Frontend (Vercel/Netlify)
```bash
# Build
npm run build

# Deploy
vercel deploy --prod
```

### Backend (Heroku/Railway)
```bash
# Préparation
pip freeze > requirements.txt

# Déployer avec:
# - PostgreSQL pour DB
# - Redis pour cache
# - Gunicorn pour serveur
```

---

## 📚 Documentation Utile

- **Django**: https://docs.djangoproject.com/
- **Django REST**: https://www.django-rest-framework.org/
- **React**: https://react.dev
- **Vite**: https://vitejs.dev
- **TailwindCSS**: https://tailwindcss.com

---

## ✅ Checklist Final

- [ ] Backend lancé sur port 8000
- [ ] Frontend lancé sur port 5173
- [ ] Signup/Login fonctionne
- [ ] Produits affichés
- [ ] Panier fonctionne
- [ ] Checkout fonctionne
- [ ] Commande créée
- [ ] Confirmation affichée
- [ ] Profile modifiable
- [ ] Dashboard affiche les stats
- [ ] Pas d'erreurs console
- [ ] Responsive design OK

---

**Date**: Décembre 2025
**Statut**: ✅ Prêt pour testing complet
