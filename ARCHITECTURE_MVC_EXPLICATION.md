# 🏗️ Architecture MVC du Projet Shopina

## 📋 Qu'est-ce que le MVC ?

Le pattern **MVC** sépare une application en 3 couches :

```
┌─────────────────────────────────────────┐
│         REQUEST HTTP (Frontend)         │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  VIEW (V)       │  ← Reçoit les requêtes
        │  (shop/views.py)│  ← Gère HTTP
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  SERVICE (C)    │  ← Logique métier
        │ (ProductService)│  ← Règles de gestion
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  REPOSITORY (R) │  ← Accès aux données
        │ (ProductRepo)   │  ← Requêtes BDD
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  MODEL (M)      │  ← Structure des données
        │  (Product)      │  ← Tables BDD
        └─────────────────┘
```

---

## 🎯 Les 3 Couches Expliquées

### **1️⃣ MODEL (M) - Structure des Données**

**Responsabilités:**
- Définir la structure des données
- Représenter les tables de la base de données
- Définir les relations entre entités

**Fichier:** `shop/models.py`

```python
# ❌ MAUVAIS: Ajouter la logique ici
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def create_product(self, ...):  # ❌ Ne pas faire ça!
        # Logique métier dans le Model
        pass

# ✅ BON: Uniquement la structure
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
```

---

### **2️⃣ VIEW (V) - Gestion des Requêtes HTTP**

**Responsabilités:**
- Recevoir les requêtes HTTP
- Extraire les données (params, body JSON, fichiers)
- Appeler le SERVICE pour traiter les données
- Retourner une réponse HTTP

**Fichier:** `shop/views.py` (lignes 80-125)

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_api(request):
    """
    VIEW: Gère la requête HTTP
    """
    # ✅ ÉTAPE 1: Extraire les données HTTP
    shop = request.user.shop
    name = request.data.get('name')
    price = request.data.get('price')
    image = request.FILES.get('image')
    
    # ❌ NE PAS FAIRE: Logique métier ici
    # if not name or price < 0:  ← C'est pour le SERVICE!
    #     ...
    
    # ✅ ÉTAPE 2: Appeler le SERVICE pour traiter
    product_service = ProductService()
    product = product_service.create_product_for_shop(
        shop=shop,
        name=name,
        price=price,
        image=image
    )
    
    # ✅ ÉTAPE 3: Retourner la réponse HTTP
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data, status=201)
```

---

### **3️⃣ SERVICE (Logique Métier) - C du MVC**

**Responsabilités:**
- Implémenter la logique métier
- Valider les données
- Coordonner les opérations
- **NE PAS accéder directement à la base de données**

**Fichier:** `shop/services/product_service.py`

```python
class ProductService:
    """SERVICE: Logique métier du produit"""
    
    def create_product_for_shop(self, shop, name, price, description, 
                                category_name, stock, image):
        # ✅ ÉTAPE 1: Valider les données métier
        if not name or not name.strip():
            raise ValidationError("Le nom du produit est requis")
        
        if price <= 0:
            raise ValidationError("Le prix doit être positif")
        
        if stock < 0:
            raise ValidationError("Le stock ne peut pas être négatif")
        
        # ✅ ÉTAPE 2: Logique métier (règles de gestion)
        # Par exemple: prix minimum, format du nom, etc.
        name = name.strip().title()  # Formater le nom
        
        # ✅ ÉTAPE 3: Appeler le REPOSITORY pour sauvegarder
        category = self._get_or_create_category(category_name)
        
        product = Product.objects.create(
            shop=shop,
            name=name,
            price=price,
            description=description,
            category=category,
            stock=stock,
            image=image
        )
        
        return product
    
    def _get_or_create_category(self, category_name):
        """Logique: créer la catégorie si elle n'existe pas"""
        if not category_name:
            category, _ = Category.objects.get_or_create(name='Autre')
        else:
            category, _ = Category.objects.get_or_create(name=category_name)
        return category
