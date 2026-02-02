# 🛒 Shopina - E-Commerce Platform

Une plateforme de commerce électronique moderne et complète construite avec **React (Frontend)** et **Django (Backend)**.

## 📋 Table des matières

- [Caractéristiques](#-caractéristiques)
- [Stack Technologique](#-stack-technologique)
- [Installation](#-installation)
- [Démarrage Rapide](#-démarrage-rapide)
- [Quick Start Collaborateurs](#-quick-start-collaborateurs)
- [Structure du Projet](#-structure-du-projet)
- [Configuration](#-configuration)
- [Fonctionnalités](#-fonctionnalités)
- [API Documentation](#-api-documentation)
- [Dépannage](#-dépannage)

## ✨ Caractéristiques

- **Authentification Sécurisée**: Support OAuth, JWT, et authentification traditionnelle
- **Gestion des Paniers**: Fonctionnalités complètes de panier persistant
- **Système de Commandes**: Gestion complète des commandes clients
- **Paiements Intégrés**: Support Stripe pour les transactions sécurisées
- **Notifications**: Système de notification pour les utilisateurs
- **Revues et Évaluations**: Système d'avis produits
- **Dashboard**: Interface d'administration avec statistiques
- **Gestion Multi-Boutiques**: Support pour plusieurs vendeurs
- **Interface Responsive**: Design adapté à tous les appareils

## 🛠 Stack Technologique

### Frontend
- **React 18** - Bibliothèque UI
- **Vite** - Bundler rapide
- **TypeScript** - Typage statique
- **Radix UI** - Composants headless
- **CSS personnalisé** - Styling

### Backend
- **Django 5.2.7** - Framework web Python
- **Django REST Framework** - API RESTful
- **Django Allauth** - Authentification sociale
- **djangorestframework-simplejwt** - JWT tokens
- **Stripe** - Paiements
- **Pillow** - Traitement d'images
- **drf-spectacular** - Documentation API

### Base de données
- **SQLite** (développement)
- Support PostgreSQL pour production

## 🚀 Installation

### Prérequis

- **Node.js** 16+ 
- **Python** 3.10+
- **pip** (gestionnaire de paquets Python)
- **Git**

### 1. Cloner le Repo (avec submodules)
### 1bis. Setup en une commande (Windows)

Vous pouvez lancer l'installation complète (backend + frontend) et démarrer les serveurs automatiquement via:

```bash
./quick_setup.bat
```

Ce script:
- Initialise les submodules
- Crée et prépare un venv Python (`.venv`) dans `code source/shopina-env/backend`
- Installe les dépendances backend et applique les migrations
- Installe les dépendances frontend
- Lance deux fenêtres PowerShell: `manage.py runserver` et `npm run dev`


Pour récupérer automatiquement le frontend (submodule), utilisez:

```bash
git clone --recurse-submodules https://github.com/Mohamed27wadi3/Shopina-project.git
cd Shopina-project
```

Si vous avez déjà cloné sans submodules:

```bash
git submodule update --init --recursive
```

### 2. Configuration Backend

```bash
# Naviguer vers le dossier backend
cd "code source/shopina-env/backend"

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un utilisateur administrateur
python manage.py createsuperuser

# Charger les données de test (optionnel)
python manage.py seed_data
```

### 3. Configuration Frontend

```bash
# Naviguer vers le dossier frontend
cd "code source/front"

# Installer les dépendances
npm install

# Créer un fichier .env.local
echo VITE_API_URL=http://localhost:8000/api > .env.local
```

## 🎯 Démarrage Rapide

### Terminal 1 - Backend

```bash
cd "code source/shopina-env/backend"
python manage.py runserver
```
✅ Backend disponible: `http://127.0.0.1:8000`

### Terminal 2 - Frontend

```bash
cd "code source/front"
npm run dev
```
✅ Frontend disponible: `http://localhost:3000`

### 📊 Admin Panel

- URL: `http://127.0.0.1:8000/admin`
- Utilisateur: `admin` (celui créé avec `createsuperuser`)

## 📁 Structure du Projet

```
Shopina-project/
├── code source/
│   ├── front/                          # React Frontend (Vite)
│   │   ├── src/
│   │   │   ├── components/             # Composants React réutilisables
│   │   │   ├── pages/                  # Pages/Routes
│   │   │   ├── services/               # Services API
│   │   │   ├── context/                # Contextes React
│   │   │   ├── styles/                 # Feuilles de style
│   │   │   ├── data/                   # Données statiques
│   │   │   └── App.tsx
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   └── tsconfig.json
│   │
│   └── shopina-env/backend/            # Django Backend
│       ├── shopina/                    # Configuration principale
│       ├── users/                      # App utilisateurs
│       ├── shops/                      # App boutiques
│       ├── shop/                       # App produits
│       ├── orders/                     # App commandes
│       ├── carts/                      # App paniers
│       ├── payments/                   # App paiements
│       ├── notifications/              # App notifications
│       ├── reviews/                    # App revues/évaluations
│       ├── manage.py
│       ├── requirements.txt
│       ├── db.sqlite3
│       └── settings.py
│
├── cahier de charge/                   # Documentation projet
├── plan de travail et Task/            # Planification
└── README.md                           # Ce fichier
```

## ⚙️ Configuration

### Backend - Fichier Settings

Éditer `code source/shopina-env/backend/shopina/settings.py` pour configurer:

```python
# Mode développement
DEBUG = True

# Hôtes autorisés
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Frontend - Fichier .env.local

```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Shopina
```

## 🎨 Fonctionnalités Principales

### 👤 Authentification
- ✅ Inscription/Connexion
- ✅ OAuth (Google, GitHub, Facebook)
- ✅ JWT Tokens
- ✅ Profil utilisateur
- ✅ Authentification à deux facteurs

### 🛍️ Produits & Boutiques
- ✅ Catalogue de produits
- ✅ Gestion de plusieurs boutiques
- ✅ Catégories et filtres
- ✅ Recherche avancée
- ✅ Images produits optimisées

### 🛒 Panier & Commandes
- ✅ Panier persistant
- ✅ Gestion des stocks
- ✅ Historique des commandes
- ✅ Statuts de livraison
- ✅ Suivi des commandes

### 💳 Paiements
- ✅ Intégration Stripe
- ✅ Paiements sécurisés
- ✅ Confirmation de transaction
- ✅ Factures

### ⭐ Évaluations & Revues
- ✅ Système d'avis utilisateurs
- ✅ Notation produits
- ✅ Photos de revues

### 📊 Dashboard
- ✅ Statistiques de ventes
- ✅ Graphiques analytiques
- ✅ Gestion des produits
- ✅ Gestion des commandes

## 📚 API Documentation

### Endpoints Principaux

#### Utilisateurs
```
POST   /api/users/register/           - Inscription
POST   /api/users/login/              - Connexion
GET    /api/users/profile/            - Profil utilisateur
PUT    /api/users/profile/            - Mise à jour profil
POST   /api/users/logout/             - Déconnexion
```

#### Produits
```
GET    /api/shop/products/            - Liste des produits
GET    /api/shop/products/{id}/       - Détail d'un produit
POST   /api/shop/products/            - Créer un produit (vendeur)
PUT    /api/shop/products/{id}/       - Modifier un produit (vendeur)
DELETE /api/shop/products/{id}/       - Supprimer un produit (vendeur)
```

#### Commandes
```
GET    /api/orders/                   - Mes commandes
POST   /api/orders/                   - Créer une commande
GET    /api/orders/{id}/              - Détail commande
PUT    /api/orders/{id}/              - Mettre à jour statut
```

#### Paiements
```
POST   /api/payments/create-intent/   - Créer intention de paiement
POST   /api/payments/confirm/         - Confirmer le paiement
GET    /api/payments/history/         - Historique paiements
```

Pour la documentation complète interactive, consulter `/api/schema/swagger/` après le démarrage du serveur.

## 🐛 Dépannage

### ❌ Erreur: "Cannot compute Sum"
**Cause**: Agrégation SQL complexe dans l'endpoint dashboard/stats
**Solution**: Vérifier `code source/shopina-env/backend/orders/views.py` ligne 148

### ❌ Port déjà utilisé
```bash
# Frontend avec port différent
npm run dev -- --port 3001

# Backend avec port différent
python manage.py runserver 8001
```

### ❌ Problèmes de CORS
Vérifier `CORS_ALLOWED_ORIGINS` dans les settings Django.

### ❌ Module non trouvé
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
npm install --legacy-peer-deps
```

### ❌ Migrations non appliquées
```bash
python manage.py migrate
python manage.py migrate --run-syncdb
```

## 📝 Commandes Utiles

### Backend
```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Charger des données d'exemple
python manage.py seed_data

# Créer un utilisateur admin
python manage.py createsuperuser

# Lancer les tests
python manage.py test

# Shell Django interactive
python manage.py shell
```

### Frontend
```bash
# Lancer en développement
npm run dev

# Build pour production
npm run build

# Prévisualisation build
npm run preview

# Tests
npm run test
```

## 🤝 Contribution

1. Forker le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📞 Support & Contact

Pour toute question ou problème:
- 📧 Ouvrir une [issue GitHub](https://github.com/Mohamed27wadi3/Shopina-project/issues)
- 📱 Contacter l'équipe de développement

## 📄 License

Ce projet est sous license MIT. 

---

**Dernière mise à jour**: 28 Décembre 2025 ✅

Développé avec ❤️ par l'équipe Shopina

6. Lancer le front (depuis `front/`):

```bash
npm install
npm run dev
```

API principales
---------------
Base URL (développement): `http://localhost:8000`

- Auth & Users
  - POST `/api/users/register/` → créer un compte (body: `username`, `email`, `password`) → renvoie `user`, `access`, `refresh`
  - POST `/api/users/token/` → obtenir `access`/`refresh` (login par username ou email)
  - POST `/api/users/token/refresh/` → rafraîchir le token
  - GET/PUT `/api/users/profile/` → profil (auth requis)

- Shop
  - GET `/api/shop/products/` → liste de produits (search & filter)
  - GET `/api/shop/products/{pk}/` → détail produit
  - GET `/api/shop/categories/` → liste catégories

- Orders
  - GET `/api/orders/` → commandes de l'utilisateur (auth requis)
  - POST `/api/orders/` → créer commande (auth requis)

Sécurité & CORS
---------------
- Le back accepte les requêtes CORS depuis `http://localhost:5173` (dev Vite). Modifier `CORS_ALLOWED_ORIGINS` dans `settings.py` si nécessaire.

Tests
-----
Exécuter les tests unitaires Django:

```bash
python manage.py test
```

Notes & choix techniques
------------------------
- J'ai implémenté une `User` personnalisée (`users.models.User`) pour étendre les attributs utilisateur (plan, avatar, shop_name).
- L'authentification est basée sur JWT (djangorestframework-simplejwt). Le endpoint de connexion accepte maintenant `email` ou `username`.
- Les modèles `Product`, `Category`, `Order`, `OrderItem` respectent la séparation des responsabilités et sont exposés via des viewsets / API views DRF.

Prochaines améliorations possibles
--------------------------------
- Ajouter l'intégration d'un fournisseur de paiement (Stripe) pour les commandes (implémentation de base fournie).
- Ajouter des endpoints d'administration pour gérer les stocks, promotions, etc.
- Ajouter bots de tests e2e (Cypress / Playwright) et pipelines CI.

Stripe (intégration fournie)
----------------------------
- Variables d'environnement à définir :
  - `STRIPE_SECRET_KEY` (clé secrète côté serveur)
  - `STRIPE_WEBHOOK_SECRET` (secret du webhook Stripe)
- Endpoints exposés :
  - POST `/api/payments/create-intent/` (auth requis) — body: `{ "order_id": <order_id> }` → renvoie `client_secret` pour la confirmation côté client
  - POST `/api/payments/webhook/` — endpoint public pour recevoir les webhooks Stripe (sécurisé par la signature `STRIPE_WEBHOOK_SECRET`)

Notes: le backend utilise la librairie officielle `stripe` et crée un objet `Payment` lié à une `Order` pour tracer le paiement.

Contact
-------
Si vous voulez que je continue (tests plus complets, Docker, CI, intégration paiement, etc.), dites-moi exactement quelle priorité et je continue pas-à-pas.

## 🚀 Quick Start Collaborateurs

### Clonage avec submodules

```bash
git clone --recurse-submodules https://github.com/Mohamed27wadi3/Shopina-project.git
cd Shopina-project
```

Si déjà cloné sans submodules :

```bash
git submodule update --init --recursive
```

### Lancer Backend (Django)

```bash
cd "code source/shopina-env/backend"
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Lancer Frontend (Vite/React)

```bash
cd "code source/front"
npm install
npm run dev
```

### Variables d’environnement rapides

- Frontend: créer `.env.local` avec `VITE_API_URL=http://localhost:8000/api`
- Backend: créer `.env` si nécessaire (voir section Configuration)

## 📦 Website Builder (bundle frontend Vite)

Le dossier `code source/front` provient d’un bundle « Website Builder » basé sur Vite. Pour l’exécuter indépendamment:

1. `cd "code source/front"`
2. `npm i`
3. `npm run dev`

### Tests end-to-end Playwright

Le bundle inclut une suite Playwright pouvant tourner en mode mock ou réel:

- Mode mock (par défaut): `npm run test:e2e`
- Mode réel (nécessite backend sur `http://localhost:8000` et clés Stripe test):

```
E2E_REAL=1 PLAYWRIGHT_BASE_URL=http://127.0.0.1:5173 npm run test:e2e
```

Pour l’installation des navigateurs Playwright: `npm run test:e2e:install`.

> Le test principal est `tests/checkout.spec.ts`. En CI, configurez `PLAYWRIGHT_BASE_URL` vers votre instance front déployée et n’activez `E2E_REAL=1` qu’avec un backend + Stripe disponibles.
