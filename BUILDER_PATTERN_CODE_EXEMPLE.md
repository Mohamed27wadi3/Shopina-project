# 🏗️ Builder Pattern - Guide Complet avec Code

## 📖 Qu'est-ce que le Builder Pattern?

Le **Builder Pattern** construit des objets complexes **étape par étape**. Au lieu de passer 10+ paramètres au constructeur, on utilise un "builder" qui construit l'objet progressivement.

```
❌ SANS BUILDER (Constructeur surchargé):
    Product(name, price, desc, cat, stock, img, var, tags, meta, ...)
    ↑ Difficile à lire, beaucoup de params

✅ AVEC BUILDER (Construction fluide):
    ProductBuilder()
        .set_name("Moteur V8")
        .set_price(5000)
        .set_category("Moteurs")
        .set_stock(10)
        .build()
    ↑ Lisible, flexible, étapes claires
```

---

## 🎯 Pourquoi Builder?

| Problème | Solution Builder |
|----------|-----------------|
| Trop de paramètres au constructeur | Construction étape par étape |
| Paramètres optionnels nombreux | Seulement ce qui est nécessaire |
| Ordre des paramètres confus | Méthodes explicites |
| Validation complexe | Valider à chaque étape |
| Objets immutables | Construction puis build final |

---

## 🏗️ Structure du Builder Pattern

```
Director (Optionnel)
   ↓
Builder (Interface)
   ├─ set_name()
   ├─ set_price()
   ├─ set_category()
   └─ build() → Product
      │
      ├─ SimpleProductBuilder
      ├─ ComplexProductBuilder
      └─ VariantProductBuilder
```

---

## 1️⃣ Builder Basique - ProductBuilder

```python
# shop/builders/product_builder.py

from shop.models import Product, Category
from decimal import Decimal
from typing import Optional

class ProductBuilder:
    """
    Builder pour construire un Product étape par étape.
    
    Usage:
        product = ProductBuilder()\\
            .set_name("Moteur V8")\\
            .set_price(5000)\\
            .set_category("Moteurs")\\
            .set_stock(10)\\
            .build()
    """
    
    def __init__(self):
        """Initialise les valeurs par défaut."""
        self._name: Optional[str] = None
        self._price: Optional[Decimal] = None
        self._description: str = ''
        self._category: Optional[Category] = None
        self._category_name: Optional[str] = None
        self._stock: int = 1
        self._image = None
        self._shop = None
        self._variants: list = []
        self._metadata: dict = {}
        self._tags: list = []
    
    # ==========================================
    # MÉTHODES DE CONSTRUCTION (Fluent API)
    # ==========================================
    
    def set_name(self, name: str):
        """Définit le nom du produit."""
        if not name or not name.strip():
            raise ValueError("Le nom ne peut pas être vide")
        self._name = name.strip().title()
        return self  # ✅ Retourne self pour chaînage
    
    def set_price(self, price: float):
        """Définit le prix du produit."""
        if price <= 0:
            raise ValueError("Le prix doit être positif")
        self._price = Decimal(str(price))
        return self
    
    def set_description(self, description: str):
        """Définit la description du produit."""
        self._description = description.strip()
        return self
    
    def set_category(self, category_name: str):
        """Définit la catégorie (créée si nécessaire)."""
        self._category_name = category_name
        return self
    
    def set_category_instance(self, category: Category):
        """Définit directement l'instance de catégorie."""
        self._category = category
        return self
    
    def set_stock(self, stock: int):
        """Définit le stock initial."""
        if stock < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        self._stock = stock
        return self
    
    def set_image(self, image):
        """Définit l'image du produit."""
        self._image = image
        return self
    
    def set_shop(self, shop):
        """Définit la boutique propriétaire."""
        if not shop:
            raise ValueError("La boutique est requise")
        self._shop = shop
        return self
    
    def add_variant(self, name: str, price: float, stock: int = 1):
        """Ajoute une variante du produit."""
        self._variants.append({
            'name': name,
            'price': Decimal(str(price)),
            'stock': stock
        })
        return self
    
    def add_metadata(self, key: str, value):
        """Ajoute des métadonnées."""
        self._metadata[key] = value
        return self
    
    def add_tag(self, tag: str):
        """Ajoute un tag."""
        self._tags.append(tag)
        return self
    
    # ==========================================
    # MÉTHODE BUILD (Construction finale)
    # ==========================================
    
    def build(self) -> Product:
        """
        Construit et retourne le produit final.
        
        Returns:
            Product instance
            
        Raises:
            ValueError: Si données manquantes ou invalides
        """
        # Validation finale
        self._validate()
        
        # Créer/récupérer la catégorie si nécessaire
        if self._category_name and not self._category:
            self._category, _ = Category.objects.get_or_create(
                name=self._category_name
            )
        
        # Construire le produit
        product = Product.objects.create(
            name=self._name,
            price=self._price,
            description=self._description,
            category=self._category,
            stock=self._stock,
            shop=self._shop,
            image=self._image,
            metadata=self._metadata if self._metadata else None
        )
        
        # Ajouter les tags (si votre modèle les supporte)
        # product.tags.set(self._tags)
        
        print(f"✅ Produit construit: {product.name}")
        return product
    
    def _validate(self):
        """Valide que toutes les données requises sont présentes."""
        if not self._name:
            raise ValueError("Le nom est requis")
        
        if not self._price:
            raise ValueError("Le prix est requis")
        
        if not self._shop:
            raise ValueError("La boutique est requise")
    
    # ==========================================
    # MÉTHODES UTILITAIRES
    # ==========================================
    
    def reset(self):
        """Réinitialise le builder pour construire un nouveau produit."""
        self.__init__()
        return self
    
    def clone(self):
        """Crée une copie du builder actuel."""
        new_builder = ProductBuilder()
        new_builder._name = self._name
        new_builder._price = self._price
        new_builder._description = self._description
        new_builder._category = self._category
        new_builder._stock = self._stock
        new_builder._shop = self._shop
        new_builder._image = self._image
        new_builder._metadata = self._metadata.copy()
        new_builder._tags = self._tags.copy()
        return new_builder
```

