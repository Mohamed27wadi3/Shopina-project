 # 🎨 Schéma Visuel MVC - Shopina

## 1️⃣ Flux Principal MVC

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React/TypeScript)              │
│                  (src/pages/MyShopPage.tsx)                 │
│                                                              │
│  Utilisateur clique sur "Ajouter un produit"               │
│              ↓                                               │
│  Envoie: POST /api/shop/create/                            │
│         { name: "Moteur V8", price: 5000, ... }            │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP REQUEST
                 ▼
┌─────────────────────────────────────────────────────────────┐
│        VIEW (shop/views.py) - create_product_api()         │
│                                                              │
│  @api_view(['POST'])                                        │
│  def create_product_api(request):                           │
│      • Extrait les données: name, price, image             │
│      • Valide HTTP: if not name: return 400                │
│      • Appelle: ProductService.create_product_for_shop()   │
│                                                              │
│              ↓ SERVICE CALL                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│   SERVICE (services/product_service.py) - ProductService   │
│                                                              │
│  def create_product_for_shop(shop, name, price, ...):      │
│      • Valide métier: if price <= 0: raise ValidationError│
│      • Applique logique: name = name.strip().title()       │
│      • Crée catégorie: Category.objects.get_or_create()    │
│      • Retourne: Product object                            │
│                                                              │
│              ↓ MODEL CALL                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│        MODEL (shop/models.py) - Product                    │
│                                                              │
│  class Product(models.Model):                              │
│      name = CharField(max_length=255)                      │
│      price = DecimalField()                                │
│      shop = ForeignKey('shops.Shop')                       │
│                                                              │
│              ↓ DATABASE SAVE                                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   DATABASE      │
        │  (PostgreSQL)   │
        │                 │
        │  INSERT INTO    │
        │  shop_product   │
        │  VALUES(...)    │
        └────────┬────────┘
                 │
                 ▼ RESPONSE
┌─────────────────────────────────────────────────────────────┐
│        SERIALIZER (shop/serializers.py)                    │
│                                                              │
│  ProductSerializer(product).data                            │
│  Transforme le Model en JSON                               │
│                                                              │
│  { id: 1, name: "Moteur V8", price: 5000, ... }           │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP RESPONSE (201 Created)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                         │
│                                                              │
│  • Affiche: "Produit ajouté avec succès!"                 │
│  • Toast notification avec gradient vert                    │
│  • Rafraîchit la liste des produits                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 2️⃣ Architecture en Couches

```
┌─────────────────────────────────────────────────────────────┐
│                     COUCHE HTTP (V)                         │
│              (Gère les requêtes HTTP)                       │
│              shop/views.py (50 lignes)                      │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ create_product_api(request)                         │  │
│  │ • Récupère: request.data.get('name')               │  │
│  │ • Valide: if not name: return 400                  │  │
│  │ • Appelle: ProductService                          │  │
│  │ • Retourne: Response(serializer.data, 201)         │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 COUCHE MÉTIER (S)                           │
│            (Logique de gestion métier)                      │
│         services/product_service.py (200 lignes)            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ ProductService.create_product_for_shop()            │  │
│  │ • Valide: if price <= 0                            │  │
│  │ • Formate: name = name.strip().title()             │  │
│  │ • Crée: Category.objects.get_or_create()           │  │
│  │ • Retourne: Product instance                       │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  COUCHE DONNÉES (M)                         │
│            (Structure et stockage des données)              │
│              shop/models.py (100 lignes)                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ class Product(models.Model):                        │  │
│  │     name = CharField(max_length=255)               │  │
│  │     price = DecimalField(max_digits=10)            │  │
│  │     shop = ForeignKey('shops.Shop')                │  │
│  │     category = ForeignKey(Category)                │  │
│  │     image = ImageField(upload_to='products/')      │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         ↓
        ┌─────────────────────────────────┐
        │      BASE DE DONNÉES            │
        │      (PostgreSQL/SQLite)        │
        │                                 │
        │  shop_product table:            │
        │  ┌─────────────────────────┐   │
        │  │ id │ name │ price │shop │   │
        │  ├─────────────────────────┤   │
        │  │ 1  │ Mot  │ 5000  │ 2   │   │
        │  │ 2  │ Rad  │ 300   │ 2   │   │
        │  └─────────────────────────┘   │
        └─────────────────────────────────┘
```

---

## 3️⃣ Responsabilités par Couche

