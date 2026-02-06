# 🏭 Factory Method Pattern - Code Concret

## 📖 Rappel: Factory Method vs Simple Factory

```
Simple Factory:
    ProductFactory.create() ← Une seule classe

Factory Method:
    Product.create() ← Chaque classe implémente sa création
    │
    ├─ PhysicalProduct.create()
    ├─ DigitalProduct.create()
    └─ SubscriptionProduct.create()
```

---

## 1️⃣ Exemple 1: Product Avec Factory Method

### Structure

```
Product (Classe abstraite)
  ├─ create() ← Chaque sous-classe l'implémente
  ├─ save()
  └─ validate()
      │
      ├─ PhysicalProduct
      │   └─ create() ← Crée un produit physique
      │
      ├─ DigitalProduct
      │   └─ create() ← Crée un produit numérique
      │
      └─ SubscriptionProduct
          └─ create() ← Crée un abonnement
```

### Code Python

```python
# shop/factories/product_factory.py

from abc import ABC, abstractmethod
from shop.models import Product, Category
from decimal import Decimal

# ==========================================
# 1️⃣ CLASSE ABSTRAITE (Interface)
# ==========================================

class ProductFactory(ABC):
    """
    Classe abstraite pour créer des produits.
    Chaque sous-classe implémente sa propre création.
    """
    
    @abstractmethod
    def create(self, shop, name, price, **kwargs):
        """
        Méthode abstraite: chaque sous-classe doit l'implémenter.
        Retourne: Product instance
        """
        pass
    
    @abstractmethod
    def validate(self, **kwargs):
        """Valide les données spécifiques au type de produit."""
        pass
    
    def _common_validation(self, shop, name, price):
        """Validation commune à tous les produits."""
        if not name or not name.strip():
            raise ValueError("Le nom du produit est requis")
        
        if price <= 0:
            raise ValueError("Le prix doit être positif")
        
        if not shop:
            raise ValueError("La boutique est requise")
        
        return name.strip().title(), Decimal(str(price))


# ==========================================
# 2️⃣ IMPLÉMENTATION 1: Produit Physique
# ==========================================

class PhysicalProductFactory(ProductFactory):
    """Factory pour créer des produits physiques (avec stock, poids, etc.)."""
    
    def create(self, shop, name, price, weight=0, dimensions=None, stock=1, image=None):
        """
        Crée un produit physique.
        
        Args:
            shop: Boutique propriétaire
            name: Nom du produit
            price: Prix
            weight: Poids en kg
            dimensions: Dimensions (L x l x H)
            stock: Quantité en stock
            image: Image du produit
        
        Returns:
            Product instance
        """
        
        # ✅ Valide les données communes
        name, price = self._common_validation(shop, name, price)
        
        # ✅ Valide les données spécifiques au produit physique
        self.validate(weight=weight, stock=stock)
        
        # ✅ Crée le produit avec des attributs physiques
        product = Product.objects.create(
            shop=shop,
            name=name,
            price=price,
            product_type='PHYSICAL',  # ← Type spécifique
            stock=stock,
            image=image,
            # Stocke les infos physiques en JSON
            metadata={
                'weight': weight,
                'dimensions': dimensions,
                'requires_shipping': True
            }
        )
        
        print(f"✅ Produit PHYSIQUE créé: {name}")
        return product
    
    def validate(self, weight=0, stock=1, **kwargs):
        """Validation spécifique aux produits physiques."""
        if weight < 0:
            raise ValueError("Le poids ne peut pas être négatif")
        
        if stock < 0:
            raise ValueError("Le stock ne peut pas être négatif")


# ==========================================
# 3️⃣ IMPLÉMENTATION 2: Produit Numérique
# ==========================================

class DigitalProductFactory(ProductFactory):
    """Factory pour créer des produits numériques (fichiers, licences, etc.)."""
    
    def create(self, shop, name, price, file_url, file_size=None, license_key=None):
        """
        Crée un produit numérique.
        
        Args:
            shop: Boutique propriétaire
            name: Nom du produit
            price: Prix
            file_url: URL du fichier à télécharger
            file_size: Taille du fichier
            license_key: Clé de licence (optionnel)
        
        Returns:
            Product instance
        """
        
        # ✅ Valide les données communes
        name, price = self._common_validation(shop, name, price)
        
        # ✅ Valide les données spécifiques au produit numérique
        self.validate(file_url=file_url)
        
        # ✅ Crée le produit numérique
        product = Product.objects.create(
            shop=shop,
            name=name,
            price=price,
            product_type='DIGITAL',  # ← Type spécifique
            stock=9999,  # Stock infini (produit numérique)
            # Stocke les infos numériques en JSON
            metadata={
                'file_url': file_url,
                'file_size': file_size,
                'license_key': license_key,
                'requires_shipping': False,
                'instant_delivery': True
            }
        )
        
        print(f"✅ Produit NUMÉRIQUE créé: {name}")
        return product
    
    def validate(self, file_url=None, **kwargs):
        """Validation spécifique aux produits numériques."""
        if not file_url or not file_url.strip():
            raise ValueError("L'URL du fichier est requise pour un produit numérique")
        
        if not file_url.startswith(('http://', 'https://')):
            raise ValueError("L'URL du fichier doit être valide")


# ==========================================
# 4️⃣ IMPLÉMENTATION 3: Abonnement
# ==========================================

class SubscriptionProductFactory(ProductFactory):
    """Factory pour créer des abonnements/produits récurrents."""
    
    def create(self, shop, name, price, billing_period='MONTHLY', duration=None):
        """
        Crée un produit d'abonnement.
        
        Args:
            shop: Boutique propriétaire
            name: Nom du produit
            price: Prix par période
            billing_period: 'MONTHLY', 'YEARLY', 'WEEKLY'
            duration: Durée en mois (None = illimité)
        
        Returns:
            Product instance
        """
        
        # ✅ Valide les données communes
        name, price = self._common_validation(shop, name, price)
        
        # ✅ Valide les données spécifiques à l'abonnement
        self.validate(billing_period=billing_period)
        
        # ✅ Crée le produit d'abonnement
        product = Product.objects.create(
            shop=shop,
            name=name,
            price=price,
            product_type='SUBSCRIPTION',  # ← Type spécifique
            stock=9999,  # Stock infini
            metadata={
                'billing_period': billing_period,
                'duration': duration,
                'is_recurring': True,
                'auto_renewal': True
            }
        )
        
        print(f"✅ Abonnement créé: {name} ({billing_period})")
        return product
    
    def validate(self, billing_period='MONTHLY', **kwargs):
        """Validation spécifique aux abonnements."""
        valid_periods = ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
        
        if billing_period not in valid_periods:
            raise ValueError(f"Période invalide. Doit être: {', '.join(valid_periods)}")


# ==========================================
# 5️⃣ FACTORY REGISTRY (Trouveur de factory)
# ==========================================

class ProductFactoryRegistry:
    """Registry pour retrouver la bonne factory selon le type."""
    
    # Mapping: type → factory class
    _factories = {
        'PHYSICAL': PhysicalProductFactory,
        'DIGITAL': DigitalProductFactory,
        'SUBSCRIPTION': SubscriptionProductFactory,
    }
    
    @staticmethod
    def get_factory(product_type):
        """Retourne la factory appropriée selon le type."""
        factory_class = ProductFactoryRegistry._factories.get(product_type)
        
        if not factory_class:
            raise ValueError(f"Type de produit inconnu: {product_type}")
        
        return factory_class()
    
    @staticmethod
    def register(product_type, factory_class):
        """Enregistre une nouvelle factory."""
        ProductFactoryRegistry._factories[product_type] = factory_class
```