---

## 2️⃣ Builder Avancé - Avec Director

```python
# shop/builders/product_director.py

from shop.builders.product_builder import ProductBuilder

class ProductDirector:
    """
    Director qui orchestre la construction de produits.
    Contient des "recettes" prédéfinies pour construire des produits.
    """
    
    def __init__(self, builder: ProductBuilder):
        self._builder = builder
    
    # ==========================================
    # RECETTES DE CONSTRUCTION
    # ==========================================
    
    def build_physical_product(self, shop, name: str, price: float, 
                              weight: float, dimensions: str):
        """
        Construit un produit physique avec tous les attributs nécessaires.
        """
        return (self._builder
            .set_shop(shop)
            .set_name(name)
            .set_price(price)
            .add_metadata('weight', weight)
            .add_metadata('dimensions', dimensions)
            .add_metadata('requires_shipping', True)
            .add_metadata('product_type', 'PHYSICAL')
            .add_tag('physical')
            .build())
    
    def build_digital_product(self, shop, name: str, price: float, 
                             file_url: str, file_size: str):
        """
        Construit un produit numérique.
        """
        return (self._builder
            .set_shop(shop)
            .set_name(name)
            .set_price(price)
            .set_stock(9999)  # Stock illimité
            .add_metadata('file_url', file_url)
            .add_metadata('file_size', file_size)
            .add_metadata('requires_shipping', False)
            .add_metadata('instant_delivery', True)
            .add_metadata('product_type', 'DIGITAL')
            .add_tag('digital')
            .add_tag('downloadable')
            .build())
    
    def build_subscription_product(self, shop, name: str, price: float,
                                  billing_period: str = 'MONTHLY'):
        """
        Construit un produit d'abonnement.
        """
        return (self._builder
            .set_shop(shop)
            .set_name(name)
            .set_price(price)
            .set_stock(9999)
            .add_metadata('billing_period', billing_period)
            .add_metadata('is_recurring', True)
            .add_metadata('auto_renewal', True)
            .add_metadata('product_type', 'SUBSCRIPTION')
            .add_tag('subscription')
            .add_tag('recurring')
            .build())
    
    def build_bundle_product(self, shop, name: str, price: float,
                           included_products: list):
        """
        Construit un pack/bundle de produits.
        """
        return (self._builder
            .set_shop(shop)
            .set_name(name)
            .set_price(price)
            .add_metadata('included_products', included_products)
            .add_metadata('is_bundle', True)
            .add_metadata('product_type', 'BUNDLE')
            .add_tag('bundle')
            .add_tag('pack')
            .build())
```

