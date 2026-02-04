# 📓 SOLID - GUIDE CAHIER (Code à Copier)

## 🎯 COMMENT UTILISER CE GUIDE

Pour chaque principe SOLID:
1. **Copier le code** dans ton cahier
2. **Noter le chemin** du fichier
3. **Comprendre l'exemple**

---

# 🔴 PRINCIPE 1: SINGLE RESPONSIBILITY (S)

## Définition
**Une classe = une seule responsabilité**

---

## EXEMPLE 1: Exception (Une erreur = une classe)

### 📝 Code à copier:

```python
class InsufficientStockError(BusinessLogicError):
    """Exception quand stock insuffisant"""
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'
```

### 📍 Chemin fichier:
```
code source/shopina-env/backend/core/utils/exceptions.py
Lignes: 17-22
```

### ✅ Pourquoi c'est SINGLE RESPONSIBILITY?
- ✅ Cette classe fait UNE chose: définir l'erreur stock insuffisant
- ✅ Si on change le message d'erreur → on modifie juste cette classe
- ✅ Pas de logique, pas de traitement → juste une définition

---

## EXEMPLE 2: Validator (Une validation = une fonction)

### 📝 Code à copier:

```python
def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """Valide le prix"""
    if price < 0:
        return False, "Price cannot be negative"
    if price > 999999.99:
        return False, "Price exceeds maximum allowed value"
    return True, None
```

### 📍 Chemin fichier:
```
code source/shopina-env/backend/core/utils/validators.py
Lignes: 45-59
```

### ✅ Pourquoi c'est SINGLE RESPONSIBILITY?
- ✅ Cette fonction fait UNE chose: valider le prix
- ✅ Pas de validation stock, pas de validation rating
- ✅ Juste le prix
- ✅ Si règle de prix change → modifier juste cette fonction

---

## EXEMPLE 3: Repository (Accès données SEULEMENT)

### 📝 Code à copier:

```python
class BaseRepository(Generic[ModelType]):
    """Repository pour accéder aux données"""
    
    def __init__(self, model: type[ModelType]):
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Récupère par ID"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
```

### 📍 Chemin fichier:
```
code source/shopina-env/backend/core/repositories/base.py
Lignes: 13-41
```

### ✅ Pourquoi c'est SINGLE RESPONSIBILITY?
- ✅ Cette classe fait UNE chose: accéder aux données
- ✅ PAS de validation métier
- ✅ PAS de logique métier
- ✅ PAS d'envoi email
- ✅ JUSTE récupérer/créer/modifier/supprimer données

---

# 🟠 PRINCIPE 2: OPEN/CLOSED (O)

## Définition
**Ouvert à extension, fermé à modification**

---

## EXEMPLE 1: BaseRepository extensible

### 📝 Code à copier:

```python
# CLASSE PARENT (ne jamais modifier)
class BaseRepository(Generic[ModelType]):
    """Base pour tous les repositories"""
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Méthode de base"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

# CLASSE ENFANT (on étend sans modifier parent)
class ProductRepository(BaseRepository[Product]):
    """Repository produit: ÉTEND BaseRepository"""
    
    def __init__(self):
        super().__init__(Product)
    
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """NOUVELLE méthode: spécifique à Product"""
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None
    
    def get_active_products(self) -> QuerySet[Product]:
        """NOUVELLE méthode: produits actifs"""
        return self.model.objects.filter(stock__gt=0)
```

### 📍 Chemin fichiers:
```
PARENT: code source/shopina-env/backend/core/repositories/base.py
Lignes: 13-41

ENFANT: code source/shopina-env/backend/shop/repositories/product_repository.py
Lignes: 10-32
```

### ✅ Pourquoi c'est OPEN/CLOSED?
- ✅ **OUVERT**: ProductRepository ajoute méthodes (get_by_slug, get_active_products)
- ✅ **FERMÉ**: BaseRepository JAMAIS modifié
- ✅ Si on crée UserRepository → même pattern, pas toucher BaseRepository

---

## EXEMPLE 2: BaseService extensible

