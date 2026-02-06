# 🏭 Pattern Factory - Shopina

## 📖 Qu'est-ce que le Factory Pattern?

Le **Factory Pattern** est un pattern de conception qui crée des objets **sans exposer la logique de création**. Au lieu de faire `new ClassName()`, on utilise une "factory" (usine) qui décide quelle classe créer.

```
❌ MAUVAIS (Direct instantiation):
    Product p = new Product()

✅ BON (Factory):
    Product p = ProductFactory.create()
                  ↑
            L'usine décide quoi créer
```

---

## 🎯 Pourquoi Factory?

| Problème | Solution Factory |
|----------|-----------------|
| Logique création compliquée | Factory la centralise |
| Création en plusieurs étapes | Factory gère toutes les étapes |
| Décision selon le type | Factory choisit le type |
| Difficile de changer | Change dans une seule place |
| Code répété partout | Code réutilisable |

---

## 📋 Types de Factory

```
Factory Patterns:

1. Simple Factory (Statique)
   ProductFactory.create(type) → Product

2. Factory Method
   class Product { abstract create() }
   → SubclassProduit { create() }

3. Abstract Factory
   ProductFactory / CategoryFactory
   → Interface commune
```

---

## 🔧 Factory dans Shopina

### 1️⃣ ProductFactory (Simple Factory)

**Objectif:** Créer des produits avec toute la logique compliquée.

```python
# shop/factories/product_factory.py (À créer)

class ProductFactory:
    """Factory pour créer des produits complètement configurés."""
    
    @staticmethod
    def create(shop, name, price, category_name='Autre', stock=1, image=None):
        """
        Factory pour créer un Product avec logique centralisée.
        
        Étapes:
        1. Valide les données
        2. Formate le nom
        3. Crée/récupère la catégorie
        4. Crée le produit
        5. Retourne le produit créé
        """
        
        # ✅ ÉTAPE 1: Valider les données
        if not name or not name.strip():
            raise ValueError("Le nom du produit est requis")
        
        if price <= 0:
            raise ValueError("Le prix doit être positif")
        
        if stock < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        
        # ✅ ÉTAPE 2: Formater
        name = name.strip().title()  # "moteur v8" → "Moteur V8"
        
        # ✅ ÉTAPE 3: Créer la catégorie si elle n'existe pas
        category, created = Category.objects.get_or_create(
            name=category_name or 'Autre'
        )
        
        # ✅ ÉTAPE 4: Créer le produit
        product = Product.objects.create(
            shop=shop,
            name=name,
            price=price,
            category=category,
            stock=stock,
            image=image,
            slug=ProductFactory._generate_slug(name)
        )
        
        return product
    
    @staticmethod
    def _generate_slug(name):
        """Génère un slug à partir du nom."""
        return name.lower().replace(' ', '-').replace('é', 'e')
    
    @staticmethod
    def create_variant_product(shop, base_product, variant_name, variant_price):
        """Factory pour créer une variante de produit."""
        return Product.objects.create(
            shop=shop,
            name=f"{base_product.name} - {variant_name}",
            price=variant_price,
            category=base_product.category,
            parent=base_product,  # Liaison à la variante parente
            image=base_product.image
        )
```

---

### 2️⃣ ShopFactory (Factory avec Logique Métier)

```python
# shops/factories/shop_factory.py (À créer)

from shops.models import Shop

class ShopFactory:
    """Factory pour créer des boutiques avec configuration complète."""
    
    @staticmethod
    def create(user, name, description=''):
        """
        Factory pour créer une Shop complètement configurée.
        
        Logique:
        1. Valide l'utilisateur
        2. Génère le slug unique
        3. Crée la boutique
        4. Configura les paramètres par défaut
        5. Retourne la boutique
        """
        
        # ✅ Valider
        if not user:
            raise ValueError("Utilisateur requis")
        
        if not name or not name.strip():
            raise ValueError("Nom de la boutique requis")
        
        # Vérifier si l'utilisateur a déjà une boutique
        if Shop.objects.filter(owner=user).exists():
            raise ValueError("Vous avez déjà une boutique")
        
        # ✅ Générer slug unique
        slug = ShopFactory._generate_unique_slug(name)
        
        # ✅ Créer la boutique
        shop = Shop.objects.create(
            owner=user,
            name=name,
            description=description,
            slug=slug,
            is_active=True,  # Activation automatique
            rating=0.0,
            followers_count=0
        )
        
        # ✅ Logger
        print(f"✅ Shop créée: {shop.name} ({shop.slug})")
        
        return shop
    
    @staticmethod
    def _generate_unique_slug(name):
        """Génère un slug unique en ajoutant un numéro si nécessaire."""
        import re
        
        slug = re.sub(r'[^\w\s-]', '', name).lower()
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        base_slug = slug
        counter = 1
        
        # Vérifier l'unicité
        while Shop.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
```