---

## 3️⃣ Utilisation dans les Views

```python
# shop/views.py

from shop.builders.product_builder import ProductBuilder
from shop.builders.product_director import ProductDirector
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# ==========================================
# OPTION 1: Utiliser le Builder directement
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_with_builder(request):
    """Crée un produit en utilisant le Builder Pattern."""
    
    try:
        # ✅ BUILDER PATTERN: Construction étape par étape
        product = (ProductBuilder()
            .set_shop(request.user.shop)
            .set_name(request.data.get('name'))
            .set_price(request.data.get('price'))
            .set_description(request.data.get('description', ''))
            .set_category(request.data.get('category'))
            .set_stock(request.data.get('stock', 1))
            .set_image(request.FILES.get('image'))
            .build())
        
        from shop.serializers import ProductSerializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)


# ==========================================
# OPTION 2: Avec variantes
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_with_variants(request):
    """Crée un produit avec des variantes."""
    
    try:
        builder = ProductBuilder()
        
        # Base product
        builder.set_shop(request.user.shop)\\
               .set_name(request.data.get('name'))\\
               .set_price(request.data.get('price'))\\
               .set_category(request.data.get('category'))
        
        # Ajouter variantes
        variants = request.data.get('variants', [])
        for variant in variants:
            builder.add_variant(
                name=variant['name'],
                price=variant['price'],
                stock=variant.get('stock', 1)
            )
        
        # Ajouter métadonnées
        builder.add_metadata('has_variants', True)\\
               .add_metadata('variant_count', len(variants))
        
        # Construire
        product = builder.build()
        
        from shop.serializers import ProductSerializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)


# ==========================================
# OPTION 3: Avec Director (Recommandé!)
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_advanced(request):
    """Crée un produit en utilisant le Director."""
    
    try:
        product_type = request.data.get('product_type', 'PHYSICAL')
        
        # ✅ BUILDER + DIRECTOR PATTERN
        builder = ProductBuilder()
        director = ProductDirector(builder)
        
        if product_type == 'PHYSICAL':
            product = director.build_physical_product(
                shop=request.user.shop,
                name=request.data.get('name'),
                price=request.data.get('price'),
                weight=request.data.get('weight', 0),
                dimensions=request.data.get('dimensions', '')
            )
        
        elif product_type == 'DIGITAL':
            product = director.build_digital_product(
                shop=request.user.shop,
                name=request.data.get('name'),
                price=request.data.get('price'),
                file_url=request.data.get('file_url'),
                file_size=request.data.get('file_size', '')
            )
        
        elif product_type == 'SUBSCRIPTION':
            product = director.build_subscription_product(
                shop=request.user.shop,
                name=request.data.get('name'),
                price=request.data.get('price'),
                billing_period=request.data.get('billing_period', 'MONTHLY')
            )
        
        elif product_type == 'BUNDLE':
            product = director.build_bundle_product(
                shop=request.user.shop,
                name=request.data.get('name'),
                price=request.data.get('price'),
                included_products=request.data.get('included_products', [])
            )
        
        else:
            return Response({'detail': 'Type de produit invalide'}, status=400)
        
        from shop.serializers import ProductSerializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)
```

---

## 4️⃣ Utilisation Côté Frontend

```typescript
// src/pages/MyShopPage.tsx

// ✅ CRÉER PRODUIT SIMPLE
const handleAddSimpleProduct = async () => {
    const response = await fetch(`${API_BASE}/api/shop/create-builder/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: 'Moteur V8',
            price: 5000,
            description: 'Moteur haute performance',
            category: 'Moteurs',
            stock: 10
        })
    });
};

// ✅ CRÉER PRODUIT AVEC VARIANTES
const handleAddProductWithVariants = async () => {
    const response = await fetch(`${API_BASE}/api/shop/create-variants/`, {
        method: 'POST',
        body: JSON.stringify({
            name: 'T-Shirt Shopina',
            price: 29.99,
            category: 'Vêtements',
            variants: [
                { name: 'T-Shirt Shopina - S', price: 29.99, stock: 10 },
                { name: 'T-Shirt Shopina - M', price: 29.99, stock: 15 },
                { name: 'T-Shirt Shopina - L', price: 32.99, stock: 8 }
            ]
        })
    });
};

