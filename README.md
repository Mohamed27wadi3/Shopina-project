# Shopina — Projet e-commerce

Résumé
-------
Shopina est une application de boutique en ligne composée d'un front-end (Vite + React + TypeScript) et d'un back-end Django REST (Django + DRF). Ce dépôt contient le code source du front et du back ; le back est conçu pour fournir des API REST sécurisées (JWT) compatibles avec le front fourni.

Principaux points techniques
---------------------------
- Back-end: Django 5.2 + Django REST Framework + Simple JWT pour l'authentification
- Front-end: Vite + React + TypeScript (déjà fourni dans `front/`)
- Architecture: apps Django séparées par domaine (`users`, `shop`, `orders`) (respect du pattern MVT / séparation des responsabilités)
- Tests de base et commande de seed pour peupler la base avec les produits d'exemple

Arborescence principale
----------------------
- `backend/` : serveur Django
  - `shopina/` : configuration projet
  - `users/`, `shop/`, `orders/` : apps Django
- `front/` : application frontend (Vite/React)

Installation (développement)
---------------------------
1. Créer un environnement virtuel et installer les dépendances (depuis `backend/`):

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Mettre à jour les settings si besoin (fichier `backend/shopina/settings.py`)

3. Créer les migrations et migrer la base de données:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Seed (peupler) la base avec des produits d'exemple:

```bash
python manage.py seed_products
```

5. Lancer le serveur Django:

```bash
python manage.py runserver
```

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
- Ajouter l'intégration d'un fournisseur de paiement (Stripe) pour les commandes.
- Ajouter des endpoints d'administration pour gérer les stocks, promotions, etc.
- Ajouter bots de tests e2e (Cypress / Playwright) et pipelines CI.

Contact
-------
Si vous voulez que je continue (tests plus complets, Docker, CI, intégration paiement, etc.), dites-moi exactement quelle priorité et je continue pas-à-pas.