---

### 3️⃣ SerializerFactory (Factory pour Serializers)

```python
# shop/factories/serializer_factory.py (À créer)

from shop.serializers import (
    ProductSerializer, 
    CategorySerializer, 
    AnnouncementSerializer
)

class SerializerFactory:
    """Factory pour créer les bons serializers selon le contexte."""
    
    # Mapping: Modèle → Serializer
    SERIALIZERS = {
        'product': ProductSerializer,
        'category': CategorySerializer,
        'announcement': AnnouncementSerializer,
    }
    
    @staticmethod
    def get_serializer(model_type, instance=None, context=None):
        """
        Factory pour récupérer le bon serializer.
        
        Usage:
        serializer = SerializerFactory.get_serializer('product', product, {'request': request})
        """
        
        serializer_class = SerializerFactory.SERIALIZERS.get(model_type)
        
        if not serializer_class:
            raise ValueError(f"Serializer non trouvé pour: {model_type}")
        
        if instance:
            return serializer_class(instance, context=context or {})
        
        return serializer_class(context=context or {})
    
    @staticmethod
    def get_list_serializer(model_type, instances, context=None):
        """Factory pour sérialiser une liste."""
        serializer_class = SerializerFactory.SERIALIZERS.get(model_type)
        
        if not serializer_class:
            raise ValueError(f"Serializer non trouvé pour: {model_type}")
        
        return serializer_class(instances, many=True, context=context or {})
```

---

## 📝 Exemples Concrets d'Utilisation

### Exemple 1: Créer un Produit avec Factory

**AVANT (sans factory - code répété partout):**

```python
# shop/views.py
@api_view(['POST'])
def create_product_api(request):
    name = request.data.get('name')
    price = request.data.get('price')
    category = request.data.get('category')
    stock = request.data.get('stock', 1)
    
    # ❌ Logique de création dans le VIEW!
    if not name or not name.strip():
        return Response({'detail': 'Name required'}, status=400)
    if price <= 0:
        return Response({'detail': 'Price > 0'}, status=400)
    if stock < 0:
        return Response({'detail': 'Stock >= 0'}, status=400)
    
    name = name.strip().title()
    cat, _ = Category.objects.get_or_create(name=category or 'Autre')
    
    product = Product.objects.create(
        shop=request.user.shop,
        name=name,
        price=price,
        category=cat,
        stock=stock
    )
    
    # ❌ Même logique répétée dans d'autres endpoints
```

**APRÈS (avec factory - centralisé):**

```python
# shop/factories/product_factory.py
class ProductFactory:
    @staticmethod
    def create(shop, name, price, category_name='Autre', stock=1, image=None):
        # ✅ TOUTE LA LOGIQUE EST ICI
        if not name or not name.strip():
            raise ValueError("Name required")
        if price <= 0:
            raise ValueError("Price > 0")
        if stock < 0:
            raise ValueError("Stock >= 0")
        
        name = name.strip().title()
        category, _ = Category.objects.get_or_create(name=category_name or 'Autre')
        
        return Product.objects.create(
            shop=shop,
            name=name,
            price=price,
            category=category,
            stock=stock,
            image=image
        )

# shop/views.py
@api_view(['POST'])
def create_product_api(request):
    name = request.data.get('name')
    price = request.data.get('price')
    category = request.data.get('category')
    stock = request.data.get('stock', 1)
    image = request.FILES.get('image')
    
    try:
        # ✅ UTILISE LA FACTORY
        product = ProductFactory.create(
            shop=request.user.shop,
            name=name,
            price=price,
            category_name=category,
            stock=stock,
            image=image
        )
        
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)
```

---

### Exemple 2: ShopFactory

**Sans Factory:**

```python
# ❌ Logique répétée
def create_shop(user, name):
    if Shop.objects.filter(owner=user).exists():
        return Response({'detail': 'Vous avez déjà une boutique'}, status=400)
    
    slug = name.lower().replace(' ', '-')
    counter = 1
    while Shop.objects.filter(slug=slug).exists():
        slug = f"{name.lower().replace(' ', '-')}-{counter}"
        counter += 1
    
    shop = Shop.objects.create(
        owner=user,
        name=name,
        slug=slug,
        is_active=True
    )
    return shop
```

**Avec Factory:**