// ✅ CRÉER PRODUIT NUMÉRIQUE
const handleAddDigitalProduct = async () => {
    const response = await fetch(`${API_BASE}/api/shop/create-advanced/`, {
        method: 'POST',
        body: JSON.stringify({
            product_type: 'DIGITAL',
            name: 'Ebook - Guide Mécanique',
            price: 29.99,
            file_url: 'https://cdn.example.com/ebooks/guide.pdf',
            file_size: '5.2MB'
        })
    });
};
```

---

## 5️⃣ Flux Complet avec Builder

```
Frontend
   ↓
POST /api/shop/create-builder/
   │ { name: "Moteur V8", price: 5000, category: "Moteurs", stock: 10 }
   ↓
VIEW: create_product_with_builder()
   ├─ ProductBuilder()
   │  ├─ .set_shop(request.user.shop)
   │  ├─ .set_name("Moteur V8")
   │  ├─ .set_price(5000)
   │  ├─ .set_category("Moteurs")
   │  ├─ .set_stock(10)
   │  └─ .build() ← Construit le produit final
   │      ├─ _validate() ← Validation
   │      ├─ Category.objects.get_or_create()
   │      └─ Product.objects.create()
   └─ Response: {"id": 1, "name": "Moteur V8", ...}

VS (Director)

POST /api/shop/create-advanced/
   │ { product_type: "DIGITAL", name: "Ebook", ... }
   ↓
VIEW: create_product_advanced()
   ├─ ProductBuilder()
   ├─ ProductDirector(builder)
   ├─ director.build_digital_product(...)
   │  ├─ builder.set_shop()
   │  ├─ builder.set_name()
   │  ├─ builder.set_price()
   │  ├─ builder.set_stock(9999)
   │  ├─ builder.add_metadata('file_url', ...)
   │  ├─ builder.add_metadata('instant_delivery', True)
   │  └─ builder.build()
   └─ Response
```

---

## 6️⃣ Comparaison: Builder vs Constructeur

### ❌ SANS BUILDER (Constructeur surchargé)

```python
# ❌ Difficile à lire, ordre confus
product = Product(
    'Moteur V8',           # name
    5000,                  # price
    'Description',         # description
    category,              # category
    10,                    # stock
    shop,                  # shop
    image,                 # image
    {'weight': 150},       # metadata
    ['physical', 'auto'],  # tags
    True,                  # is_active
    False,                 # is_featured
)

# ❌ Que se passe-t-il si on veut omettre certains params?
product = Product('Moteur', 5000, '', None, 0, shop, None, {}, [], True, False)
                                    ↑ Beaucoup de None/defaults
```

### ✅ AVEC BUILDER (Construction fluide)

```python
# ✅ Lisible, flexible, explicite
product = (ProductBuilder()
    .set_name('Moteur V8')
    .set_price(5000)
    .set_shop(shop)
    .set_stock(10)
    .set_category('Moteurs')
    .add_metadata('weight', 150)
    .add_tag('physical')
    .add_tag('auto')
    .build())

# ✅ Omettre des params? Pas de problème!
product = (ProductBuilder()
    .set_name('Moteur V8')
    .set_price(5000)
    .set_shop(shop)
    .build())  # Tout le reste = valeurs par défaut
```

---

## 7️⃣ Avantages du Builder Pattern

| Avantage | Description |
|----------|-------------|
| **Lisibilité** | Code self-documented (set_name au lieu de param 1) |
| **Flexibilité** | Ordre des appels importe peu |
| **Paramètres optionnels** | Seulement ce qui est nécessaire |
| **Validation** | À chaque étape + finale |
| **Réutilisabilité** | Recettes via Director |
| **Immutabilité** | Build final crée l'objet |
| **Maintenance** | Ajouter attribut = ajouter méthode |

---

## 8️⃣ Tests Unitaires

```python
# shop/tests/test_product_builder.py