### 📝 Code à copier:

```python
# CLASSE PARENT (ne jamais modifier)
class BaseService(Generic[ModelType]):
    """Base pour tous les services"""
    
    def __init__(self, repository=None):
        self.repository = repository
    
    def validate_business_rules(self, data: dict):
        """À surcharger dans enfants"""
        return True, None

# CLASSE ENFANT (on étend sans modifier parent)
class ProductService(BaseService[Product]):
    """Service produit: ÉTEND BaseService"""
    
    def __init__(self):
        self.product_repository = ProductRepository()
        super().__init__(self.product_repository)
    
    def create_product_for_shop(self, shop, name, price, ...):
        """NOUVELLE méthode: créer produit"""
        # Validation
        is_valid, error = validate_price(price)
        if not is_valid:
            raise ValidationError(error)
        
        # Création
        product = Product.objects.create(
            name=name,
            price=price,
            shop=shop
        )
        return product
```

### 📍 Chemin fichiers:
```
PARENT: code source/shopina-env/backend/core/services/base.py
Lignes: 13-48

ENFANT: code source/shopina-env/backend/shop/services/product_service.py
Lignes: 17-122
```

### ✅ Pourquoi c'est OPEN/CLOSED?
- ✅ **OUVERT**: ProductService ajoute méthodes (create_product_for_shop)
- ✅ **FERMÉ**: BaseService JAMAIS modifié
- ✅ Si on crée OrderService → même pattern

---

# 🟡 PRINCIPE 3: LISKOV SUBSTITUTION (L)

## Définition
**Sous-classe peut remplacer parent sans casser le code**

---

## EXEMPLE: Repository substitution

### 📝 Code à copier:

```python
# PARENT
class BaseRepository(Generic[ModelType]):
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Retourne Model | None"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

# ENFANT
class ProductRepository(BaseRepository[Product]):
    def get_by_id(self, id: int) -> Optional[Product]:
        """Retourne TOUJOURS Product | None (respect contrat)"""
        return super().get_by_id(id)

# UTILISATION (Liskov en action)
def fetch_entity(repo: BaseRepository[T], id: int):
    """Fonction accepte BaseRepository"""
    return repo.get_by_id(id)

# ON PEUT PASSER ProductRepository sans problème:
product_repo = ProductRepository()
product = fetch_entity(product_repo, 1)  # ✅ FONCTIONNE

# ProductRepository REMPLACE BaseRepository ✓
```

### 📍 Chemin fichiers:
```
PARENT: code source/shopina-env/backend/core/repositories/base.py
Lignes: 27-41

ENFANT: code source/shopina-env/backend/shop/repositories/product_repository.py
Lignes: 10-17
```

### ✅ Pourquoi c'est LISKOV SUBSTITUTION?
- ✅ ProductRepository retourne TOUJOURS Optional[Product]
- ✅ Respecte la signature de BaseRepository
- ✅ Peut remplacer BaseRepository partout
- ✅ Code qui utilise BaseRepository fonctionne avec ProductRepository

---

# 🟢 PRINCIPE 4: INTERFACE SEGREGATION (I)

## Définition
**Clients utilisent JUSTE ce qu'ils ont besoin**

---

## EXEMPLE 1: Validators séparés

### 📝 Code à copier:

```python
# VALIDATOR 1: Prix seulement
def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """Valide JUSTE le prix"""
    if price < 0:
        return False, "Price cannot be negative"
    return True, None

# VALIDATOR 2: Quantité seulement
def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """Valide JUSTE la quantité"""
    if quantity < 1:
        return False, "Quantity must be at least 1"
    return True, None

# VALIDATOR 3: Rating seulement
def validate_rating(rating: float) -> tuple[bool, Optional[str]]:
    """Valide JUSTE le rating"""
    if rating < 0 or rating > 5:
        return False, "Rating must be between 0 and 5"
    return True, None

# USAGE dans ProductService:
from core.utils.validators import validate_price
# N'importe PAS validate_rating (pas besoin) ✓

# USAGE dans ReviewService:
from core.utils.validators import validate_rating
# N'importe PAS validate_price (pas besoin) ✓
```