```

---

## 🔄 Flux Complet: Un Exemple

### **Scénario: Créer un produit**

#### **1️⃣ Frontend envoie une requête HTTP**

```typescript
// src/pages/MyShopPage.tsx
const handleAddProduct = async (formData) => {
    const response = await fetch(`${API_BASE}/api/shop/create/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: "Moteur V8",
            price: 5000,
            description: "Moteur haute performance",
            category: "Moteurs",
            stock: 10,
            image: imageFile
        })
    });
};
```

---

#### **2️⃣ VIEW reçoit et extrait les données**

```python
# shop/views.py (lignes 88-125)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_api(request):
    """
    📥 ÉTAPE 1: Recevoir la requête HTTP
    """
    # Extraire shop de l'utilisateur authentifié
    shop = request.user.shop
    
    # Extraire les champs du formulaire
    name = request.data.get('name')          # "Moteur V8"
    price = request.data.get('price')        # 5000
    description = request.data.get('description')
    category_name = request.data.get('category')  # "Moteurs"
    stock = request.data.get('stock')        # 10
    image = request.FILES.get('image')
    
    # Validation basique HTTP
    if not name or not price:
        return Response({'detail': 'name and price required'}, status=400)
    
    """
    📤 ÉTAPE 2: Appeler le SERVICE
    """
    product_service = ProductService()
    product = product_service.create_product_for_shop(
        shop=shop,
        name=name,
        price=price,
        description=description,
        category_name=category_name,
        stock=stock,
        image=image
    )
    
    """
    📤 ÉTAPE 3: Retourner la réponse HTTP
    """
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data, status=201)
```

---

#### **3️⃣ SERVICE valide et traite les données**

```python
# shop/services/product_service.py
class ProductService:
    def create_product_for_shop(self, shop, name, price, ...):
        """
        🧠 ÉTAPE 2: Logique métier
        """
        
        # Validation 1: Le nom ne peut pas être vide
        if not name or not name.strip():
            raise ValidationError("Le nom du produit est requis")
            # ↑ Le VIEW reçoit cette erreur et la retourne avec status 400
        
        # Validation 2: Prix positif
        if price <= 0:
            raise ValidationError("Le prix doit être > 0")
        
        # Validation 3: Stock valide
        if stock < 0:
            raise ValidationError("Le stock ne peut pas être négatif")
        
        # Logique métier: Formater le nom
        name = name.strip().title()  # "moteur v8" → "Moteur V8"
        
        # Logique métier: Créer la catégorie si elle n'existe pas
        category = self._get_or_create_category(category_name)
        
        # Appeler le Model pour sauvegarder
        product = Product.objects.create(
            shop=shop,
            name=name,           # "Moteur V8" (formaté)
            price=price,         # 5000 (validé)
            description=description,
            category=category,   # Category(name="Moteurs") (créée si nécessaire)
            stock=stock,         # 10 (validé)
            image=image
        )
        
        return product
```

---

#### **4️⃣ MODEL stocke les données**

```python
# shop/models.py
class Product(models.Model):
    """
    💾 ÉTAPE 3: Stocker dans la BDD
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    stock = models.IntegerField(default=1)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

# Base de données (PostgreSQL/SQLite)
# ┌──────────────────────────────────────┐
# │ shop_product                         │
# ├──────────────────────────────────────┤
# │ id | name        | price | stock    │
# │ 1  | Moteur V8   | 5000  | 10       │
# └──────────────────────────────────────┘
```

---

#### **5️⃣ VIEW retourne la réponse HTTP**

```python
# Response au Frontend
{
    "id": 1,
    "name": "Moteur V8",
    "price": "5000.00",
    "description": "Moteur haute performance",
    "category": "Moteurs",
    "stock": 10,
    "image_url": "/media/products/moteur.jpg",
    "created_at": "2026-02-04T10:30:00Z"
}
```

---

## 🎨 Comparaison: BON vs MAUVAIS

### **❌ MAUVAIS Architecture (Tout dans le Model)**

```python
# ❌ ANTI-PATTERN
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def create_with_validation(self, shop, name, price, ...):
        # ❌ Logique métier dans le Model
        if not name:
            raise Exception("Name required")
        if price <= 0:
            raise Exception("Price must be positive")
        if not shop.is_active:
            raise Exception("Shop not active")
        # ❌ Accès à la BDD directement
        category = Category.objects.get_or_create(name=...)
        # ❌ Trop de responsabilités!
```

**Problèmes:**
- 🔴 Difficile à tester (couplé à la BDD)
- 🔴 Logique métier mélangée à la structure de données
- 🔴 Impossible de réutiliser la logique ailleurs
- 🔴 Vue trop grosse et compliquée

---

### **✅ BON Architecture (MVC + Service)**

```python
# ✅ MODEL: Structure uniquement
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

# ✅ SERVICE: Logique métier
class ProductService:
    def create_product_for_shop(self, shop, name, price, category_name, ...):
        if not name or not name.strip():
            raise ValidationError("Name required")
        if price <= 0:
            raise ValidationError("Price must be positive")
        if not shop.is_active:
            raise ValidationError("Shop not active")
        
        category = Category.objects.get_or_create(name=category_name or 'Autre')
        return Product.objects.create(shop=shop, name=name, price=price, ...)

# ✅ VIEW: Gestion HTTP uniquement
@api_view(['POST'])
def create_product_api(request):
    name = request.data.get('name')
    price = request.data.get('price')
    
    try:
        service = ProductService()
        product = service.create_product_for_shop(
            shop=request.user.shop,
            name=name,
            price=price,
            ...
        )
        return Response(ProductSerializer(product).data, status=201)
    except ValidationError as e:
        return Response({'detail': str(e)}, status=400)
```

**Avantages:**
- ✅ Code modulaire et réutilisable
- ✅ Facile à tester (chaque couche indépendante)
- ✅ Séparation claire des responsabilités
- ✅ Logique métier indépendante de l'HTTP
- ✅ Facile de changer le framework HTTP

---

## 📚 Résumé: Qui fait Quoi ?

| Couche | Fichier | Responsabilités | Exemple |
|--------|---------|-----------------|---------|
| **MODEL** | `shop/models.py` | Structure données, tables BDD | `class Product(models.Model)` |
| **SERVICE** | `services/product_service.py` | Logique métier, validation | `ProductService.create_product_for_shop()` |
| **VIEW** | `shop/views.py` | Requête HTTP → Response HTTP | `@api_view(['POST']) def create_product_api()` |

---

## 🔗 Flux Récapitulatif

```
Frontend (TypeScript/React)
    │
    ├─ Envoie: POST /api/shop/create/ avec {name, price, ...}
    │
    ▼
VIEW (create_product_api)
    │
    ├─ Extrait: name = request.data.get('name')
    ├─ Appelle: ProductService.create_product_for_shop(...)
    │
    ▼
SERVICE (ProductService)
    │
    ├─ Valide: if price <= 0: raise ValidationError
    ├─ Logique: name = name.strip().title()
    ├─ Crée: category = Category.objects.get_or_create(...)
    ├─ Retourne: Product object
    │
    ▼
MODEL (Product)
    │
    └─ Stocke dans la BDD (PostgreSQL/SQLite)

    ▼
Response HTTP
    │
    └─ Retourne JSON au Frontend: {id, name, price, ...}
```

---

## 💡 Points Clés à Retenir

✅ **MODEL** = Structure (pas de logique)
✅ **SERVICE** = Logique métier (pas d'HTTP, pas de BDD directe)
✅ **VIEW** = Requête/Réponse HTTP (pas de logique métier)
✅ **Chaque couche a UNE responsabilité**
✅ **Les données circulent toujours de la même façon: VIEW → SERVICE → MODEL**
✅ **Les erreurs remontent: MODEL → SERVICE → VIEW → Frontend**