```
┌────────────────────────────────────────────────────────────┐
│                          VIEW (V)                           │
│                   Gère les Requêtes HTTP                   │
├────────────────────────────────────────────────────────────┤
│ ✅ FAIT:                    │ ❌ NE FAIT PAS:              │
│ • Reçoit request           │ • Logique métier             │
│ • Extrait données          │ • Accès BDD direct           │
│ • Appelle Service          │ • Transformation JSON        │
│ • Retourne Response        │ • Validation métier          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                      SERVICE (S)                            │
│                  Logique Métier / Business                 │
├────────────────────────────────────────────────────────────┤
│ ✅ FAIT:                    │ ❌ NE FAIT PAS:              │
│ • Valide données           │ • Gestion HTTP               │
│ • Applique règles          │ • Accès direct BDD           │
│ • Coordonne opérations     │ • Transformation JSON        │
│ • Lève exceptions          │ • Requêtes HTTP              │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                       MODEL (M)                             │
│                   Structure des Données                    │
├────────────────────────────────────────────────────────────┤
│ ✅ FAIT:                    │ ❌ NE FAIT PAS:              │
│ • Défini schema             │ • Logique métier             │
│ • Relations entre tables    │ • Requêtes complexes         │
│ • Contraintes              │ • Accès direct bdd           │
│ • Types de données         │ • Transformation JSON        │
└────────────────────────────────────────────────────────────┘
```

---

## 4️⃣ Flux Complet: Exemple "Ajouter un Produit"

```
┌─────────────────────────────────────────────────────────────┐
│ ÉTAPE 1: Frontend envoie la requête                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📱 MyShopPage.tsx (Frontend)                              │
│  ↓                                                           │
│  const handleAddProduct = async (formData) => {            │
│    const response = await fetch(                           │
│      `${API_BASE}/api/shop/create/`,                       │
│      {                                                       │
│        method: 'POST',                                      │
│        body: JSON.stringify({                              │
│          name: "Moteur V8",                                │
│          price: 5000,                                       │
│          category: "Moteurs",                              │
│          stock: 10,                                         │
│          image: File                                        │
│        })                                                    │
│      }                                                       │
│    );                                                        │
│  }                                                           │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │ POST /api/shop/create/
                   │ { name, price, ... }
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ ÉTAPE 2: VIEW reçoit et valide HTTP                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔽 shop/views.py :: create_product_api()                 │
│                                                              │
│  @api_view(['POST'])                                        │
│  @permission_classes([IsAuthenticated])                    │
│  def create_product_api(request):                          │
│      ✅ shop = request.user.shop                           │
│      ✅ name = request.data.get('name')  # "Moteur V8"     │
│      ✅ price = request.data.get('price')  # 5000          │
│      ✅ if not name: return Response(..., 400)  # HTTP     │
│      ⬇️  Appelle le SERVICE                                │
│      ✅ product_service = ProductService()                 │
│      ✅ product = product_service.create_product_for_shop(│
│             shop=shop, name=name, price=price, ...         │
│         )                                                    │
│      ⬇️  Prépare la réponse                                │
│      ✅ serializer = ProductSerializer(product, ...)      │
│      ✅ return Response(serializer.data, 201)             │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │ Appelle SERVICE
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ ÉTAPE 3: SERVICE applique la logique métier                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🧠 services/product_service.py :: ProductService          │
│                                                              │
│  def create_product_for_shop(shop, name, price, ...):      │
│      ⚡ VALIDATION MÉTIER:                                 │
│      ✅ if not name or not name.strip():                   │
│           raise ValidationError("Name required")           │
│      ✅ if price <= 0:                                     │
│           raise ValidationError("Price > 0")               │
│      ✅ if stock < 0:                                      │
│           raise ValidationError("Stock >= 0")              │
│                                                              │
│      ⚙️  LOGIQUE MÉTIER:                                    │
│      ✅ name = name.strip().title()  # Format: "Moteur V8" │
│      ✅ category = Category.objects.get_or_create(         │
│             name=category_name or 'Autre'                  │
│         )                                                    │
│                                                              │
│      💾 CRÉE LE PRODUIT:                                    │
│      ✅ product = Product.objects.create(                  │
│             shop=shop,                                      │
│             name=name,  # "Moteur V8"                       │
│             price=price,  # 5000                            │
│             category=category,                              │
│             stock=stock,  # 10                              │
│             image=image                                     │
│         )                                                    │
│      ✅ return product  # Product instance                 │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │ Product object
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ ÉTAPE 4: MODEL stocke dans la BDD                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  💾 shop/models.py :: Product                              │
│                                                              │
│  class Product(models.Model):                              │
│      id = AutoField(primary_key=True)                      │
│      name = CharField(max_length=255)                      │
│      price = DecimalField(max_digits=10, decimal_places=2) │
│      shop = ForeignKey('shops.Shop', ...)                  │
│      category = ForeignKey(Category, ...)                  │
│      stock = IntegerField(default=1)                       │
│      image = ImageField(upload_to='products/')             │
│      created_at = DateTimeField(auto_now_add=True)         │
│                                                              │
│  Django ORM exécute:                                        │
│  INSERT INTO shop_product                                  │
│  (name, price, shop_id, category_id, stock, image)         │
│  VALUES                                                     │
│  ('Moteur V8', 5000, 2, 5, 10, 'products/xyz.jpg')        │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │ INSERT success
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ ÉTAPE 5: SERIALIZER transforme en JSON                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📦 shop/serializers.py :: ProductSerializer               │
│                                                              │
│  class ProductSerializer(serializers.ModelSerializer):     │
│      class Meta:                                            │
│          model = Product                                    │
│          fields = ['id', 'name', 'price', 'stock', ...]    │
│                                                              │
│  Convertit: Product object → JSON dict                     │
│  {                                                           │
│      "id": 1,                                               │
│      "name": "Moteur V8",                                   │
│      "price": "5000.00",                                    │
│      "stock": 10,                                           │
│      "category": "Moteurs",                                 │
│      "image_url": "/media/products/xyz.jpg",               │
│      "created_at": "2026-02-04T10:30:00Z"                  │
│  }                                                           │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │ JSON Response
                   │ Status: 201 Created
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ ÉTAPE 6: Frontend reçoit et affiche le résultat            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📱 MyShopPage.tsx                                          │
│  ↓                                                           │
│  ✅ Status 201 reçu                                         │
│  ✅ Toast: "✅ Moteur V8 ajouté avec succès !"             │
│  ✅ Gradient vert appliqué au toast                         │
│  ✅ Appelle fetchProducts() pour rafraîchir la liste      │
│  ✅ Affiche: "1 produit(s) dans votre boutique"            │
│                                                              │
│  Avant:  []                                                 │
│  Après: [{ id: 1, name: "Moteur V8", price: 5000, ... }]  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5️⃣ Comparaison: Bon vs Mauvais Code

### ❌ MAUVAIS (Mélange tout dans le Model)

```
Frontend
   ↓