### 📍 Chemin fichier:
```
code source/shopina-env/backend/core/utils/validators.py
Lignes: 45-85
```

### ✅ Pourquoi c'est INTERFACE SEGREGATION?
- ✅ Chaque fonction = une validation
- ✅ ProductService importe JUSTE validate_price
- ✅ ReviewService importe JUSTE validate_rating
- ✅ Pas forcé d'importer tout un gros validateur

---

## EXEMPLE 2: Repository méthodes minimales

### 📝 Code à copier:

```python
class BaseRepository(Generic[ModelType]):
    """
    Interface MINIMALE:
    - get_by_id()  ✓
    - get_all()    ✓
    - create()     ✓
    - update()     ✓
    - delete()     ✓
    
    PAS de méthodes inutiles:
    - cache_get()      ✗
    - send_webhook()   ✗
    - export_csv()     ✗
    - analytics()      ✗
    """
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Essentiel: récupérer par ID"""
        pass
    
    def get_all(self) -> QuerySet[ModelType]:
        """Essentiel: récupérer tous"""
        pass
```

### 📍 Chemin fichier:
```
code source/shopina-env/backend/core/repositories/base.py
Lignes: 13-50
```

### ✅ Pourquoi c'est INTERFACE SEGREGATION?
- ✅ Expose JUSTE méthodes essentielles
- ✅ Pas de méthodes dont certains repos n'ont pas besoin
- ✅ ProductRepository/UserRepository/OrderRepository: tous peuvent implémenter

---

# 🔵 PRINCIPE 5: DEPENDENCY INVERSION (D)

## Définition
**Dépendre d'abstractions, PAS de concrétions**

---

## EXEMPLE 1: Service dépend de Repository abstraction

### 📝 Code à copier:

```python
# ❌ MAUVAIS: Service dépend de concrète DB
class ProductService:
    def __init__(self):
        self.db = PostgresConnection()  # ❌ Concrète
    
    def create_product(self):
        self.db.execute("INSERT INTO...")  # ❌ Couplé à DB

# ✅ BON: Service dépend d'abstraction Repository
class ProductService(BaseService[Product]):
    def __init__(self):
        # ✅ Dépend de Repository ABSTRACTION
        self.product_repository = ProductRepository()
        super().__init__(self.product_repository)
    
    def create_product_for_shop(self, shop, name, price, ...):
        """Utilise Repository abstraction"""
        # Validation
        is_valid, error = validate_price(price)
        if not is_valid:
            raise ValidationError(error)
        
        # ✅ Délègue à Repository (pas direct DB)
        product = Product.objects.create(
            name=name,
            price=price,
            shop=shop
        )
        return product
```

### 📍 Chemin fichier:
```
code source/shopina-env/backend/shop/services/product_service.py
Lignes: 17-122
```

### ✅ Pourquoi c'est DEPENDENCY INVERSION?
- ✅ Service dépend de ProductRepository (abstraction)
- ✅ PAS de dépendance directe à PostgreSQL
- ✅ Si on change DB → modifier juste Repository
- ✅ Service reste identique

---

## EXEMPLE 2: View dépend de Service abstraction

### 📝 Code à copier:

```python
from rest_framework.decorators import api_view
from .services.product_service import ProductService

@api_view(['POST'])
def create_product_api(request):
    """View dépend de Service abstraction"""
    
    # Extract data
    name = request.data.get('name')
    price = request.data.get('price')
    shop = request.user.shop
    
    # ✅ Dépend de Service ABSTRACTION
    product_service = ProductService()
    
    # ✅ Délègue TOUTE logique au Service
    product = product_service.create_product_for_shop(
        shop=shop,
        name=name,
        price=price
    )
    
    # Return JSON
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=201)
```

### 📍 Chemin fichier:
```
code source/shopina-env/backend/shop/views.py
Lignes: 40-85
```