---

## 2️⃣ Comment Utiliser dans les Views

```python
# shop/views.py

from shop.factories.product_factory import (
    PhysicalProductFactory,
    DigitalProductFactory,
    SubscriptionProductFactory,
    ProductFactoryRegistry
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# ==========================================
# OPTION 1: Utiliser directement
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_physical_product(request):
    """Endpoint pour créer un produit physique."""
    
    try:
        # ✅ Crée la factory
        factory = PhysicalProductFactory()
        
        # ✅ Appelle create() avec les données spécifiques
        product = factory.create(
            shop=request.user.shop,
            name=request.data.get('name'),
            price=request.data.get('price'),
            weight=request.data.get('weight', 0),
            dimensions=request.data.get('dimensions'),
            stock=request.data.get('stock', 1),
            image=request.FILES.get('image')
        )
        
        from shop.serializers import ProductSerializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_digital_product(request):
    """Endpoint pour créer un produit numérique."""
    
    try:
        # ✅ Crée la factory
        factory = DigitalProductFactory()
        
        # ✅ Appelle create() avec les données spécifiques
        product = factory.create(
            shop=request.user.shop,
            name=request.data.get('name'),
            price=request.data.get('price'),
            file_url=request.data.get('file_url'),
            file_size=request.data.get('file_size'),
            license_key=request.data.get('license_key')
        )
        
        from shop.serializers import ProductSerializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription_product(request):
    """Endpoint pour créer un produit d'abonnement."""
    
    try:
        # ✅ Crée la factory
        factory = SubscriptionProductFactory()
        
        # ✅ Appelle create() avec les données spécifiques
        product = factory.create(
            shop=request.user.shop,
            name=request.data.get('name'),
            price=request.data.get('price'),
            billing_period=request.data.get('billing_period', 'MONTHLY'),
            duration=request.data.get('duration')
        )
        
        from shop.serializers import ProductSerializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)


# ==========================================
# OPTION 2: Utiliser la Registry (Recommandé!)
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    """Endpoint générique pour créer n'importe quel type de produit."""
    
    try:
        product_type = request.data.get('product_type', 'PHYSICAL')
        
        # ✅ LA REGISTRY CHOISIT LA FACTORY!
        factory = ProductFactoryRegistry.get_factory(product_type)
        
        # ✅ Appelle create() avec les données
        product = factory.create(
            shop=request.user.shop,
            name=request.data.get('name'),
            price=request.data.get('price'),
            **request.data  # Passe tous les extra arguments
        )
        
        from shop.serializers import ProductSerializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)
```