from django.test import TestCase
from shop.builders.product_builder import ProductBuilder
from shop.builders.product_director import ProductDirector
from shops.models import Shop
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductBuilderTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.shop = Shop.objects.create(owner=self.user, name='Test', slug='test')
    
    def test_build_simple_product(self):
        """Test construction d'un produit simple."""
        product = (ProductBuilder()
            .set_shop(self.shop)
            .set_name('Moteur')
            .set_price(5000)
            .build())
        
        self.assertEqual(product.name, 'Moteur')
        self.assertEqual(product.price, 5000)
        self.assertEqual(product.stock, 1)  # Default
    
    def test_build_product_with_variants(self):
        """Test construction avec variantes."""
        builder = ProductBuilder()
        product = (builder
            .set_shop(self.shop)
            .set_name('T-Shirt')
            .set_price(29.99)
            .add_variant('S', 29.99, 10)
            .add_variant('M', 29.99, 15)
            .add_variant('L', 32.99, 8)
            .build())
        
        self.assertEqual(len(builder._variants), 3)
    
    def test_director_physical_product(self):
        """Test Director pour produit physique."""
        builder = ProductBuilder()
        director = ProductDirector(builder)
        
        product = director.build_physical_product(
            shop=self.shop,
            name='Moteur',
            price=5000,
            weight=150,
            dimensions='50x50x30'
        )
        
        self.assertEqual(product.metadata['weight'], 150)
        self.assertEqual(product.metadata['product_type'], 'PHYSICAL')
    
    def test_director_digital_product(self):
        """Test Director pour produit numérique."""
        builder = ProductBuilder()
        director = ProductDirector(builder)
        
        product = director.build_digital_product(
            shop=self.shop,
            name='Ebook',
            price=29.99,
            file_url='https://example.com/ebook.pdf',
            file_size='5MB'
        )
        
        self.assertEqual(product.stock, 9999)
        self.assertTrue(product.metadata['instant_delivery'])
    
    def test_builder_validation(self):
        """Test validation du builder."""
        builder = ProductBuilder()
        
        with self.assertRaises(ValueError):
            builder.set_name('')  # Nom vide
        
        with self.assertRaises(ValueError):
            builder.set_price(-100)  # Prix négatif
        
        with self.assertRaises(ValueError):
            builder.set_stock(-5)  # Stock négatif
    
    def test_builder_reset(self):
        """Test reset du builder."""
        builder = ProductBuilder()
        builder.set_name('Test').set_price(100)
        
        builder.reset()
        
        self.assertIsNone(builder._name)
        self.assertIsNone(builder._price)
    
    def test_builder_clone(self):
        """Test clonage du builder."""
        builder1 = (ProductBuilder()
            .set_name('Test')
            .set_price(100))
        
        builder2 = builder1.clone()
        
        self.assertEqual(builder2._name, 'Test')
        self.assertEqual(builder2._price, 100)
```

---

## 9️⃣ Structure du Projet

```
shopina-env/backend/
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── builders/               ← NOUVEAU DOSSIER
│   │   ├── __init__.py
│   │   ├── product_builder.py  ← Builder
│   │   └── product_director.py ← Director
│   └── tests/
│       └── test_product_builder.py
└── ...
```

---

## 🔟 Builder vs Factory

| | Builder | Factory |
|--|---------|---------|
| **But** | Construction étape par étape | Création instantanée |
| **Complexité** | Objet complexe, beaucoup de params | Objet simple/moyen |
| **Flexibilité** | Très flexible (optionnel) | Moins flexible |
| **Lisibilité** | Excellent (fluent API) | Bon |
| **Exemple** | `.set_name().set_price().build()` | `Factory.create(name, price)` |

---

## 💡 Résumé

**Builder Pattern = Construction progressive d'objets complexes** 🏗️

```python
# BUILDER: Construction fluide étape par étape
product = (ProductBuilder()
    .set_name("Moteur V8")
    .set_price(5000)
    .set_category("Moteurs")
    .set_stock(10)
    .add_metadata('weight', 150)
    .add_tag('physical')
    .build())

# DIRECTOR: Recettes prédéfinies
director = ProductDirector(ProductBuilder())
product = director.build_digital_product(shop, name, price, file_url, size)
```

Le Builder Pattern, c'est du **LEGO**: on assemble pièce par pièce! 🧱
