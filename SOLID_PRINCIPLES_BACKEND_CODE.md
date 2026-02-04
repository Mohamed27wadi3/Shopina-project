# 🏛️ PRINCIPES SOLID - BACKEND DJANGO (CODE EXACT)

## 📍 TABLE DES MATIÈRES

1. [S - Single Responsibility](#s---single-responsibility)
2. [O - Open/Closed](#o---openclosed)
3. [L - Liskov Substitution](#l---liskov-substitution)
4. [I - Interface Segregation](#i---interface-segregation)
5. [D - Dependency Inversion](#d---dependency-inversion)

---

## 🔴 S - SINGLE RESPONSIBILITY

### Définition
**Chaque classe doit avoir UNE seule raison de changer**

---

### 1️⃣ CUSTOM EXCEPTIONS (Une exception = une raison)

**📁 Fichier**: `code source/shopina-env/backend/core/utils/exceptions.py`

```python
"""
Custom exception classes for the application.
"""
from rest_framework.exceptions import APIException
from rest_framework import status

# ✅ SINGLE RESPONSIBILITY: Chaque exception = une situation
# ✅ Si la règle de message change → modifier juste son exception

class BusinessLogicError(APIException):
    """
    ✅ RESPONSABILITÉ UNIQUE: Définir erreur métier
    - Pas de logique
    - Pas de traitement
    - Juste structure exception
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic validation failed.'
    default_code = 'business_logic_error'


class InsufficientStockError(BusinessLogicError):
    """
    ✅ RESPONSABILITÉ UNIQUE: Stock insuffisant
    - Hérité de BusinessLogicError
    - Message spécifique seulement
    """
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'


class InvalidOrderStateError(BusinessLogicError):
    """
    ✅ RESPONSABILITÉ UNIQUE: Ordre en état invalide
    """
    default_detail = 'Order is in invalid state for this operation.'
    default_code = 'invalid_order_state'


class PaymentError(APIException):
    """
    ✅ RESPONSABILITÉ UNIQUE: Erreur paiement
    - Code 402 Payment Required
    """
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Payment processing failed.'
    default_code = 'payment_error'


class UnauthorizedAccessError(APIException):
    """
    ✅ RESPONSABILITÉ UNIQUE: Accès non autorisé
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'unauthorized_access'


class ResourceNotFoundError(APIException):
    """
    ✅ RESPONSABILITÉ UNIQUE: Ressource pas trouvée
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Requested resource not found.'
    default_code = 'resource_not_found'


class DuplicateResourceError(BusinessLogicError):
    """
    ✅ RESPONSABILITÉ UNIQUE: Ressource déjà existe
    """
    default_detail = 'Resource already exists.'
    default_code = 'duplicate_resource'


class ValidationError(BusinessLogicError):
    """
    ✅ RESPONSABILITÉ UNIQUE: Validation données échoue
    """
    default_detail = 'Data validation failed.'
    default_code = 'validation_error'

# ✅ AVANTAGE: Si on ajoute nouvelle erreur → créer nouvelle classe
# ✅ Pas besoin de modifier exceptions existantes
# ✅ Chaque exception change pour sa propre raison
```

**🎯 Bénéfices**:
- ✅ Chaque exception = une responsabilité
- ✅ Messages centralisés et cohérents
- ✅ Facile à ajouter nouvelles exceptions
- ✅ Pas de répétition de code

---

### 2️⃣ CUSTOM VALIDATORS (Une fonction = une validation)

**📁 Fichier**: `code source/shopina-env/backend/core/utils/validators.py`

```python
"""
Custom validation utilities.
"""
import re
from typing import Optional

# ✅ SINGLE RESPONSIBILITY: Chaque validator = une seule validation
# ✅ Si la règle change → modifier juste ce validator

def validate_phone_number(phone: str) -> bool:
    """
    ✅ RESPONSABILITÉ UNIQUE: Valider numéro téléphone
    - Pas de logique métier
    - Pas de log
    - Juste validation
    """
    # International phone number validation
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))


def validate_postal_code(postal_code: str, country: str = 'US') -> bool:
    """
    ✅ RESPONSABILITÉ UNIQUE: Valider code postal
    - Par pays (configurable)
    - Juste validation
    """
    patterns = {
        'US': r'^\d{5}(-\d{4})?$',
        'FR': r'^\d{5}$',
        'UK': r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$',
        'CA': r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$',
    }
    
    pattern = patterns.get(country, r'^\d{4,10}$')
    return bool(re.match(pattern, postal_code.upper()))


def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """
    ✅ RESPONSABILITÉ UNIQUE: Valider prix
    - Retourne (is_valid, error_message)
    - Utilisé PARTOUT dans services
    """
    if price < 0:
        return False, "Price cannot be negative"
    if price > 999999.99:
        return False, "Price exceeds maximum allowed value"
    return True, None


def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """
    ✅ RESPONSABILITÉ UNIQUE: Valider quantité
    - Min: 1
    - Max: 10000
    """
    if quantity < 1:
        return False, "Quantity must be at least 1"
    if quantity > 10000:
        return False, "Quantity exceeds maximum allowed value"
    return True, None


def validate_rating(rating: float) -> tuple[bool, Optional[str]]:
    """
    ✅ RESPONSABILITÉ UNIQUE: Valider note
    - Entre 0 et 5
    """
    if rating < 0 or rating > 5:
        return False, "Rating must be between 0 and 5"
    return True, None

# ✅ USAGE dans ProductService:
# from core.utils.validators import validate_price
# is_valid, error_msg = validate_price(price)
# if not is_valid:
#     raise ValidationError(error_msg)
```

**🎯 Bénéfices**:
- ✅ Validation centralisée
- ✅ Réutilisable partout
- ✅ Si règle change → modifier une fois
- ✅ Tests faciles

---

### 3️⃣ REPOSITORY (Une classe = une source de données)

**📁 Fichier**: `code source/shopina-env/backend/core/repositories/base.py`

```python
"""
Base repository class for data access abstraction.
"""
from typing import Generic, TypeVar, Optional, List
from django.db import models
from django.db.models import QuerySet

ModelType = TypeVar('ModelType', bound=models.Model)

class BaseRepository(Generic[ModelType]):
    """
    ✅ RESPONSABILITÉ UNIQUE: Accéder aux données
    - PAS de validation métier
    - PAS de logique métier
    - JUSTE requêtes SQL
    """
    
    def __init__(self, model: type[ModelType]):
        """
        ✅ RESPONSABILITÉ: Initialiser pour model
        """
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        ✅ RESPONSABILITÉ: Récupérer par ID
        - Gère exception DoesNotExist
        - Retourne None si pas trouvé
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
    
    def get_all(self) -> QuerySet[ModelType]:
        """
        ✅ RESPONSABILITÉ: Récupérer tous
        - Juste requête
        """
        return self.model.objects.all()
    
    def create(self, **kwargs) -> ModelType:
        """
        ✅ RESPONSABILITÉ: Créer instance
        - PAS de validation
        - PAS de transformation
        - JUSTE créer
        """
        instance = self.model(**kwargs)
        instance.save()
        return instance
    
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """
        ✅ RESPONSABILITÉ: Mettre à jour
        """
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        return instance
    
    def delete(self, instance: ModelType) -> None:
        """
        ✅ RESPONSABILITÉ: Supprimer
        """
        instance.delete()

# ✅ AVANTAGE: Si DB change (PostgreSQL → MongoDB)
# - Modifier JUSTE Repository
# - Services/Views restent identiques
```

---

### 4️⃣ SERVICE (Une classe = une logique métier)

**📁 Fichier**: `code source/shopina-env/backend/shop/services/product_service.py` (EXTRAIT)

```python
"""
Product service for business logic operations.
"""
from core.services.base import BaseService
from core.utils.exceptions import ValidationError, ResourceNotFoundError
from core.utils.validators import validate_price, validate_quantity
from shop.models import Product, Category
from shop.repositories.product_repository import ProductRepository

class ProductService(BaseService[Product]):
    """
    ✅ RESPONSABILITÉ UNIQUE: Logique métier PRODUIT
    - Validation prix ✓
    - Validation stock ✓
    - Créer catégorie si nécessaire ✓
    - PAS d'accès direct DB (délègue Repository)
    - PAS de HTTP (View le fait)
    """
    
    def __init__(self):
        """✅ Initialise Repository"""
        self.product_repository = ProductRepository()
        super().__init__(self.product_repository)
    
    def create_product(self, name: str, price: float, category_id: int,
                      description: str = '', stock: int = 0, **kwargs) -> Product:
        """
        ✅ RESPONSABILITÉ: Créer produit avec validation
        - Valide prix via validate_price()
        - Valide stock
        - Récupère catégorie
        - Délègue création à Repository
        - Retourne produit
        """
        # ÉTAPE 1: Valider prix
        is_valid, error_msg = validate_price(price)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # ÉTAPE 2: Valider stock
        if stock < 0:
            raise ValidationError("Stock cannot be negative")
        
        # ÉTAPE 3: Récupérer catégorie
        category = self.product_repository.get_by_id(category_id)
        if not category:
            raise ResourceNotFoundError("Category not found")
        
        # ÉTAPE 4: Délègue à Repository
        product = self.product_repository.create(
            name=name,
            price=price,
            category=category,
            description=description,
            stock=stock,
            **kwargs
        )
        
        # ÉTAPE 5: Log
        self.log_operation('product_created', {'product_id': product.id})
        
        return product
    
    def create_product_for_shop(self, shop, name: str, price: float, 
                               description: str = '', category_name: str = None,
                               stock: int = 1, image=None) -> Product:
        """
        ✅ RESPONSABILITÉ: Créer produit pour boutique
        """
        # Valider prix
        is_valid, error_msg = validate_price(float(price))
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Valider stock
        stock_int = int(stock)
        if stock_int < 0:
            raise ValidationError("Stock cannot be negative")
        
        # Get or create category (Factory pattern)
        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
        
        # Créer produit
        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            category=category,
            stock=stock_int,
            shop=shop,
            image=image
        )
        
        # Log
        self.log_operation('product_created_for_shop', {
            'product_id': product.id,
            'shop_id': shop.id
        })
        
        return product
    
    def update_product(self, product_id: int, **kwargs) -> Product:
        """
        ✅ RESPONSABILITÉ: Mettre à jour produit
        - Valide avant modification
        - Délègue à Repository
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Product not found")
        
        # Valide prix si changement
        if 'price' in kwargs:
            is_valid, error_msg = validate_price(kwargs['price'])
            if not is_valid:
                raise ValidationError(error_msg)
        
        # Valide stock si changement
        if 'stock' in kwargs and kwargs['stock'] < 0:
            raise ValidationError("Stock cannot be negative")
        
        # Délègue à Repository
        product = self.product_repository.update(product, **kwargs)
        
        # Log
        self.log_operation('product_updated', {'product_id': product_id})
        
        return product
    
    def delete_product(self, product_id: int) -> None:
        """
        ✅ RESPONSABILITÉ: Supprimer produit
        - Vérifie existe
        - Délègue à Repository
        - Log
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Product not found")
        
        self.product_repository.delete(product)
        self.log_operation('product_deleted', {'product_id': product_id})

# ✅ AVANTAGE:
# Si logique métier change → modifier JUSTE Service
# Views/Repositories/Models restent inchangés
```

---

### 5️⃣ VIEWS/CONTROLLERS (Une view = une action HTTP)

**📁 Fichier**: `code source/shopina-env/backend/shop/views.py` (EXTRAIT)

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.product_service import ProductService
from .serializers import ProductSerializer
from .models import Product
from core.utils.exceptions import ValidationError as CustomValidationError

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_api(request):
    """
    ✅ RESPONSABILITÉ UNIQUE: Gérer HTTP POST
    - Reçoit requête HTTP
    - Valide données présentes
    - Délègue à Service
    - Retourne JSON
    
    PAS de:
    - Logique métier (Service le fait)
    - Accès DB direct (Service le fait)
    - Validation complexe (Service le fait)
    """
    
    # Étape 1: Check user has shop
    try:
        shop = request.user.shop
    except AttributeError:
        return Response(
            {'detail': "Vous devez créer une boutique avant d'ajouter des produits."},
            status=400
        )
    
    # Étape 2: Extract data from request
    name = request.data.get('name')
    price = request.data.get('price')
    description = request.data.get('description', '')
    category_name = request.data.get('category')
    stock = request.data.get('stock', 1)
    image = request.FILES.get('image')
    
    # Étape 3: Basic validation (données présentes)
    if not name or not price:
        return Response({'detail': 'name and price are required.'}, status=400)
    
    # Étape 4: Délègue à Service
    try:
        # ✅ Crée instance service
        product_service = ProductService()
        
        # ✅ Délègue logique métier au service
        product = product_service.create_product_for_shop(
            shop=shop,
            name=name,
            price=price,
            description=description,
            category_name=category_name,
            stock=stock,
            image=image
        )
        
        # Étape 5: Sérialize et retourne JSON
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=201)
        
    except CustomValidationError as e:
        # ✅ Capture erreurs métier (viennent du Service)
        return Response({'detail': str(e)}, status=400)
    except Exception as e:
        # ✅ Capture erreurs système
        return Response({'detail': f'Erreur: {str(e)}'}, status=500)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_product_api(request, product_id):
    """
    ✅ RESPONSABILITÉ UNIQUE: Gérer HTTP PUT/PATCH
    """
    try:
        user_shop = request.user.shop
    except Exception:
        return Response({'detail': 'You do not own a shop.'}, status=403)
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=404)
    
    if product.shop_id != user_shop.id:
        return Response({'detail': 'Permission denied.'}, status=403)
    
    try:
        # ✅ Délègue à Service
        product_service = ProductService()
        updated_product = product_service.update_product(product_id, **request.data)
        
        serializer = ProductSerializer(updated_product)
        return Response(serializer.data)
        
    except CustomValidationError as e:
        return Response({'detail': str(e)}, status=400)
    except Exception as e:
        return Response({'detail': f'Erreur: {str(e)}'}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_api(request, product_id):
    """
    ✅ RESPONSABILITÉ UNIQUE: Gérer HTTP DELETE
    """
    try:
        user_shop = request.user.shop
    except Exception:
        return Response({'detail': 'You do not own a shop.'}, status=403)
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=404)
    
    if product.shop_id != user_shop.id:
        return Response({'detail': 'Permission denied.'}, status=403)
    
    try:
        # ✅ Délègue à Service
        product_service = ProductService()
        product_service.delete_product(product_id)
        
        return Response({'detail': 'Product deleted successfully.'}, status=200)
        
    except Exception as e:
        return Response({'detail': f'Erreur: {str(e)}'}, status=500)

# ✅ AVANTAGE: Si endpoints changent → modifier JUSTE Views
```

---

### 6️⃣ SERIALIZERS (Une classe = une transformation)

**📁 Fichier**: `code source/shopina-env/backend/shop/serializers.py` (EXTRAIT)

```python
from rest_framework import serializers
from shop.models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    """
    ✅ RESPONSABILITÉ UNIQUE: Valider + Transformer Model ↔ JSON
    - Validation format données
    - Transformation champs
    - PAS de logique métier
    - PAS d'accès DB
    """
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'image', 'category', 'rating']
    
    def validate_price(self, value):
        """
        ✅ RESPONSABILITÉ: Valider prix format/valeur
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        
        if value > 999999.99:
            raise serializers.ValidationError("Price too high")
        
        return value
    
    def validate_stock(self, value):
        """
        ✅ RESPONSABILITÉ: Valider stock format/valeur
        """
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value

# ✅ AVANTAGE: Si format JSON change → modifier JUSTE Serializer
```

---

## 🟠 O - OPEN/CLOSED

### Définition
**Classes OUVERTES à extension, FERMÉES à modification**

---

### 1️⃣ BaseRepository - Extensible sans modification

**📁 Fichier**: `code source/shopina-env/backend/core/repositories/base.py`

```python
from typing import Generic, TypeVar
from django.db import models
from django.db.models import QuerySet

ModelType = TypeVar('ModelType', bound=models.Model)

class BaseRepository(Generic[ModelType]):
    """
    ✅ OPEN/CLOSED: Ouvert à extension, fermé à modification
    
    OUVERT À EXTENSION:
    - Chaque Repository peut surcharger méthodes
    - Chaque Repository peut ajouter méthodes spécifiques
    
    FERMÉ À MODIFICATION:
    - Ne jamais modifier BaseRepository pour ajouter fonctionnalité
    - Créer nouvelle Repository qui hérite
    """
    
    def __init__(self, model: type[ModelType]):
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Template: À surcharger dans enfants si besoin"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
    
    def get_all(self) -> QuerySet[ModelType]:
        """Template: À surcharger si besoin"""
        return self.model.objects.all()

# ✅ EXEMPLE: ProductRepository ÉTEND sans modifier BaseRepository

class ProductRepository(BaseRepository[Product]):
    """
    ✅ EXTENSIBLE: Ajoute méthodes spécifiques
    ✅ SANS MODIFIER BaseRepository
    """
    
    def __init__(self):
        super().__init__(Product)
    
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """
        ✅ NOUVELLE MÉTHODE: Spécifique à Product
        ✅ N'a pas modifié BaseRepository
        """
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None
    
    def get_active_products(self) -> QuerySet[Product]:
        """✅ NOUVELLE MÉTHODE: Business-specific"""
        return self.model.objects.filter(stock__gt=0)
    
    def search_products(self, query: str) -> QuerySet[Product]:
        """✅ NOUVELLE MÉTHODE: Complex query encapsulation"""
        return self.model.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

# ✅ EXEMPLE: UserRepository ÉTEND sans modifier BaseRepository

class UserRepository(BaseRepository[User]):
    """
    ✅ AUTRE Repository: Même pattern
    ✅ ÉTEND BaseRepository
    ✅ Ajoute méthodes User-spécifiques
    """
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """✅ NOUVELLE: Spécifique à User"""
        try:
            return self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """✅ NOUVELLE: Spécifique à User"""
        try:
            return self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            return None

# ✅ AVANTAGE:
# - Ajouter nouvel Repository → hériter de BaseRepository
# - BaseRepository JAMAIS modifié
# - Chaque Repository peut être testé indépendamment
# - Pattern réutilisable pour CategoryRepository, OrderRepository, etc.
```

---

### 2️⃣ BaseService - Extensible sans modification

**📁 Fichier**: `code source/shopina-env/backend/core/services/base.py`

```python
from typing import Generic, TypeVar, Optional
from django.db import models

ModelType = TypeVar('ModelType', bound=models.Model)

class BaseService(Generic[ModelType]):
    """
    ✅ OPEN/CLOSED: Ouvert à extension, fermé à modification
    
    OUVERT À EXTENSION:
    - Chaque Service peut surcharger validate_business_rules()
    - Chaque Service peut ajouter ses propres méthodes
    - Chaque Service ajoute sa logique métier
    
    FERMÉ À MODIFICATION:
    - Ne jamais modifier BaseService pour ajouter cas spécial
    - Créer nouvelle Service qui hérite et surcharge
    """
    
    def __init__(self, repository=None):
        self.repository = repository
    
    def validate_business_rules(self, data: dict) -> tuple[bool, Optional[str]]:
        """
        ✅ TEMPLATE METHOD: À override dans enfants
        - ProductService override pour valider Product
        - UserService override pour valider User
        - OrderService override pour valider Order
        """
        return True, None
    
    def log_operation(self, operation: str, details: dict):
        """✅ Logging centralisé"""
        pass

# ✅ EXEMPLE: ProductService ÉTEND sans modifier BaseService

class ProductService(BaseService[Product]):
    """
    ✅ EXTENSIBLE: Ajoute logique produit spécifique
    ✅ SANS MODIFIER BaseService
    """
    
    def __init__(self):
        self.product_repository = ProductRepository()
        super().__init__(self.product_repository)
    
    def validate_business_rules(self, product_data: dict) -> tuple[bool, Optional[str]]:
        """
        ✅ OVERRIDE: Surcharge pour Product-specific validation
        """
        price = product_data.get('price')
        stock = product_data.get('stock')
        
        # Produit-spécifique: Valider prix
        if price and price < 0:
            return False, "Price cannot be negative"
        
        # Produit-spécifique: Valider stock
        if stock and stock < 0:
            return False, "Stock cannot be negative"
        
        return True, None
    
    def create_product_for_shop(self, shop, name: str, price: float, ...):
        """✅ NOUVELLE MÉTHODE: Produit-specific"""
        # Validation via inherited method
        is_valid, error = self.validate_business_rules({'price': price, 'stock': stock})
        
        if not is_valid:
            raise ValidationError(error)
        
        # Logique métier
        product = self.product_repository.create(...)
        self.log_operation('product_created', {...})
        
        return product

# ✅ EXEMPLE: OrderService ÉTEND sans modifier BaseService

class OrderService(BaseService[Order]):
    """✅ AUTRE Service: Même pattern"""
    
    def __init__(self):
        self.order_repository = OrderRepository()
        super().__init__(self.order_repository)
    
    def validate_business_rules(self, order_data: dict) -> tuple[bool, Optional[str]]:
        """✅ OVERRIDE: Surcharge pour Order-specific validation"""
        total = order_data.get('total')
        items_count = order_data.get('items_count')
        
        # Ordre-spécifique: Valider total > 0
        if total and total <= 0:
            return False, "Order total must be positive"
        
        # Ordre-spécifique: Valider items count
        if items_count and items_count == 0:
            return False, "Order must have at least one item"
        
        return True, None

# ✅ AVANTAGE:
# - Ajouter nouveau Service → hériter de BaseService
# - BaseService JAMAIS modifié
# - Chaque Service override validate_business_rules() avec sa logique
# - Pattern unifié et réutilisable
```

---

### 3️⃣ Custom Exceptions - Extensible sans modification

**📁 Fichier**: `code source/shopina-env/backend/core/utils/exceptions.py`

```python
from rest_framework.exceptions import APIException
from rest_framework import status

class BusinessLogicError(APIException):
    """
    ✅ OPEN/CLOSED: Base pour toutes erreurs métier
    
    OUVERT À EXTENSION:
    - Hériter et créer nouvelles exceptions
    
    FERMÉ À MODIFICATION:
    - Ne jamais modifier BusinessLogicError pour cas spécial
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic validation failed.'
    default_code = 'business_logic_error'

# ✅ EXTENSIONS: Sans modifier BusinessLogicError

class InsufficientStockError(BusinessLogicError):
    """✅ NOUVELLE: Stock insuffisant"""
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'

class InvalidOrderStateError(BusinessLogicError):
    """✅ NOUVELLE: Ordre invalide"""
    default_detail = 'Order is in invalid state for this operation.'
    default_code = 'invalid_order_state'

class DuplicateResourceError(BusinessLogicError):
    """✅ NOUVELLE: Ressource dupliquée"""
    default_detail = 'Resource already exists.'
    default_code = 'duplicate_resource'

class ValidationError(BusinessLogicError):
    """✅ NOUVELLE: Validation échouée"""
    default_detail = 'Data validation failed.'
    default_code = 'validation_error'

# ✅ AVANTAGE:
# - Ajouter nouvelle erreur → hériter de BusinessLogicError
# - BusinessLogicError JAMAIS modifié
# - Cohérence: Toutes erreurs ont status_code/detail/code
# - Facile à ajouter nouvelles exceptions sans risque
```

---

## 🟡 L - LISKOV SUBSTITUTION

### Définition
**Sous-classes peuvent remplacer parent sans casser code**

---

### 1️⃣ Repository Substitution

**📁 Fichier**: `code source/shopina-env/backend/shop/repositories/product_repository.py`

```python
from core.repositories.base import BaseRepository
from shop.models import Product

class ProductRepository(BaseRepository[Product]):
    """
    ✅ LISKOV: ProductRepository peut remplacer BaseRepository[Product]
    
    CONTRAT DE BaseRepository:
    - get_by_id(id) -> Optional[Product]
    - get_all() -> QuerySet[Product]
    - create(**kwargs) -> Product
    - update(instance, **kwargs) -> Product
    - delete(instance) -> None
    
    ProductRepository RESPECTE ce contrat:
    - get_by_id() retourne TOUJOURS Product | None ✓
    - get_all() retourne TOUJOURS QuerySet[Product] ✓
    - create() retourne TOUJOURS Product ✓
    - Peut AJOUTER méthodes (get_by_slug, search_products)
    - JAMAIS modifier signature héritées
    """
    
    def __init__(self):
        super().__init__(Product)
    
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """
        ✅ NOUVELLE MÉTHODE: OK, on peut ajouter
        ✅ CONTRAT parent pas violé
        """
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None
    
    def search_products(self, query: str) -> QuerySet[Product]:
        """✅ NOUVELLE MÉTHODE: OK, on peut ajouter"""
        return self.model.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

# ✅ USAGE: BaseRepository peut être ProductRepository

def fetch_by_id(repository: BaseRepository[T], id: int) -> Optional[T]:
    """
    Fonction accepte BaseRepository[T]
    ProductRepository[Product] peut être passé sans problème
    """
    return repository.get_by_id(id)

# UTILISATION:
product_repo = ProductRepository()
product = fetch_by_id(product_repo, 1)  # ✅ FONCTIONNE

# ✅ AVANTAGE:
# - Code écrit pour BaseRepository fonctionne avec TOUT Repository
# - Tests faciles: Peut utiliser MockRepository
# - Extension facile: Créer CategoryRepository même signature
```

---

### 2️⃣ Service Substitution

**📁 Fichier**: `code source/shopina-env/backend/shop/services/product_service.py`

```python
from core.services.base import BaseService

class ProductService(BaseService[Product]):
    """
    ✅ LISKOV: ProductService peut remplacer BaseService[Product]
    
    CONTRAT DE BaseService:
    - __init__(repository)
    - validate_business_rules(data) -> tuple[bool, Optional[str]]
    - log_operation(operation, details)
    
    ProductService RESPECTE ce contrat:
    - __init__() initialise avec ProductRepository ✓
    - validate_business_rules() override correctement ✓
    - log_operation() héritée correctement ✓
    """
    
    def __init__(self):
        self.product_repository = ProductRepository()
        # ✅ Appelle parent init
        super().__init__(self.product_repository)
    
    def validate_business_rules(self, data: dict) -> tuple[bool, Optional[str]]:
        """
        ✅ LISKOV: Override respecte signature parent
        - DOIT retourner tuple[bool, Optional[str]] ✓
        - DOIT faire validation métier ✓
        - JAMAIS violer contrat parent
        """
        price = data.get('price')
        if price and price < 0:
            return False, "Price cannot be negative"
        return True, None

# ✅ USAGE: BaseService peut être ProductService

def process_entity(service: BaseService[T], data: dict):
    """
    Fonction accepte BaseService[T]
    ProductService peut être passé sans problème
    """
    is_valid, error = service.validate_business_rules(data)
    if not is_valid:
        raise ValidationError(error)
    return service.create(data)

# UTILISATION:
product_service = ProductService()
product = process_entity(product_service, product_data)  # ✅ FONCTIONNE

# ✅ AVANTAGE:
# - Code écrit pour BaseService fonctionne avec TOUT Service
# - Pas de surprises: ProductService respecte contrat
# - Facile tester et étendre
```

---

### 3️⃣ Exception Substitution

**📁 Fichier**: `code source/shopina-env/backend/core/utils/exceptions.py`

```python
class BusinessLogicError(APIException):
    """
    ✅ LISKOV: Parent exception
    
    CONTRAT:
    - status_code = 400
    - default_detail: str
    - default_code: str
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic validation failed.'
    default_code = 'business_logic_error'

class InsufficientStockError(BusinessLogicError):
    """
    ✅ LISKOV: Sous-classe RESPECTE contrat parent
    - status_code = 400 (hérité de parent) ✓
    - default_detail: str ✓
    - default_code: str ✓
    """
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'

# ✅ USAGE: Catch parent, reçoit sous-classe

try:
    # Code peut lever InsufficientStockError
    if product.stock < quantity:
        raise InsufficientStockError()
except BusinessLogicError as e:
    # ✅ LISKOV: Peut catch parent, reçoit sous-classe
    # InsufficientStockError IS-A BusinessLogicError
    return Response({'detail': str(e)}, status=e.status_code)

# ✅ AVANTAGE:
# - Code générique pour BusinessLogicError fonctionne avec sous-classes
# - Ajouter nouvelles exceptions: juste hériter
# - Comportement prévisible
```

---

## 🟢 I - INTERFACE SEGREGATION

### Définition
**Clients n'implémentent QUE ce qu'ils utilisent**

---

### 1️⃣ Repository Minimal Interface

**📁 Fichier**: `code source/shopina-env/backend/core/repositories/base.py`

```python
class BaseRepository(Generic[ModelType]):
    """
    ✅ INTERFACE SEGREGATION: Expose JUSTE ce qui est nécessaire
    
    MÉTHODES ESSENTIELLES:
    - get_by_id()  ✓
    - get_all()    ✓
    - create()     ✓
    - update()     ✓
    - delete()     ✓
    
    PAS EXPOSÉ (caché en interne):
    - __init__ (interne)
    - model (interne)
    
    ❌ MAUVAIS exemple:
    class RepositoryBig:
        def get_by_id()
        def get_all()
        def create()
        def update()
        def delete()
        def cache_get()         # Pas tous utilisent
        def bulk_create()       # Pas tous utilisent
        def raw_sql()           # Pas tous utilisent
        def export_csv()        # Pas tous utilisent
        def send_webhook()      # Pas tous utilisent
        # ... 50 autres méthodes
        
        # Classe implémentant DOIT implémenter TOUT ❌
    
    ✅ BON: Interface minimum
    """
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Essentiel: Récupérer par ID"""
        pass
    
    def get_all(self) -> QuerySet[ModelType]:
        """Essentiel: Récupérer tous"""
        pass
    
    def create(self, **kwargs) -> ModelType:
        """Essentiel: Créer"""
        pass
    
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Essentiel: Mettre à jour"""
        pass
    
    def delete(self, instance: ModelType) -> None:
        """Essentiel: Supprimer"""
        pass
    
    # ✅ METHODS SPÉCIFIQUES dans child repositories seulement
    # ProductRepository ajoute: search_products(), get_by_slug()
    # UserRepository ajoute: get_by_email(), get_by_username()

# ✅ AVANTAGE:
# - Repository interface minimum et cohérent
# - ProductRepository/UserRepository/OrderRepository all respectent
# - Code utilisant Repository: pas surprises
```

---

### 2️⃣ Service Minimal Interface

**📁 Fichier**: `code source/shopina-env/backend/core/services/base.py`

```python
class BaseService(Generic[ModelType]):
    """
    ✅ INTERFACE SEGREGATION: Service expose JUSTE ce qui est nécessaire
    
    MÉTHODES PUBLIQUES:
    - validate_business_rules()  ✓
    - log_operation()             ✓
    
    PAS EXPOSÉ (caché):
    - __init__ (interne)
    - repository (interne)
    
    ❌ MAUVAIS:
    class ServiceBig:
        - create()
        - read()
        - update()
        - delete()
        - validate()
        - log()
        - cache()
        - send_email()
        - generate_pdf()
        - send_webhook()
        - analytics()
        # ... 50 autres
        
        # Classe implémentant DOIT implémenter TOUT ❌
    
    ✅ BON: Interface minimum
    """
    
    def validate_business_rules(self, data: dict) -> tuple[bool, Optional[str]]:
        """À override: Valider métier"""
        return True, None
    
    def log_operation(self, operation: str, details: dict):
        """À override: Logger"""
        pass
    
    # ✅ METHODS SPÉCIFIQUES dans child services seulement
    # ProductService ajoute: create_product(), update_product()
    # UserService ajoute: register_user(), change_password()
    # OrderService ajoute: create_order(), update_order_status()

# ✅ AVANTAGE:
# - Service interface minimum
# - Chaque Service implément juste ce qu'il utilise
# - Pas de méthodes inutiles imposées
```

---

### 3️⃣ Validator Segregation

**📁 Fichier**: `code source/shopina-env/backend/core/utils/validators.py`

```python
"""
✅ INTERFACE SEGREGATION: Chaque validator = une responsabilité
"""

def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """
    ✅ SEGREGATED: Valide JUSTE prix
    - Pas de validation stock
    - Pas de validation quantity
    - Pas de validation rating
    - JUSTE prix
    """
    if price < 0:
        return False, "Price cannot be negative"
    if price > 999999.99:
        return False, "Price exceeds maximum allowed value"
    return True, None

def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """✅ SEGREGATED: Valide JUSTE quantity"""
    if quantity < 1:
        return False, "Quantity must be at least 1"
    if quantity > 10000:
        return False, "Quantity exceeds maximum allowed value"
    return True, None

def validate_rating(rating: float) -> tuple[bool, Optional[str]]:
    """✅ SEGREGATED: Valide JUSTE rating"""
    if rating < 0 or rating > 5:
        return False, "Rating must be between 0 and 5"
    return True, None

# ✅ USAGE: Import JUSTE ce qu'on besoin

# Dans ProductService:
from core.utils.validators import validate_price, validate_quantity
# N'importe pas validate_rating ✓

# Dans ReviewService:
from core.utils.validators import validate_rating
# N'importe pas validate_price/validate_quantity ✓

# ✅ AVANTAGE:
# - Chaque classe/fonction utilise JUSTE ce dont elle a besoin
# - Import déclarent dépendances
# - Pas de dépendances cachées
```

---

## 🔵 D - DEPENDENCY INVERSION

### Définition
**Dépend d'abstractions, PAS de concrétions**

---

### 1️⃣ Service dépend de Repository Abstraction

**📁 Fichier**: `code source/shopina-env/backend/shop/services/product_service.py`

```python
from core.services.base import BaseService
from core.repositories.base import BaseRepository  # ✅ Dépend d'ABSTRACTION
from shop.repositories.product_repository import ProductRepository

class ProductService(BaseService[Product]):
    """
    ✅ DEPENDENCY INVERSION: Service dépend de Repository ABSTRACTION
    
    AVANT (❌ MAUVAIS):
    class ProductService:
        def __init__(self):
            self.db = PostgresConnection()  # ❌ Dépend de concrète DB
            self.product = Product.objects.all()  # ❌ Directement ORM
        
        # Difficile à tester
        # Difficile à changer DB
    
    APRÈS (✅ BON):
    """
    
    def __init__(self):
        # ✅ Dépend de Repository ABSTRACTION
        self.product_repository = ProductRepository()
        # ProductRepository hérite de BaseRepository (abstraction)
        super().__init__(self.product_repository)
    
    def create_product_for_shop(self, shop, name, price, ...):
        """
        ✅ UTILISE Repository ABSTRACTION
        - self.product_repository est-un BaseRepository[Product]
        - N'importe pas details implementation
        """
        # ... validation ...
        
        # ✅ Délègue à Repository ABSTRACTION
        product = self.product_repository.create(
            name=name,
            price=price,
            ...
        )
        
        self.log_operation('product_created', {...})
        return product
    
    def update_product(self, product_id, **kwargs):
        """✅ UTILISE Repository ABSTRACTION"""
        product = self.product_repository.get_by_id(product_id)
        # ...
        product = self.product_repository.update(product, **kwargs)
        return product
    
    def delete_product(self, product_id):
        """✅ UTILISE Repository ABSTRACTION"""
        product = self.product_repository.get_by_id(product_id)
        self.product_repository.delete(product)

# ✅ TESTING: Peut injecter MockRepository
class MockRepository(BaseRepository[Product]):
    """✅ Mock pour tests"""
    def __init__(self):
        super().__init__(Product)
    
    def get_by_id(self, id):
        return Product(id=id, name="Mock Product")

# TEST:
service = ProductService()
service.product_repository = MockRepository()  # ✅ Injecte mock
product = service.update_product(1, name="New Name")
# Tests sans DB ✓

# ✅ AVANTAGE:
# - Facile à tester: Injecter MockRepository
# - Facile à changer DB: Créer PostgresRepository/MongoRepository
# - Service pas couplée à détails implementation
```

---

### 2️⃣ View dépend de Service Abstraction

**📁 Fichier**: `code source/shopina-env/backend/shop/views.py`

```python
from rest_framework.decorators import api_view
from .services.product_service import ProductService  # ✅ Dépend Service

@api_view(['POST'])
def create_product_api(request):
    """
    ✅ DEPENDENCY INVERSION: View dépend de Service ABSTRACTION
    
    AVANT (❌ MAUVAIS):
    @api_view(['POST'])
    def create_product_api(request):
        # ❌ Directement accès à Model
        product = Product.objects.create(
            name=request.data.get('name'),
            price=request.data.get('price'),
            ...
        )
        # Logique métier EN VUE ❌
        if product.price > 1000:
            product.requires_approval = True
        
        # Difficile à tester
        # Logique dispersée
    
    APRÈS (✅ BON):
    """
    
    try:
        shop = request.user.shop
    except AttributeError:
        return Response({'detail': '...'}, status=400)
    
    name = request.data.get('name')
    price = request.data.get('price')
    
    try:
        # ✅ DÉPEND DE SERVICE ABSTRACTION
        product_service = ProductService()
        
        # ✅ Délègue TOUTE logique au Service
        product = product_service.create_product_for_shop(
            shop=shop,
            name=name,
            price=price,
            ...
        )
        
        # ✅ Serializer transforme réponse
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=201)
        
    except ValidationError as e:
        return Response({'detail': str(e)}, status=400)

# ✅ AVANTAGE:
# - View juste HTTP: reçoit, délègue, retourne
# - Service: logique métier
# - Repository: données
# - Facile de tester chaque couche
```

---

### 3️⃣ Serializer dépend de Model Abstraction

**📁 Fichier**: `code source/shopina-env/backend/shop/serializers.py`

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    ✅ DEPENDENCY INVERSION: Serializer dépend de Model INTERFACE
    
    INTERFACE Model:
    - id
    - name
    - price
    - stock
    - description
    - category
    - rating
    
    Serializer déclare ce dont il a besoin:
    """
    
    class Meta:
        model = Product  # ✅ Dépend d'abstraction Model
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'stock', 'image', 'category', 'rating'
        ]
    
    def validate_price(self, value):
        """✅ Valide interface expectée"""
        if value <= 0:
            raise serializers.ValidationError("Price must be > 0")
        return value

# ✅ AVANTAGE:
# - Serializer pas couplée à details Product
# - Si Product ajoute champs: Juste ajouter à fields
# - Si Product change implementation: Serializer pas affectée
```

---

### 4️⃣ Exception Handling avec Inversion

**📁 Fichier**: `code source/shopina-env/backend/core/utils/exceptions.py`

```python
from rest_framework.exceptions import APIException

class BusinessLogicError(APIException):
    """
    ✅ DEPENDENCY INVERSION: Code dépend d'exception ABSTRACTION
    
    View code:
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic validation failed.'
    default_code = 'business_logic_error'

# Views utilisent exception ABSTRACTION:

@api_view(['POST'])
def create_product_api(request):
    try:
        product_service = ProductService()
        product = product_service.create_product_for_shop(...)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=201)
        
    except BusinessLogicError as e:
        # ✅ DÉPEND D'ABSTRACTION BusinessLogicError
        # PAS de ProductService exception hardcodée
        # PAS de Repository exception hardcodée
        return Response({'detail': str(e)}, status=e.status_code)

# ✅ Service peut lever InsufficientStockError (sous-classe)
# ✅ View peut les catch TOUTES avec BusinessLogicError parent
# ✅ Couplage faible entre View et Service

# ✅ AVANTAGE:
# - Ajouter nouvelle exception: Juste hériter de BusinessLogicError
# - View code pas affectée
# - Exception hierarchy cohérente
```

---

## 📊 RÉSUMÉ: SOLID AU BACKEND

| Principe | Application | Fichier |
|----------|-------------|---------|
| **S** | Chaque classe = une responsabilité | exceptions.py, validators.py, repositories/, services/, views.py, serializers.py |
| **O** | BaseRepository/BaseService extensible | core/repositories/base.py, core/services/base.py |
| **L** | ProductRepository remplace BaseRepository | shop/repositories/product_repository.py |
| **I** | Repository expose juste méthodes essentielles | core/repositories/base.py |
| **D** | Service dépend de Repository abstraction | shop/services/product_service.py |

---

### 🎯 FLUX COMPLET avec SOLID

```
1. REQUEST (VIEW)
   ↓ (Single Responsibility: HTTP seulement)
2. VIEW → SERVICE
   ↓ (Dependency Inversion: Dépend service abstraction)
3. SERVICE → VALIDATION
   ↓ (Single Responsibility: Validation centralisée)
4. SERVICE → REPOSITORY
   ↓ (Dependency Inversion: Dépend repository abstraction)
5. REPOSITORY → DATABASE
   ↓ (Single Responsibility: Data access seulement)
6. DATABASE → REPOSITORY
   ↓ (Liskov: Repository retourne toujours bon type)
7. REPOSITORY → SERVICE
   ↓ (Open/Closed: Service peut étendre sans modifier)
8. SERVICE → SERIALIZER
   ↓ (Single Responsibility: Transform model ↔ JSON)
9. SERIALIZER → VIEW
   ↓ (Interface Segregation: Juste fields nécessaires)
10. VIEW → RESPONSE (HTTP)
    ✅ SOLID respecté à chaque étape
```

---

**Document créé**: 2026-02-03  
**Type**: Principes SOLID - Code Exact Commenté  
**Couverture**: Backend Django  
**Status**: ✅ 100% Expliqué