---

## 3️⃣ Utilisation Côté Frontend

```typescript
// src/pages/MyShopPage.tsx

// ✅ Créer un produit PHYSIQUE
const handleAddPhysicalProduct = async (formData) => {
    const response = await fetch(`${API_BASE}/api/shop/create-physical/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            product_type: 'PHYSICAL',
            name: 'Moteur V8',
            price: 5000,
            weight: 150,  // kg
            dimensions: '50x50x30',
            stock: 10
        })
    });
    const product = await response.json();
    toast.success(`✅ ${product.name} ajouté!`);
};

// ✅ Créer un produit NUMÉRIQUE
const handleAddDigitalProduct = async (formData) => {
    const response = await fetch(`${API_BASE}/api/shop/create-digital/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            product_type: 'DIGITAL',
            name: 'Ebook - Guide Mécanique',
            price: 29.99,
            file_url: 'https://cdn.example.com/ebooks/guide.pdf',
            file_size: '5.2MB',
            license_key: 'EBC-12345-ABCDE'
        })
    });
};

// ✅ Créer un ABONNEMENT
const handleAddSubscription = async (formData) => {
    const response = await fetch(`${API_BASE}/api/shop/create-subscription/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            product_type: 'SUBSCRIPTION',
            name: 'Abonnement Premium',
            price: 9.99,
            billing_period: 'MONTHLY',
            duration: 12  // 12 mois
        })
    });
};
```

---

## 4️⃣ Flux Complet

```
Frontend
   ↓
POST /api/shop/create-physical/
   │ { name: "Moteur V8", price: 5000, weight: 150, ... }
   ↓
VIEW: create_physical_product()
   ├─ PhysicalProductFactory.create(...)
   │  ├─ _common_validation() ← Validation commune
   │  ├─ validate() ← Validation PHYSIQUE
   │  └─ Product.objects.create() → metadata
   └─ Response: {"id": 1, "name": "Moteur V8", ...}

VS

POST /api/shop/create-digital/
   │ { name: "Ebook", price: 29.99, file_url: "...", ... }
   ↓
