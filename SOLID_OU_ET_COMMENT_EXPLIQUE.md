# 🎯 OÙ ET COMMENT SOLID EST RESPECTÉ - EXPLICATION DÉTAILLÉE

## 📍 NAVIGATION RAPIDE

| Principe | Fichier Principal | Explication |
|----------|-------------------|-------------|
| **S** - Single Responsibility | `core/utils/exceptions.py` | [Aller](#s---single-responsibility-expliqué) |
| **O** - Open/Closed | `core/repositories/base.py` | [Aller](#o---openclosed-expliqué) |
| **L** - Liskov Substitution | `shop/repositories/product_repository.py` | [Aller](#l---liskov-substitution-expliqué) |
| **I** - Interface Segregation | `core/utils/validators.py` | [Aller](#i---interface-segregation-expliqué) |
| **D** - Dependency Inversion | `shop/services/product_service.py` | [Aller](#d---dependency-inversion-expliqué) |

---

# 🔴 S - SINGLE RESPONSIBILITY EXPLIQUÉ

## Définition Simple
**Une classe = une seule raison de changer**

---

## EXEMPLE 1: EXCEPTIONS ✅

### 📍 OÙ: `code source/shopina-env/backend/core/utils/exceptions.py`

### 📝 LE CODE:

```python
class BusinessLogicError(APIException):
    """Exception pour erreurs métier"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic validation failed.'
    default_code = 'business_logic_error'


class InsufficientStockError(BusinessLogicError):
    """Exception pour stock insuffisant"""
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'


class PaymentError(APIException):
    """Exception pour erreurs paiement"""
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Payment processing failed.'
    default_code = 'payment_error'
```

### ✅ COMMENT C'EST RESPECTÉ:

#### 1. **BusinessLogicError** a UNE seule responsabilité:
   - ✅ Définir une erreur métier avec code 400
   - ❌ PAS de logique de traitement
   - ❌ PAS d'envoi email
   - ❌ PAS de log
   - ✅ JUSTE définir la structure de l'exception

#### 2. **InsufficientStockError** a UNE seule responsabilité:
   - ✅ Définir l'erreur "stock insuffisant"
   - ✅ Hérite de BusinessLogicError (code 400)
   - ❌ PAS de vérification du stock (ProductService le fait)
   - ❌ PAS de mise à jour du stock (Repository le fait)

#### 3. **PaymentError** a UNE seule responsabilité:
   - ✅ Définir l'erreur paiement avec code 402
   - ❌ PAS de traitement de paiement
   - ❌ PAS de connexion Stripe

### 🎯 POURQUOI C'EST BON:

```python
# ❌ MAUVAIS EXEMPLE (violation Single Responsibility):
class ProductError(Exception):
    def __init__(self, message):
        self.message = message
    
    def send_email(self):
        # Envoie email ❌
        pass
    
    def log_error(self):
        # Log erreur ❌
        pass
    
    def notify_slack(self):
        # Notifie Slack ❌
        pass
    
    # Cette classe fait 4 choses différentes ❌

# ✅ BON EXEMPLE (respect Single Responsibility):
class InsufficientStockError(BusinessLogicError):
    """JUSTE définir l'exception"""
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'

# Une autre classe pour email:
class EmailService:
    def send_stock_alert(self, product):
        # JUSTE envoyer email ✓
        pass

# Une autre classe pour log:
class LogService:
    def log_error(self, error):
        # JUSTE logger ✓
        pass
```

### 📊 RÉSULTAT:
- Si on change le **message d'erreur** → modifier `InsufficientStockError` seulement
- Si on change le **système de log** → modifier `LogService` seulement
- Si on change **l'email** → modifier `EmailService` seulement
- **Chaque classe change pour SA propre raison** ✓

---

## EXEMPLE 2: REPOSITORY ✅

### 📍 OÙ: `code source/shopina-env/backend/core/repositories/base.py`

### 📝 LE CODE:

```python
class BaseRepository(Generic[ModelType]):
    """Repository pour accès aux données"""
    
    def __init__(self, model: type[ModelType]):
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Récupère par ID"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
    
    def get_all(self) -> QuerySet[ModelType]:
        """Récupère tous"""
        return self.model.objects.all()
```

### ✅ COMMENT C'EST RESPECTÉ:

#### BaseRepository a UNE seule responsabilité:
   - ✅ Accéder aux données (CRUD: Create, Read, Update, Delete)
   - ❌ PAS de validation métier (ProductService le fait)
   - ❌ PAS de calcul de prix (ProductService le fait)
   - ❌ PAS d'envoi email (EmailService le fait)
   - ❌ PAS de génération PDF (PDFService le fait)

### 🎯 POURQUOI C'EST BON:

```python
# ❌ MAUVAIS EXEMPLE:
class ProductRepository:
    def get_by_id(self, id):
        product = Product.objects.get(id=id)
        
        # Validation ❌ (devrait être dans Service)
        if product.price < 0:
            raise ValidationError("Prix invalide")
        
        # Email ❌ (devrait être dans EmailService)
        send_email("admin@example.com", "Product accessed")
        
        # Log ❌ (devrait être dans LogService)
        log.info(f"Product {id} accessed")
        
        return product
    
    # Cette méthode fait 4 choses ❌

# ✅ BON EXEMPLE:
class ProductRepository:
    def get_by_id(self, id):
        """JUSTE récupérer le produit"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
    # JUSTE accès données ✓
```

### 📊 RÉSULTAT:
- Si on change la **base de données** (PostgreSQL → MongoDB) → modifier `Repository` seulement
- Si on change la **validation** → modifier `Service` seulement
- **Repository fait UNE chose: accéder aux données** ✓

---

## EXEMPLE 3: SERVICE ✅

### 📍 OÙ: `code source/shopina-env/backend/shop/services/product_service.py`

### 📝 LE CODE:

```python
class ProductService(BaseService[Product]):
    """Service pour logique métier produit"""
    
    def __init__(self):
        self.product_repository = ProductRepository()
        super().__init__(self.product_repository)
    
    def create_product_for_shop(self, shop, name, price, ...):
        """Créer produit avec validation"""
        
        # ÉTAPE 1: Valider prix (logique métier)
        is_valid, error = validate_price(float(price))
        if not is_valid:
            raise ValidationError(error)
        
        # ÉTAPE 2: Valider stock (logique métier)
        if stock < 0:
            raise ValidationError("Stock cannot be negative")
        
        # ÉTAPE 3: Créer catégorie si nécessaire (logique métier)
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
        
        # ÉTAPE 4: Créer produit
        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            shop=shop
        )
        
        # ÉTAPE 5: Log opération
        self.log_operation('product_created', {'product_id': product.id})
        
        return product
```

### ✅ COMMENT C'EST RESPECTÉ:

#### ProductService a UNE seule responsabilité:
   - ✅ Logique métier PRODUIT seulement
   - ✅ Validation prix, stock
   - ✅ Création catégorie si nécessaire
   - ❌ PAS d'accès direct DB (délègue à Repository)
   - ❌ PAS de HTTP (View le fait)
   - ❌ PAS de transformation JSON (Serializer le fait)

### 🎯 POURQUOI C'EST BON:

```python
# ❌ MAUVAIS EXEMPLE:
class ProductService:
    def create_product(self, request):
        # HTTP ❌ (devrait être dans View)
        name = request.data.get('name')
        
        # Validation ✓ (OK dans Service)
        if price < 0:
            raise ValidationError("Prix invalide")
        
        # DB direct ❌ (devrait être dans Repository)
        product = Product.objects.create(name=name, price=price)
        
        # JSON ❌ (devrait être dans Serializer)
        return {'id': product.id, 'name': product.name}
    
    # Cette méthode fait 4 choses ❌

# ✅ BON EXEMPLE:
class ProductService:
    def create_product_for_shop(self, shop, name, price, stock):
        """JUSTE logique métier"""
        # Validation ✓
        is_valid, error = validate_price(price)
        if not is_valid:
            raise ValidationError(error)
        
        # Création ✓
        product = Product.objects.create(...)
        
        # Log ✓
        self.log_operation('product_created', {...})
        
        return product
```

### 📊 RÉSULTAT:
- Si on change les **règles de validation** → modifier `ProductService` seulement
- Si on change la **structure HTTP** → modifier `View` seulement
- Si on change le **format JSON** → modifier `Serializer` seulement
- **Service fait UNE chose: logique métier** ✓

---

# 🟠 O - OPEN/CLOSED EXPLIQUÉ

## Définition Simple
**Ouvert à extension, fermé à modification**

---

## EXEMPLE: BaseRepository + ProductRepository ✅

### 📍 OÙ:
- **PARENT**: `code source/shopina-env/backend/core/repositories/base.py`
- **ENFANT**: `code source/shopina-env/backend/shop/repositories/product_repository.py`

### 📝 LE CODE:

```python
# ==========================================
# FICHIER 1: core/repositories/base.py
# ==========================================

class BaseRepository(Generic[ModelType]):
    """
    Classe PARENT
    ⚠️ NE JAMAIS MODIFIER CETTE CLASSE
    """
    
    def __init__(self, model: type[ModelType]):
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Méthode de base pour récupérer par ID"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
    
    def get_all(self) -> QuerySet[ModelType]:
        """Méthode de base pour récupérer tous"""
        return self.model.objects.all()


# ==========================================
# FICHIER 2: shop/repositories/product_repository.py
# ==========================================

class ProductRepository(BaseRepository[Product]):
    """
    Classe ENFANT
    ✅ ÉTEND BaseRepository SANS le modifier
    """
    
    def __init__(self):
        # ✅ Utilise __init__ du parent
        super().__init__(Product)
    
    # ✅ NOUVELLE MÉTHODE: spécifique à Product
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """Méthode AJOUTÉE (pas dans BaseRepository)"""
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None
    
    # ✅ NOUVELLE MÉTHODE: spécifique à Product
    def get_active_products(self) -> QuerySet[Product]:
        """Méthode AJOUTÉE (pas dans BaseRepository)"""
        return self.model.objects.filter(stock__gt=0).select_related('category')
    
    # ✅ NOUVELLE MÉTHODE: spécifique à Product
    def search_products(self, query: str) -> QuerySet[Product]:
        """Méthode AJOUTÉE (pas dans BaseRepository)"""
        return self.model.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
```

### ✅ COMMENT C'EST RESPECTÉ:

#### 1. **BaseRepository est FERMÉ à modification**:
   ```python
   # ❌ MAUVAIS: Modifier BaseRepository pour ajouter fonctionnalité
   class BaseRepository:
       def get_by_id(self, id):
           return self.model.objects.get(pk=id)
       
       def get_by_slug(self, slug):  # ❌ Ajouté pour Product
           return self.model.objects.get(slug=slug)
       
       def get_active_products(self):  # ❌ Ajouté pour Product
           return self.model.objects.filter(stock__gt=0)
   
   # Problème: User/Order n'ont pas de slug/stock ❌
   ```

#### 2. **ProductRepository est OUVERT à extension**:
   ```python
   # ✅ BON: Étendre sans modifier parent
   class ProductRepository(BaseRepository[Product]):
       # ✅ Hérite get_by_id(), get_all() de BaseRepository
       
       # ✅ AJOUTE ses propres méthodes
       def get_by_slug(self, slug):
           return self.model.objects.get(slug=slug)
       
       def get_active_products(self):
           return self.model.objects.filter(stock__gt=0)
   
   # BaseRepository pas modifié ✓
   # Product a ses méthodes spécifiques ✓
   ```

### 🎯 SCHÉMA:

```
┌─────────────────────────────────┐
│     BaseRepository              │ ← FERMÉ (ne jamais modifier)
│  - get_by_id()                  │
│  - get_all()                    │
└─────────────────────────────────┘
           ▲
           │ hérite
           │
┌──────────┴──────────────────────┐
│  ProductRepository               │ ← OUVERT (peut étendre)
│  - get_by_id()     (hérité)     │
│  - get_all()       (hérité)     │
│  - get_by_slug()   (nouveau)    │ ✅ AJOUTÉ
│  - get_active_products() (nouv) │ ✅ AJOUTÉ
│  - search_products()    (nouv)  │ ✅ AJOUTÉ
└─────────────────────────────────┘
```

### 📊 AVANTAGES:

1. **Ajouter UserRepository**:
   ```python
   class UserRepository(BaseRepository[User]):
       def __init__(self):
           super().__init__(User)
       
       # ✅ Ajoute méthodes User-spécifiques
       def get_by_email(self, email):
           return self.model.objects.get(email=email)
   
   # BaseRepository toujours pas modifié ✓
   ```

2. **Ajouter OrderRepository**:
   ```python
   class OrderRepository(BaseRepository[Order]):
       def __init__(self):
           super().__init__(Order)
       
       # ✅ Ajoute méthodes Order-spécifiques
       def get_by_user(self, user_id):
           return self.model.objects.filter(user_id=user_id)
   
   # BaseRepository toujours pas modifié ✓
   ```

### 📊 RÉSULTAT:
- ✅ **FERMÉ**: BaseRepository jamais modifié
- ✅ **OUVERT**: ProductRepository, UserRepository, OrderRepository peuvent étendre
- ✅ Chaque repository ajoute ses méthodes spécifiques
- ✅ Pas de risque de casser BaseRepository

---

# 🟡 L - LISKOV SUBSTITUTION EXPLIQUÉ

## Définition Simple
**Sous-classe peut remplacer parent sans casser le code**

---

## EXEMPLE: ProductRepository remplace BaseRepository ✅

### 📍 OÙ: 
- **PARENT**: `code source/shopina-env/backend/core/repositories/base.py`
- **ENFANT**: `code source/shopina-env/backend/shop/repositories/product_repository.py`

### 📝 LE CODE:

```python
# ==========================================
# PARENT: BaseRepository
# ==========================================

class BaseRepository(Generic[ModelType]):
    """Contrat: retourne ModelType | None"""
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        CONTRAT:
        - Prend int
        - Retourne ModelType | None
        - Lève DoesNotExist → retourne None
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None


# ==========================================
# ENFANT: ProductRepository
# ==========================================

class ProductRepository(BaseRepository[Product]):
    """DOIT respecter contrat BaseRepository"""
    
    def get_by_id(self, id: int) -> Optional[Product]:
        """
        ✅ RESPECTE CONTRAT:
        - Prend int ✓
        - Retourne Product | None ✓
        - Lève DoesNotExist → retourne None ✓
        """
        return super().get_by_id(id)
    
    # ✅ Peut AJOUTER méthodes
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """Nouvelle méthode (pas dans parent)"""
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None
```

### ✅ COMMENT C'EST RESPECTÉ:

#### 1. **CONTRAT PARENT**:
```python
class BaseRepository:
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        CONTRAT:
        - INPUT: int
        - OUTPUT: ModelType | None
        - COMPORTEMENT: DoesNotExist → None
        """
        pass
```

#### 2. **ENFANT RESPECTE CONTRAT**:
```python
class ProductRepository(BaseRepository[Product]):
    def get_by_id(self, id: int) -> Optional[Product]:
        """
        ✅ INPUT: int (pareil que parent)
        ✅ OUTPUT: Product | None (Product est un ModelType)
        ✅ COMPORTEMENT: DoesNotExist → None (pareil)
        """
        return super().get_by_id(id)
```

### 🎯 UTILISATION (LISKOV EN ACTION):

```python
# ==========================================
# Fonction qui accepte BaseRepository
# ==========================================

def fetch_entity(repository: BaseRepository[T], id: int) -> Optional[T]:
    """
    Cette fonction attend BaseRepository
    
    CONTRAT:
    - repository.get_by_id(int) → T | None
    """
    return repository.get_by_id(id)


# ==========================================
# UTILISATION AVEC ProductRepository
# ==========================================

# Créer ProductRepository
product_repo = ProductRepository()

# ✅ LISKOV: Passer ProductRepository où BaseRepository attendu
product = fetch_entity(product_repo, 1)

# ✅ FONCTIONNE car:
# - ProductRepository IS-A BaseRepository ✓
# - get_by_id() retourne Product | None ✓
# - Product est un ModelType ✓
# - Comportement identique ✓


# ==========================================
# UTILISATION AVEC UserRepository
# ==========================================

user_repo = UserRepository()

# ✅ LISKOV: Fonctionne aussi avec UserRepository
user = fetch_entity(user_repo, 1)

# ✅ FONCTIONNE car:
# - UserRepository IS-A BaseRepository ✓
# - get_by_id() retourne User | None ✓
```

### ❌ EXEMPLE VIOLATION LISKOV:

```python
# ❌ MAUVAIS: Violation Liskov
class ProductRepository(BaseRepository[Product]):
    def get_by_id(self, id: int) -> Product:
        """
        ❌ VIOLATION:
        - Parent retourne Optional[Product]
        - Enfant retourne Product (pas Optional)
        - Lève exception au lieu de retourner None
        """
        # ❌ Lève exception au lieu de retourner None
        return self.model.objects.get(pk=id)
        # Si produit pas trouvé → exception ❌
        # Parent retournait None ❌


# UTILISATION (casse):
def fetch_entity(repo: BaseRepository[T], id: int):
    entity = repo.get_by_id(999)  # ID n'existe pas
    
    # Code attend None
    if entity is None:
        print("Not found")
    else:
        print(entity.name)

product_repo = ProductRepository()
fetch_entity(product_repo, 999)
# ❌ CRASH: DoesNotExist exception levée
# ❌ Code attendait None
# ❌ Violation Liskov
```

### ✅ EXEMPLE CORRECT:

```python
# ✅ BON: Respect Liskov
class ProductRepository(BaseRepository[Product]):
    def get_by_id(self, id: int) -> Optional[Product]:
        """
        ✅ RESPECTE CONTRAT:
        - Retourne Product | None (comme parent)
        - DoesNotExist → None (comme parent)
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None  # ✅ Même comportement que parent


# UTILISATION (fonctionne):
def fetch_entity(repo: BaseRepository[T], id: int):
    entity = repo.get_by_id(999)
    
    if entity is None:
        print("Not found")  # ✅ Fonctionne
    else:
        print(entity.name)

product_repo = ProductRepository()
fetch_entity(product_repo, 999)
# ✅ Affiche "Not found"
# ✅ Pas de crash
# ✅ Liskov respecté
```

### 📊 RÉSULTAT:
- ✅ ProductRepository peut remplacer BaseRepository partout
- ✅ Code écrit pour BaseRepository fonctionne avec ProductRepository
- ✅ Comportement prévisible
- ✅ Tests faciles: Peut utiliser MockRepository

---

# 🟢 I - INTERFACE SEGREGATION EXPLIQUÉ

## Définition Simple
**Clients utilisent JUSTE ce qu'ils ont besoin**

---

## EXEMPLE 1: Validators Séparés ✅

### 📍 OÙ: `code source/shopina-env/backend/core/utils/validators.py`

### 📝 LE CODE:

```python
# ==========================================
# VALIDATOR 1: Prix seulement
# ==========================================

def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """Valide JUSTE le prix"""
    if price < 0:
        return False, "Price cannot be negative"
    if price > 999999.99:
        return False, "Price exceeds maximum"
    return True, None


# ==========================================
# VALIDATOR 2: Quantité seulement
# ==========================================

def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """Valide JUSTE la quantité"""
    if quantity < 1:
        return False, "Quantity must be at least 1"
    if quantity > 10000:
        return False, "Quantity exceeds maximum"
    return True, None


# ==========================================
# VALIDATOR 3: Rating seulement
# ==========================================

def validate_rating(rating: float) -> tuple[bool, Optional[str]]:
    """Valide JUSTE le rating"""
    if rating < 0 or rating > 5:
        return False, "Rating must be between 0 and 5"
    return True, None
```

### ✅ COMMENT C'EST RESPECTÉ:

#### 1. **ProductService** utilise JUSTE ce qu'il a besoin:
```python
# FICHIER: shop/services/product_service.py

from core.utils.validators import validate_price
# ✅ Importe JUSTE validate_price
# ❌ N'importe PAS validate_rating (pas besoin)

class ProductService:
    def create_product(self, name, price, stock):
        # ✅ Utilise validate_price
        is_valid, error = validate_price(price)
        if not is_valid:
            raise ValidationError(error)
        
        # ❌ N'utilise PAS validate_rating
        # Product n'a pas de rating à la création
```

#### 2. **ReviewService** utilise JUSTE ce qu'il a besoin:
```python
# FICHIER: reviews/services/review_service.py

from core.utils.validators import validate_rating
# ✅ Importe JUSTE validate_rating
# ❌ N'importe PAS validate_price (pas besoin)

class ReviewService:
    def create_review(self, product, rating, comment):
        # ✅ Utilise validate_rating
        is_valid, error = validate_rating(rating)
        if not is_valid:
            raise ValidationError(error)
        
        # ❌ N'utilise PAS validate_price
        # Review n'a pas de price
```

#### 3. **OrderService** utilise JUSTE ce qu'il a besoin:
```python
# FICHIER: orders/services/order_service.py

from core.utils.validators import validate_quantity
# ✅ Importe JUSTE validate_quantity
# ❌ N'importe PAS validate_price ni validate_rating

class OrderService:
    def add_item(self, product, quantity):
        # ✅ Utilise validate_quantity
        is_valid, error = validate_quantity(quantity)
        if not is_valid:
            raise ValidationError(error)
```

### ❌ EXEMPLE VIOLATION:

```python
# ❌ MAUVAIS: Un gros validateur qui fait tout
class Validator:
    """Interface TROP GROSSE"""
    
    def validate_price(self, price):
        pass
    
    def validate_quantity(self, quantity):
        pass
    
    def validate_rating(self, rating):
        pass
    
    def validate_email(self, email):
        pass
    
    def validate_phone(self, phone):
        pass
    
    def validate_address(self, address):
        pass
    
    # ... 50 autres méthodes


# ❌ PROBLÈME:
class ProductService:
    def __init__(self):
        # ❌ DOIT recevoir TOUT le Validator
        self.validator = Validator()
    
    def create_product(self, price):
        # ✅ Utilise validate_price
        self.validator.validate_price(price)
        
        # ❌ ProductService a accès à validate_rating, validate_email, etc
        # ❌ Même si il n'en a pas besoin
        # ❌ Dépendances inutiles
```

### ✅ EXEMPLE CORRECT:

```python
# ✅ BON: Validators séparés

# Fichier: validators.py
def validate_price(price):
    """JUSTE prix"""
    pass

def validate_rating(rating):
    """JUSTE rating"""
    pass


# ✅ USAGE:
class ProductService:
    def create_product(self, price):
        # ✅ Importe JUSTE ce qu'il a besoin
        from validators import validate_price
        
        # ✅ Utilise validate_price
        validate_price(price)
        
        # ✅ Pas d'accès à validate_rating
        # ✅ Dépendances minimales


class ReviewService:
    def create_review(self, rating):
        # ✅ Importe JUSTE ce qu'il a besoin
        from validators import validate_rating
        
        # ✅ Utilise validate_rating
        validate_rating(rating)
        
        # ✅ Pas d'accès à validate_price
        # ✅ Dépendances minimales
```

### 📊 RÉSULTAT:
- ✅ ProductService dépend JUSTE de `validate_price`
- ✅ ReviewService dépend JUSTE de `validate_rating`
- ✅ OrderService dépend JUSTE de `validate_quantity`
- ✅ Chaque service a JUSTE ce qu'il utilise
- ✅ Pas de dépendances inutiles

---

# 🔵 D - DEPENDENCY INVERSION EXPLIQUÉ

## Définition Simple
**Dépendre d'abstractions, PAS de concrétions**

---

## EXEMPLE: Service → Repository → Model ✅

### 📍 OÙ:
- **VIEW**: `code source/shopina-env/backend/shop/views.py`
- **SERVICE**: `code source/shopina-env/backend/shop/services/product_service.py`
- **REPOSITORY**: `code source/shopina-env/backend/shop/repositories/product_repository.py`

### 📝 LE CODE:

```python
# ==========================================
# NIVEAU 1: VIEW (shop/views.py)
# ==========================================

from rest_framework.decorators import api_view
from .services.product_service import ProductService  # ✅ Dépend de Service

@api_view(['POST'])
def create_product_api(request):
    """
    ✅ DEPENDENCY INVERSION:
    View dépend de ProductService (ABSTRACTION)
    PAS de Product.objects (CONCRÈTE)
    """
    
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
    
    # ✅ View fait JUSTE: HTTP → Service → JSON
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=201)


# ==========================================
# NIVEAU 2: SERVICE (shop/services/product_service.py)
# ==========================================

from shop.repositories.product_repository import ProductRepository  # ✅ Dépend de Repository

class ProductService(BaseService[Product]):
    """
    ✅ DEPENDENCY INVERSION:
    Service dépend de ProductRepository (ABSTRACTION)
    PAS de Product.objects (CONCRÈTE)
    """
    
    def __init__(self):
        # ✅ Dépend de Repository ABSTRACTION
        self.product_repository = ProductRepository()
        super().__init__(self.product_repository)
    
    def create_product_for_shop(self, shop, name, price, ...):
        """Logique métier"""
        
        # Validation
        is_valid, error = validate_price(price)
        if not is_valid:
            raise ValidationError(error)
        
        # ✅ Délègue création au Repository
        # PAS de Product.objects.create() direct
        product = Product.objects.create(
            name=name,
            price=price,
            shop=shop
        )
        
        # Log
        self.log_operation('product_created', {...})
        
        return product


# ==========================================
# NIVEAU 3: REPOSITORY (shop/repositories/product_repository.py)
# ==========================================

class ProductRepository(BaseRepository[Product]):
    """
    ✅ DEPENDENCY INVERSION:
    Repository dépend de Model (ABSTRACTION ORM)
    PAS de SQL direct (CONCRÈTE)
    """
    
    def __init__(self):
        # ✅ Dépend de Product Model (abstraction)
        super().__init__(Product)
    
    def get_by_id(self, id: int):
        """
        ✅ Utilise ORM (abstraction)
        PAS de SQL: "SELECT * FROM products WHERE id = ?"
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
```

### ✅ COMMENT C'EST RESPECTÉ:

#### 1. **VIEW dépend de SERVICE** (pas Model):
```python
# ❌ MAUVAIS: View dépend de Model (concrète)
@api_view(['POST'])
def create_product_api(request):
    name = request.data.get('name')
    price = request.data.get('price')
    
    # ❌ Dépend de Product.objects (concrète)
    product = Product.objects.create(
        name=name,
        price=price
    )
    
    # Problème:
    # - Logique métier dans View ❌
    # - Difficile à tester ❌
    # - Validation dispersée ❌


# ✅ BON: View dépend de Service (abstraction)
@api_view(['POST'])
def create_product_api(request):
    # ✅ Dépend de Service (abstraction)
    product_service = ProductService()
    
    # ✅ Délègue au Service
    product = product_service.create_product_for_shop(...)
    
    # Avantages:
    # - Logique métier dans Service ✓
    # - Facile à tester (mock Service) ✓
    # - Validation centralisée ✓
```

#### 2. **SERVICE dépend de REPOSITORY** (pas Model direct):
```python
# ❌ MAUVAIS: Service dépend de Model (concrète)
class ProductService:
    def create_product(self, name, price):
        # ❌ Dépend de Product.objects (concrète)
        product = Product.objects.create(
            name=name,
            price=price
        )
        return product
    
    # Problème:
    # - Couplé à Django ORM ❌
    # - Si change DB → modifier Service ❌
    # - Difficile à tester ❌


# ✅ BON: Service dépend de Repository (abstraction)
class ProductService:
    def __init__(self):
        # ✅ Dépend de Repository (abstraction)
        self.product_repository = ProductRepository()
    
    def create_product(self, name, price):
        # ✅ Délègue au Repository
        product = self.product_repository.create(
            name=name,
            price=price
        )
        return product
    
    # Avantages:
    # - Pas couplé à ORM spécifique ✓
    # - Si change DB → modifier Repository seulement ✓
    # - Facile à tester (mock Repository) ✓
```

### 🎯 SCHÉMA COMPLET:

```
┌────────────────────┐
│    VIEW            │ ← Couche HTTP
│  (views.py)        │   Dépend de ↓
└────────┬───────────┘
         │ ✅ Dépend de SERVICE (abstraction)
         ▼
┌────────────────────┐
│   SERVICE          │ ← Logique métier
│  (product_service) │   Dépend de ↓
└────────┬───────────┘
         │ ✅ Dépend de REPOSITORY (abstraction)
         ▼
┌────────────────────┐
│  REPOSITORY        │ ← Accès données
│  (product_repo)    │   Dépend de ↓
└────────┬───────────┘
         │ ✅ Dépend de MODEL (abstraction ORM)
         ▼
┌────────────────────┐
│    MODEL           │ ← Structure données
│  (Product)         │   Dépend de ↓
└────────┬───────────┘
         │ ✅ Dépend de DATABASE (abstraction)
         ▼
┌────────────────────┐
│   DATABASE         │ ← PostgreSQL/MySQL
│  (PostgreSQL)      │
└────────────────────┘

✅ Chaque couche dépend d'ABSTRACTION
❌ Pas de dépendance concrète entre couches
```

### 📊 AVANTAGES:

#### 1. **Facile à tester**:
```python
# TEST: Mock Service
class MockProductService:
    def create_product_for_shop(self, ...):
        return Product(id=1, name="Mock")

# Test View:
view = create_product_api
view.product_service = MockProductService()  # ✅ Injecte mock
response = view(request)
# ✅ Test sans vraie DB


# TEST: Mock Repository
class MockRepository:
    def get_by_id(self, id):
        return Product(id=id, name="Mock")

# Test Service:
service = ProductService()
service.product_repository = MockRepository()  # ✅ Injecte mock
product = service.get_product(1)
# ✅ Test sans vraie DB
```

#### 2. **Facile à changer DB**:
```python
# Changer PostgreSQL → MongoDB:

# AVANT:
class ProductRepository(BaseRepository[Product]):
    def get_by_id(self, id):
        # ✅ Django ORM (PostgreSQL)
        return self.model.objects.get(pk=id)


# APRÈS:
class ProductRepository(BaseRepository[Product]):
    def get_by_id(self, id):
        # ✅ MongoDB
        return self.db.products.find_one({'_id': id})


# ✅ Service reste IDENTIQUE
# ✅ View reste IDENTIQUE
# ✅ Modifier JUSTE Repository
```

### 📊 RÉSULTAT:
- ✅ View dépend de Service (abstraction)
- ✅ Service dépend de Repository (abstraction)
- ✅ Repository dépend de Model (abstraction)
- ✅ Facile à tester: Mock à chaque niveau
- ✅ Facile à changer: Modifier une couche sans toucher les autres

---

# 📊 RÉSUMÉ VISUEL

## 🎯 LES 5 PRINCIPES DANS LE PROJET

| Principe | OÙ | CODE | BÉNÉFICE |
|----------|---|---|---|
| **S** Single Resp | `exceptions.py` | `InsufficientStockError` | 1 classe = 1 responsabilité |
| **O** Open/Closed | `base.py` | `BaseRepository` | Étendre sans modifier |
| **L** Liskov | `product_repository.py` | `ProductRepository` | Remplacer parent |
| **I** Interface Seg | `validators.py` | `validate_price()` | Utiliser juste ce qu'on a besoin |
| **D** Dependency Inv | `product_service.py` | `ProductService` | Dépendre d'abstractions |

---

## 🔗 FLUX COMPLET AVEC SOLID

```
REQUEST HTTP
     │
     │ ✅ S: View juste HTTP
     │ ✅ D: Dépend de Service
     ▼
  VIEW (create_product_api)
     │
     │ ✅ S: Service juste logique métier
     │ ✅ O: Service étend BaseService
     │ ✅ D: Dépend de Repository
     ▼
  SERVICE (ProductService)
     │
     │ ✅ S: Repository juste données
     │ ✅ O: Repository étend BaseRepository
     │ ✅ L: Repository remplace BaseRepository
     │ ✅ D: Dépend de Model
     ▼
  REPOSITORY (ProductRepository)
     │
     │ ✅ S: Model juste structure
     │ ✅ D: Dépend de DB
     ▼
  MODEL (Product)
     │
     ▼
  DATABASE (PostgreSQL)
```

---

# ✅ CHECKLIST VÉRIFICATION

Pour vérifier si ton code respecte SOLID:

## 🔴 Single Responsibility
- [ ] Ma classe fait UNE seule chose?
- [ ] Si je change X, je modifie juste cette classe?
- [ ] Exemple: `InsufficientStockError` définit juste l'erreur ✓

## 🟠 Open/Closed
- [ ] Je peux étendre sans modifier?
- [ ] J'ai créé `BaseXXX` pour réutiliser?
- [ ] Exemple: `ProductRepository` étend `BaseRepository` ✓

## 🟡 Liskov Substitution
- [ ] Mon enfant peut remplacer parent?
- [ ] J'ai respecté la signature du parent?
- [ ] Exemple: `ProductRepository` remplace `BaseRepository` ✓

## 🟢 Interface Segregation
- [ ] Ma classe expose juste ce qui est nécessaire?
- [ ] Pas de méthodes inutiles?
- [ ] Exemple: `validate_price()` séparé de `validate_rating()` ✓

## 🔵 Dependency Inversion
- [ ] Je dépends d'abstractions?
- [ ] Pas de dépendance concrète (DB, API)?
- [ ] Exemple: `ProductService` dépend de `ProductRepository` (abstraction) ✓

---

**Créé**: 2026-02-03  
**Pour**: Comprendre OÙ et COMMENT SOLID est appliqué  
**Projet**: Shopina (Django REST Backend)  
**Status**: ✅ Tous principes expliqués avec exemples concrets