View (HTTP)
   ↓
Model
├─ Structure (❌ Ok)
├─ Validation (❌ Pas ici!)
├─ Logique métier (❌ Pas ici!)
└─ Accès BDD (❌ Pas ici!)
   ↓
Database

❌ PROBLÈMES:
• Impossible à tester (couplé à la BDD)
• Impossible de réutiliser la logique
• Code illisible et complexe
• Changement = risque d'erreurs
```

### ✅ BON (MVC avec séparation)

```
Frontend
   ↓
View (HTTP)     ← Gère UNIQUEMENT les requêtes
   ↓ appelle
Service         ← Gère UNIQUEMENT la logique métier
   ↓ appelle
Model/Repository ← Gère UNIQUEMENT l'accès BDD
   ↓
Database

✅ AVANTAGES:
• Chaque couche a UNE responsabilité
• Facile à tester
• Facile à réutiliser
• Facile à changer
• Code lisible et maintenable
```

---

## 6️⃣ Circulation des Données

```
┌─────────────┐
│  Frontend   │
└──────┬──────┘
       │ JSON
       │ {name, price}
       ▼
    ┌─────────────┐
    │   VIEW      │ Extrait: name, price
    │             │ Valide HTTP: if not name
    │             │ Appelle: Service
    └──────┬──────┘
           │ Python object
           │ (shop, name, price)
           ▼
    ┌─────────────┐
    │  SERVICE    │ Valide: if price <= 0
    │             │ Formate: name.title()
    │             │ Crée: Product()
    └──────┬──────┘
           │ Model instance
           │ Product(...)
           ▼
    ┌─────────────┐
    │   MODEL     │ Sauve en BDD
    │             │ Retourne: id
    └──────┬──────┘
           │ QuerySet / Object
           │ {id, name, price}
           ▼
    ┌─────────────┐
    │ SERIALIZER  │ Transforme: Model → JSON
    └──────┬──────┘
           │ JSON
           │ {id, name, price}
           ▼
    ┌─────────────┐
    │  Frontend   │ Affiche résultat
    └─────────────┘
```

---

## 7️⃣ Fichiers du Projet

```
shopina-env/backend/
├── shop/
│   ├── models.py              (M) Structure Product, Category
│   ├── views.py               (V) create_product_api()
│   ├── serializers.py         (Transform Model → JSON)
│   ├── services/
│   │   └── product_service.py (S) ProductService
│   └── urls.py                (Routes)
├── shops/
│   ├── models.py              (M) Structure Shop
│   └── ...
└── core/
    └── utils/
        └── exceptions.py      (ValidationError, etc.)

code source/front/
├── src/
│   ├── pages/
│   │   └── MyShopPage.tsx      Frontend (Envoie les requêtes)
│   ├── services/
│   │   └── api.ts             Fetch helper
│   └── components/
│       └── Header.tsx         UI
```

---

## 📊 Résumé Visuel

```
UTILISATEUR
    ↓
FRONTEND (React)        ← Affiche l'interface
    ↓
VIEW (HTTP)             ← Reçoit les requêtes
    ↓
SERVICE (Logique)       ← Valide et traite
    ↓
MODEL (Données)         ← Sauve en BDD
    ↓
DATABASE                ← Persiste les données
    ↓
SERVICE                 ← Récupère les données
    ↓
SERIALIZER              ← Transforme en JSON
    ↓
VIEW                    ← Retourne response
    ↓
FRONTEND                ← Affiche le résultat
    ↓
UTILISATEUR
```

Cela, c'est le cycle complet du MVC! 🔄