VIEW: create_digital_product()
   ├─ DigitalProductFactory.create(...)
   │  ├─ _common_validation() ← Validation commune
   │  ├─ validate() ← Validation NUMÉRIQUE
   │  └─ Product.objects.create() → metadata
   └─ Response: {"id": 2, "name": "Ebook", ...}
```

---

## 5️⃣ Avantages Factory Method

| Avantage | Description |
|----------|------------|
| **Polymorphisme** | Chaque type gère sa création |
| **Extensible** | Ajouter type = nouvelle classe |
| **Réutilisable** | Chaque factory peut être utilisée ailleurs |
| **Testable** | Test chaque factory indépendamment |
| **Flexible** | Validation spécifique par type |
| **Maintenable** | Changement = une seule classe |

---

## 6️⃣ Tests Unitaires

```python
# shop/tests/test_product_factory.py

from django.test import TestCase
from shop.factories.product_factory import (
    PhysicalProductFactory,
    DigitalProductFactory,
    SubscriptionProductFactory
)
from shops.models import Shop
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductFactoryTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.shop = Shop.objects.create(owner=self.user, name='Test Shop', slug='test-shop')
    
    # ✅ TEST PHYSICAL
    def test_create_physical_product(self):
        factory = PhysicalProductFactory()
        product = factory.create(
            shop=self.shop,
            name='Moteur',
            price=5000,
            weight=150,
            stock=10
        )
        
        self.assertEqual(product.name, 'Moteur')
        self.assertEqual(product.price, 5000)
        self.assertEqual(product.product_type, 'PHYSICAL')
        self.assertEqual(product.metadata['weight'], 150)
    
    # ✅ TEST DIGITAL
    def test_create_digital_product(self):
        factory = DigitalProductFactory()
        product = factory.create(
            shop=self.shop,
            name='Ebook',
            price=29.99,
            file_url='https://example.com/ebook.pdf'
        )
        
        self.assertEqual(product.product_type, 'DIGITAL')
        self.assertEqual(product.stock, 9999)
        self.assertTrue(product.metadata['instant_delivery'])
    
    # ✅ TEST SUBSCRIPTION
    def test_create_subscription_product(self):
        factory = SubscriptionProductFactory()
        product = factory.create(
            shop=self.shop,
            name='Premium',
            price=9.99,
            billing_period='MONTHLY'
        )
        
        self.assertEqual(product.product_type, 'SUBSCRIPTION')
        self.assertTrue(product.metadata['is_recurring'])
    
    # ✅ TEST VALIDATION
    def test_physical_product_invalid_weight(self):
        factory = PhysicalProductFactory()
        
        with self.assertRaises(ValueError):
            factory.create(
                shop=self.shop,
                name='Moteur',
                price=5000,
                weight=-10  # ❌ Négatif!
            )
    
    # ✅ TEST REGISTRY
    def test_registry_get_factory(self):
        from shop.factories.product_factory import ProductFactoryRegistry
        
        factory = ProductFactoryRegistry.get_factory('PHYSICAL')
        self.assertIsInstance(factory, PhysicalProductFactory)
        
        factory = ProductFactoryRegistry.get_factory('DIGITAL')
        self.assertIsInstance(factory, DigitalProductFactory)
```

---

## 7️⃣ Structure du Projet

```
shopina-env/backend/
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── factories/              ← DOSSIER FACTORIES
│       ├── __init__.py
│       ├── product_factory.py  ← FACTORY METHOD
│       └── ...
├── tests/
│   └── test_product_factory.py ← TESTS
└── ...
```

---

## 💡 Résumé

**Factory Method = Chaque type gère sa création** 🏭

```python
# Simple Factory (Une classe)
ProductFactory.create(type='PHYSICAL')

# Factory Method (Polymorphisme)
PhysicalProductFactory().create()
DigitalProductFactory().create()
SubscriptionProductFactory().create()

# Registry (Dispatching)
ProductFactoryRegistry.get_factory('PHYSICAL').create()
```

Le Factory Method, c'est du **polymorphisme appliqué à la création d'objets**! 🎯