```python
# ✅ Centralisé et réutilisable
def create_shop(user, name):
    try:
        shop = ShopFactory.create(user=user, name=name)
        return Response(ShopSerializer(shop).data, status=201)
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)

# ✅ RÉUTILISABLE AILLEURS
# Dans un signal, un job async, un script d'admin, etc.
shop = ShopFactory.create(user=user, name=name)
```

---

### Exemple 3: SerializerFactory

**Sans Factory:**

```python
# ❌ Beaucoup de if/else
@api_view(['GET'])
def get_resource(request, resource_type, resource_id):
    if resource_type == 'product':
        obj = Product.objects.get(id=resource_id)
        serializer = ProductSerializer(obj, context={'request': request})
    elif resource_type == 'category':
        obj = Category.objects.get(id=resource_id)
        serializer = CategorySerializer(obj, context={'request': request})
    elif resource_type == 'announcement':
        obj = Announcement.objects.get(id=resource_id)
        serializer = AnnouncementSerializer(obj, context={'request': request})
    
    return Response(serializer.data)
```

**Avec Factory:**

```python
# ✅ Propre et extensible
@api_view(['GET'])
def get_resource(request, resource_type, resource_id):
    from shop.factories.serializer_factory import SerializerFactory
    
    # Récupérer l'objet
    models = {'product': Product, 'category': Category, 'announcement': Announcement}
    model = models.get(resource_type)
    obj = model.objects.get(id=resource_id)
    
    # ✅ LA FACTORY CHOISIT LE BON SERIALIZER
    serializer = SerializerFactory.get_serializer(
        resource_type, 
        obj, 
        context={'request': request}
    )
    
    return Response(serializer.data)
```

---

## 🏗️ Structure Factory dans Shopina

```
shopina-env/backend/
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── factories/           ← NOUVEAU
│       ├── __init__.py
│       ├── product_factory.py
│       └── serializer_factory.py
├── shops/
│   ├── models.py
│   └── factories/           ← NOUVEAU
│       ├── __init__.py
│       └── shop_factory.py
└── core/
    └── utils/
        └── exceptions.py
```

---

## 📊 Flux avec Factory

```
Frontend
   ↓
View
   ├─ Extrait les données
   ├─ Appelle: Factory.create(...)    ← Factory Pattern!
   │             ↓
   │         Factory
   │         ├─ Valide
   │         ├─ Formate
   │         ├─ Crée objets dépendants
   │         ├─ Retourne: Object
   │         ↑
   ├─ Reçoit l'objet
   └─ Retourne Response

Database
```

---

## ✅ Avantages Factory

| Avantage | Description |
|----------|-------------|
| **Centralisé** | Logique création en UN endroit |
| **Réutilisable** | Utilisable partout (views, jobs, scripts) |
| **Testable** | Facile de tester la factory |
| **Maintenable** | Changement = une seule place |
| **Flexible** | Ajouter logique sans changer views |
| **Scalable** | Ajouter types sans complexifier code |

---

## 🔄 Cycle Complet avec Factory

```
FRONTEND
   ↓ POST /api/shop/create/
   │ { name: "Belaid Auto" }
   ↓
VIEW (create_product_api)
   ├─ name = request.data.get('name')
   ├─ price = request.data.get('price')
   ├─ category = request.data.get('category')
   │
   │ ✅ UTILISE FACTORY
   ├─ product = ProductFactory.create(
   │    shop=request.user.shop,
   │    name=name,
   │    price=price,
   │    category_name=category
   │ )
   │
   ├─ serializer = ProductSerializer(product)
   └─ return Response(serializer.data, 201)
      ↑ Factory a géré TOUTE la logique
        de création!
```

---

## 💡 Quand Utiliser Factory?

✅ **Utilise Factory quand:**
- Création complexe (plusieurs étapes)
- Logique répétée partout
- Besoin de validation
- Objets dépendants à créer
- Différents types à créer

❌ **Ne pas utiliser Factory quand:**
- Simple `new Object()`
- Aucune logique
- Une seule utilisation

---

## 🎯 Résumé

| Concept | Explication |
|---------|------------|
| **Factory Pattern** | Crée des objets sans exposer la logique |
| **Simple Factory** | Classe statique avec méthodes `create()` |
| **Avantage 1** | Logique centralisée |
| **Avantage 2** | Réutilisable partout |
| **Avantage 3** | Facile à tester |
| **Exemple 1** | `ProductFactory.create(shop, name, price)` |
| **Exemple 2** | `ShopFactory.create(user, name)` |
| **Exemple 3** | `SerializerFactory.get_serializer(type)` |

La Factory, c'est une **"usine"** qui fabrique les objets correctement! 🏭