### ✅ Pourquoi c'est DEPENDENCY INVERSION?
- ✅ View dépend de ProductService (abstraction)
- ✅ PAS d'accès direct à Product.objects (concrète)
- ✅ PAS de logique métier dans View
- ✅ View juste: reçoit HTTP → délègue Service → retourne JSON

---

# 📊 RÉSUMÉ POUR TON CAHIER

## 🔴 S - SINGLE RESPONSIBILITY
**Une classe = une responsabilité**

```
✅ InsufficientStockError → définir erreur
✅ validate_price() → valider prix
✅ BaseRepository → accès données
✅ ProductService → logique métier
✅ create_product_api → HTTP seulement
```

**Fichiers**:
- `core/utils/exceptions.py`
- `core/utils/validators.py`
- `core/repositories/base.py`
- `shop/services/product_service.py`
- `shop/views.py`

---

## 🟠 O - OPEN/CLOSED
**Ouvert à extension, fermé à modification**

```
✅ BaseRepository → ne jamais modifier
✅ ProductRepository → étend BaseRepository
✅ BaseService → ne jamais modifier
✅ ProductService → étend BaseService
```

**Fichiers**:
- `core/repositories/base.py` (parent)
- `shop/repositories/product_repository.py` (enfant)
- `core/services/base.py` (parent)
- `shop/services/product_service.py` (enfant)

---

## 🟡 L - LISKOV SUBSTITUTION
**Sous-classe remplace parent**

```
✅ ProductRepository IS-A BaseRepository
✅ Peut remplacer BaseRepository partout
✅ Respecte signature parent
```

**Fichiers**:
- `core/repositories/base.py` (parent)
- `shop/repositories/product_repository.py` (enfant)

---

## 🟢 I - INTERFACE SEGREGATION
**Utiliser JUSTE ce qu'on a besoin**

```
✅ validate_price() séparé de validate_rating()
✅ ProductService importe validate_price seulement
✅ ReviewService importe validate_rating seulement
```

**Fichiers**:
- `core/utils/validators.py`
- `core/repositories/base.py`

---

## 🔵 D - DEPENDENCY INVERSION
**Dépendre d'abstractions**

```
✅ ProductService dépend de ProductRepository (abstraction)
✅ View dépend de ProductService (abstraction)
✅ PAS de dépendance directe DB/ORM
```

**Fichiers**:
- `shop/services/product_service.py`
- `shop/views.py`

---

# 🎯 FLUX COMPLET (avec SOLID)

```
1. HTTP Request
   ↓
2. VIEW (shop/views.py)
   └─ S: Juste HTTP
   └─ D: Dépend de Service abstraction
   ↓
3. SERVICE (shop/services/product_service.py)
   └─ S: Juste logique métier
   └─ O: Étend BaseService
   └─ L: Remplace BaseService
   └─ D: Dépend de Repository abstraction
   ↓
4. REPOSITORY (shop/repositories/product_repository.py)
   └─ S: Juste accès données
   └─ O: Étend BaseRepository
   └─ L: Remplace BaseRepository
   └─ I: Interface minimale
   ↓
5. DATABASE
```

---

# 📝 CHECKLIST POUR TON CAHIER

Quand tu écris du code, vérifie:

## ✅ Single Responsibility
- [ ] Ma classe fait UNE seule chose?
- [ ] Si je change X, je modifie juste cette classe?

## ✅ Open/Closed
- [ ] Je peux étendre sans modifier?
- [ ] J'ai créé BaseXXX pour réutiliser?

## ✅ Liskov Substitution
- [ ] Mon enfant peut remplacer parent?
- [ ] J'ai respecté signature parent?

## ✅ Interface Segregation
- [ ] Ma classe expose juste ce qui est nécessaire?
- [ ] Pas de méthodes inutiles?

## ✅ Dependency Inversion
- [ ] Je dépends d'abstractions?
- [ ] Pas de dépendance concrète (DB, API)?

---

**Créé pour**: Cahier d'apprentissage  
**Date**: 2026-02-03  
**Backend**: Django REST Framework  
**Status**: ✅ Code testé et fonctionnel
