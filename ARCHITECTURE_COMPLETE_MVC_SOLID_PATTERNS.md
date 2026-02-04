# 🏛️ ARCHITECTURE COMPLÈTE: MVC + SOLID + DESIGN PATTERNS

## 📍 TABLE DES MATIÈRES
1. [Architecture MVC](#architecture-mvc)
2. [Principes SOLID](#principes-solid)
3. [Design Patterns Utilisés](#design-patterns-utilisés)
4. [Localisation des Composants](#localisation-des-composants)

---

## 🏗️ ARCHITECTURE MVC

### Qu'est-ce que MVC?
- **Model**: Logique métier + accès données
- **View**: Présentation (UI)
- **Controller**: Orchestration + requêtes HTTP

---

## BACKEND (Django REST Framework)

### 1️⃣ LAYER: MODEL (Données)

**Localisation**: `code source/shopina-env/backend/[app]/models.py`

#### Exemple: Product Model
```
📁 shop/models.py
   └─ class Product(models.Model)
      ├─ name: CharField
      ├─ price: DecimalField
      ├─ shop: ForeignKey(Shop)
      ├─ stock: PositiveIntegerField
      └─ save() -> génère slug unique
```

**Où trouver**:
- [Product Model](code%20source/shopina-env/backend/shop/models.py)
- [Shop Model](code%20source/shopina-env/backend/shops/models.py)
- [User Model](code%20source/shopina-env/backend/users/models.py)

**SOLID appliqué**:
- ✅ Single Responsibility: Chaque model gère UNE entité
- ✅ Open/Closed: Extensible via héritage
- ✅ Liskov Substitution: Tous les models héritent de models.Model

---

### 2️⃣ LAYER: REPOSITORY (Data Access)

**Localisation**: `code source/shopina-env/backend/[app]/repositories/`

```
📁 shop/repositories/
   ├─ __init__.py
   └─ product_repository.py
      ├─ class ProductRepository(BaseRepository[Product])
      │  ├─ get_by_slug()
      │  ├─ get_active_products()
      │  ├─ search_products()
      │  ├─ update_stock()
      │  └─ update_rating()
```

**Où trouver**:
- [ProductRepository](code%20source/shopina-env/backend/shop/repositories/product_repository.py#L1-L50)
- [UserRepository](code%20source/shopina-env/backend/users/repositories/user_repository.py)
- [BaseRepository](code%20source/shopina-env/backend/core/repositories/base.py)

**SOLID appliqué**:
- ✅ Single Responsibility: UNE classe = UNE table
- ✅ Dependency Inversion: Service → Repository (abstraction)
- ✅ Interface Segregation: Méthodes spécifiques

**Design Pattern**:
- 🎯 **Repository Pattern**: Abstrait les requêtes SQL
- 🎯 **Generic/Base Class**: `BaseRepository[T]` réutilisable

---

### 3️⃣ LAYER: SERVICE (Business Logic)

**Localisation**: `code source/shopina-env/backend/[app]/services/`

```
📁 shop/services/
   └─ product_service.py
      ├─ class ProductService(BaseService[Product])
      │  ├─ create_product_for_shop()
      │  │  ├─ validate_price()
      │  │  ├─ validate_stock()
      │  │  ├─ get_or_create_category()
      │  │  └─ Product.objects.create()
      │  ├─ update_product()
      │  │  ├─ validation
      │  │  └─ repository.update()
      │  ├─ delete_product()
      │  ├─ decrease_stock()
      │  └─ increase_stock()
```

**Où trouver**:
- [ProductService](code%20source/shopina-env/backend/shop/services/product_service.py#L1-L100)
- [UserService](code%20source/shopina-env/backend/users/services/user_service.py)
- [BaseService](code%20source/shopina-env/backend/core/services/base.py)

**SOLID appliqué**:
- ✅ Single Responsibility: Logique métier UNI UNIQUE
- ✅ Open/Closed: Extensible sans modification
- ✅ Liskov Substitution: Tous héritent de BaseService
- ✅ Interface Segregation: Méthodes focalisées

**Design Pattern**:
- 🎯 **Service Locator**: Centralize business logic
- 🎯 **Template Method**: `BaseService` définit le pattern
- 🎯 **Validation Chain**: Valide avant de créer

**Exemple de flux**:
```python
# Validation → Métier → Persistence
def create_product_for_shop(self, shop, name, price, ...):
    validate_price(price)           # 1️⃣ Validation
    validate_stock(stock)           # 2️⃣ Validation
    category = get_or_create()      # 3️⃣ Métier
    product = Product.create()      # 4️⃣ Persistence
    log_operation()                 # 5️⃣ Audit
    return product
```

---

### 4️⃣ LAYER: SERIALIZER (DTO - Data Transfer Object)

**Localisation**: `code source/shopina-env/backend/[app]/serializers.py`

```
📁 shop/serializers.py
   ├─ class ProductSerializer(serializers.ModelSerializer)
   │  ├─ Meta:
   │  │  ├─ model = Product
   │  │  └─ fields = [...]
   │  ├─ validate_price()      # Validation de couche
   │  └─ to_representation()   # Transformation sortie
```

**Où trouver**:
- [ProductSerializer](code%20source/shopina-env/backend/shop/serializers.py)
- [UserSerializer](code%20source/shopina-env/backend/users/serializers.py)

**SOLID appliqué**:
- ✅ Single Responsibility: UNE classe = UNE validation
- ✅ Dependency Inversion: Abstrait la sérialisation

**Design Pattern**:
- 🎯 **DTO Pattern**: Transfert sécurisé des données
- 🎯 **Validation Decorator**: `@validator` methods

---

### 5️⃣ LAYER: VIEW/CONTROLLER (HTTP)

**Localisation**: `code source/shopina-env/backend/[app]/views.py`

```
📁 shop/views.py
   ├─ @api_view(['POST'])
   ├─ @permission_classes([IsAuthenticated])
   ├─ def create_product_api(request):
   │  ├─ 1️⃣ Authentification
   │  ├─ 2️⃣ Validation
   │  ├─ 3️⃣ ProductService.create_product_for_shop()
   │  ├─ 4️⃣ Sérialisation
   │  └─ 5️⃣ Response
```

**Où trouver**:
- [create_product_api](code%20source/shopina-env/backend/shop/views.py#L40-L85)
- [update_product_api](code%20source/shopina-env/backend/shop/views.py#L104-L150)
- [delete_product_api](code%20source/shopina-env/backend/shop/views.py#L152-L185)

**SOLID appliqué**:
- ✅ Single Responsibility: Gère HTTP UNIQUEMENT
- ✅ Dependency Inversion: Utilise Service (abstraction)
- ✅ Open/Closed: Facile d'ajouter new endpoints

**Design Pattern**:
- 🎯 **Controller Pattern**: Orchestration requêtes
- 🎯 **Decorator Pattern**: `@api_view`, `@permission_classes`
- 🎯 **Chain of Responsibility**: Auth → Validation → Logic

---

### 6️⃣ Exemple Complet: Créer un Produit

```
REQUEST (Vue/Frontend)
    ↓
CONTROLLER (views.py:create_product_api)
    ├─ Validation: name, price requis ✓
    ├─ Authentification: user a shop ✓
    └─ appelle ProductService.create_product_for_shop()
         ↓
SERVICE (services/product_service.py)
    ├─ Validation: prix > 0 ✓
    ├─ Validation: stock ≥ 0 ✓
    ├─ Métier: créer ou récupérer category
    └─ appelle ProductRepository.create()
         ↓
REPOSITORY (repositories/product_repository.py)
    └─ Appelle ProductRepository.create()
         ↓
MODEL (models.py)
    ├─ Product.objects.create()
    ├─ save() → génère slug unique
    └─ retourne Product instance
         ↓
SERIALIZER (serializers.py)
    └─ ProductSerializer(product).data
         ↓
CONTROLLER
    └─ Response(data, status=201)
         ↓
JSON → FRONTEND
```

---

## FRONTEND (React + TypeScript)

### Architecture MVC Frontend

#### 🔵 MODEL: Context + Hooks (État + Logique)

**Localisation**: `code source/front/src/context/`

```
📁 context/
   ├─ AuthContext.tsx
   │  ├─ user state
   │  ├─ tokens (access, refresh)
   │  ├─ login(identifier, password)
   │  ├─ logout()
   │  ├─ refreshProfile()
   │  └─ refreshToken()
   └─ ThemeLanguageContext.tsx
```

**Où trouver**:
- [AuthContext](code%20source/front/src/context/AuthContext.tsx#L1-L50)

**SOLID appliqué**:
- ✅ Single Responsibility: UNE source de vérité
- ✅ Dependency Inversion: Fournisseurs abstraits

**Design Pattern**:
- 🎯 **Context API Pattern**: Gestion d'état centralisée
- 🎯 **Provider Pattern**: `AuthProvider` wrapper

---

#### 🟢 VIEW: Pages + Composants (Présentation)

**Localisation**: `code source/front/src/pages/` et `code source/front/src/components/`

```
📁 pages/
   ├─ LoginPage.tsx        ← Écran de connexion
   ├─ MyShopPage.tsx        ← Tableau de bord boutique
   ├─ ShopPage.tsx          ← Affichage public
   ├─ TemplatesPage.tsx     ← Sélection templates
   ├─ CheckoutPage.tsx      ← Paiement
   └─ ...

📁 components/
   ├─ Header.tsx            ← Navigation
   ├─ Footer.tsx            ← Pied de page
   ├─ DashboardHeader.tsx   ← Dashboard header
   ├─ DashboardSidebar.tsx  ← Sidebar
   ├─ CTA.tsx               ← Call-to-action
   └─ ...
```

**Où trouver**:
- [MyShopPage](code%20source/front/src/pages/MyShopPage.tsx) - Gestion produits
- [ShopPage](code%20source/front/src/pages/ShopPage.tsx) - Affichage boutique
- [TemplatesPage](code%20source/front/src/pages/TemplatesPage.tsx) - Templates

**SOLID appliqué**:
- ✅ Single Responsibility: UNE page = UNE fonctionnalité
- ✅ Composition over Inheritance: Composants réutilisables
- ✅ Dependency Injection: Props passées de parent → enfant

---

#### 🟡 CONTROLLER: Services API + Hooks (Logique)

**Localisation**: `code source/front/src/services/` et `code source/front/src/utils/`

```
📁 services/
   └─ api.ts
      ├─ handleResponse(res)    ← Gestion erreurs
      ├─ getAuthHeaders()       ← Ajout tokens
      └─ fetch() wrapper

📁 utils/
   ├─ apiBase.ts              ← Configuration URL
   ├─ applyTheme.ts           ← Logique thème
   └─ ...
```

**Où trouver**:
- [API Service](code%20source/front/src/services/api.ts#L1-L50)
- [API Base](code%20source/front/src/utils/apiBase.ts)

**SOLID appliqué**:
- ✅ Single Responsibility: Couche API isolée
- ✅ Dependency Inversion: Services abstraits

**Design Pattern**:
- 🎯 **Adapter Pattern**: Wrapper fetch()
- 🎯 **Error Handler Pattern**: Centralisé
- 🎯 **Interceptor Pattern**: Ajoute tokens automatiquement

---

#### 📊 Flux Complet Côté Frontend

```
USER ACTION (Clic bouton)
    ↓
PAGE COMPONENT (MyShopPage.tsx)
    ├─ Gère state local: (pName, pPrice, pStock, ...)
    ├─ event handler: handleAddProduct()
    └─ appelle API
         ↓
SERVICE (services/api.ts)
    ├─ getAuthHeaders()      ← Récupère token
    ├─ fetch(endpoint)       ← Appel HTTP
    ├─ handleResponse()      ← Vérifie réponse
    └─ retourne data
         ↓
PAGE COMPONENT
    ├─ Mise à jour state
    ├─ toast.success()       ← Notification
    ├─ fetchProducts()       ← Recharge liste
    └─ setState(products)
         ↓
UI COMPONENT (Product List)
    └─ .map(product => <ProductCard />)
         ↓
SCREEN
```

---

## ✅ PRINCIPES SOLID

### 🔴 S - Single Responsibility Principle

**Chaque classe/fonction a UNE SEULE responsabilité**

**Exemples dans le projet**:

| Classe | Responsabilité |
|--------|---|
| `ProductRepository` | Accès données Product |
| `ProductService` | Logique métier Product |
| `ProductSerializer` | Sérialisation Product |
| `create_product_api` | Gestion requête HTTP |
| `MyShopPage` | Affichage table de bord |
| `AuthContext` | Gestion authentification |

**Violation ❌**:
```python
# ❌ MAUVAIS: Trop de responsabilités
def create_product(request):
    user = request.user
    if not user.shop:
        return error
    
    # Validation
    if not request.data['name']:
        return error
    
    # Création
    product = Product.objects.create(...)
    
    # Email
    send_email()
    
    # Log
    log()
    
    return response
```

**Conforme ✅**:
```python
# ✅ BON: Responsabilités séparées

# Controller: Gère HTTP
def create_product_api(request):
    service = ProductService()
    product = service.create_product_for_shop(...)
    return Response(ProductSerializer(product).data)

# Service: Logique métier
class ProductService:
    def create_product_for_shop(self, ...):
        validate_price()
        product = repository.create()
        log_operation()
        return product

# Repository: Accès données
class ProductRepository:
    def create(self, ...):
        return Product.objects.create(...)
```

---

### 🟠 O - Open/Closed Principle

**Ouvert à l'extension, fermé à la modification**

**Exemples dans le projet**:

#### Backend - BaseService Pattern:
```python
# ✅ OUVERT: Facile d'étendre
class BaseService(Generic[T]):
    def __init__(self, repository):
        self.repository = repository
    
    def create(self, **kwargs):
        entity = self.repository.create(**kwargs)
        self.log_operation('created', ...)
        return entity

# Spécialisation sans modification de base
class ProductService(BaseService[Product]):
    def create_product_for_shop(self, shop, ...):
        # Logique spécifique produit
        validate_price()
        # Appelle méthode de base
        return super().create(...)
```

#### Frontend - Composants réutilisables:
```tsx
// ✅ OUVERT: Composant flexible
interface ButtonProps {
    onClick?: () => void;
    variant?: 'primary' | 'secondary';
    children: React.ReactNode;
}

export function Button({ onClick, variant = 'primary', children }: ButtonProps) {
    return <button className={`btn-${variant}`}>{children}</button>;
}

// Utilisation sans modifier Button
<Button variant="primary">Créer</Button>
<Button variant="secondary">Annuler</Button>
```

---

### 🟡 L - Liskov Substitution Principle

**Sous-classes peuvent remplacer leurs parents**

**Exemples dans le projet**:

```python
# ✅ CONFORME: UserRepository peut remplacer BaseRepository
class BaseRepository(Generic[T]):
    def get_by_id(self, id) -> Optional[T]:
        return self.model.objects.get(id=id)

class UserRepository(BaseRepository[User]):
    # Hérite toutes les méthodes de base
    # Peut être utilisé partout où BaseRepository[User] est attendu
    pass

# Utilisation polymorphe
def get_entity(repo: BaseRepository[User], id: int) -> User:
    return repo.get_by_id(id)  # Fonctionne avec UserRepository ✓
```

---

### 🟢 I - Interface Segregation Principle

**Clients ne doivent pas dépendre d'interfaces qu'ils n'utilisent pas**

**Exemples dans le projet**:

```python
# ✅ CONFORME: Interfaces séparées

class ProductRepository:
    def get_by_id(self, id): ...          # Pour lecture
    def search_products(self, query): ...  # Pour recherche
    def update_stock(self, product, qty): # Pour stock

class UserRepository:
    def get_by_id(self, id): ...          # Pour lecture
    def get_by_email(self, email): ...    # Spécifique user

# Service utilise UNIQUEMENT ce dont il a besoin
class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        # N'utilise que: get_by_id, update_stock
        # Ne voit pas: get_by_email (du UserRepository)
```

---

### 🔵 D - Dependency Inversion Principle

**Dépendre d'abstractions, pas de concrétions**

**Exemples dans le projet**:

```python
# ✅ CONFORME: Service dépend de Repository (abstraction)

# Vue dépend de Service (abstraction)
@api_view(['POST'])
def create_product_api(request):
    service = ProductService()  # Abstraction
    product = service.create_product_for_shop(...)
    return Response(ProductSerializer(product).data)

# Service dépend de Repository (abstraction)
class ProductService:
    def __init__(self):
        self.repository = ProductRepository()  # Abstraction
    
    def create_product(self, ...):
        product = self.repository.create(...)

# ❌ ÉVITÉ: Dépendance directe au modèle
# product = Product.objects.create(...)  ← ❌ Mauvais
```

---

## 🎯 DESIGN PATTERNS UTILISÉS

### 1. Repository Pattern

**Où**: Backend - `repositories/`  
**Quoi**: Abstrait l'accès aux données  
**Pourquoi**: Changeable (SQL → NoSQL) sans impacter le service

```python
# Interface
class ProductRepository(BaseRepository[Product]):
    def get_by_slug(self, slug): ...
    def search_products(self, query): ...

# Utilisation
class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
    
    def find_product(self, slug):
        return self.repository.get_by_slug(slug)
```

**Localisation**:
- [ProductRepository](code%20source/shopina-env/backend/shop/repositories/product_repository.py)
- [BaseRepository](code%20source/shopina-env/backend/core/repositories/base.py)

---

### 2. Service Locator Pattern

**Où**: Backend - `services/`  
**Quoi**: Centralise logique métier  
**Pourquoi**: Réutilisable, testable, découplée

```python
class ProductService(BaseService[Product]):
    def create_product_for_shop(self, shop, name, price, ...):
        # Logique métier centralisée
        validate_price(price)
        validate_stock(stock)
        product = self.repository.create(...)
        self.log_operation('product_created', ...)
        return product
```

**Localisation**:
- [ProductService](code%20source/shopina-env/backend/shop/services/product_service.py)
- [BaseService](code%20source/shopina-env/backend/core/services/base.py)

---

### 3. DTO (Data Transfer Object) Pattern

**Où**: Backend - `serializers.py`  
**Quoi**: Transforme Model ↔ JSON  
**Pourquoi**: Valide et transforme données entre couches

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'created_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be > 0")
        return value
```

**Localisation**:
- [ProductSerializer](code%20source/shopina-env/backend/shop/serializers.py)
- [UserSerializer](code%20source/shopina-env/backend/users/serializers.py)

---

### 4. Dependency Injection Pattern

**Où**: Partout (Backend + Frontend)  
**Quoi**: Injecte dépendances au lieu de les créer  
**Pourquoi**: Testable, découplée, réutilisable

```python
# Backend
class ProductService:
    def __init__(self, repository=None):
        self.repository = repository or ProductRepository()

# Frontend (via Props)
function MyShopPage() {
    const { user } = useAuth();  // Injection via hook
    const { shop } = useShop();  // Injection via hook
    // Utilisation
}
```

---

### 5. Factory Pattern

**Où**: Backend - Category management  
**Quoi**: Crée objets sans spécifier classe exacte  
**Pourquoi**: Encapsule logique de création

```python
# Dans ProductService.create_product_for_shop()
category = None
if category_name:
    category, _ = Category.objects.get_or_create(name=category_name)
    # Factory pattern: créer OU récupérer

product = Product.objects.create(
    name=name,
    category=category,  # Utilise ce qui a été créé/récupéré
    ...
)
```

**Localisation**:
- [create_product_for_shop](code%20source/shopina-env/backend/shop/services/product_service.py#L50-L100)

---

### 6. Observer Pattern

**Où**: Frontend - Context API  
**Quoi**: Notifie composants quand état change  
**Pourquoi**: Synchronisation automatique

```tsx
// Provider
export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [tokens, setTokens] = useState(null);
    
    // Tous les composants "observent" ces changements
    return (
        <AuthContext.Provider value={{ user, tokens }}>
            {children}
        </AuthContext.Provider>
    );
}

// Observateur
function LoginPage() {
    const { user } = useAuth();  // S'abonne aux changements
    // Component re-render quand user change
}
```

**Localisation**:
- [AuthContext](code%20source/front/src/context/AuthContext.tsx)
- [ThemeLanguageContext](code%20source/front/src/context/ThemeLanguageContext.tsx)

---

### 7. Adapter Pattern

**Où**: Frontend - `services/api.ts`  
**Quoi**: Adapte fetch() pour projet spécifique  
**Pourquoi**: Centralize auth, error handling

```typescript
export async function handleResponse(res: Response) {
    if (!res.ok) {
        if (res.status === 401) {
            // Gère token expiré
        }
        const text = await res.text();
        throw new Error(text);
    }
    return res.json();
}

// Utilisation
const data = await fetch(url).then(handleResponse);
```

**Localisation**:
- [API Service](code%20source/front/src/services/api.ts)

---

### 8. Decorator Pattern

**Où**: Backend - `@api_view`, `@permission_classes`  
**Quoi**: Ajoute fonctionnalité sans modifier fonction  
**Pourquoi**: Clean, réutilisable, composable

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_api(request):
    # Les décorateurs ajoutent validation, auth
    pass
```

**Localisation**:
- [create_product_api](code%20source/shopina-env/backend/shop/views.py#L40-L85)
- [update_product_api](code%20source/shopina-env/backend/shop/views.py#L104-L150)
- [delete_product_api](code%20source/shopina-env/backend/shop/views.py#L152-L185)

---

### 9. Template Method Pattern

**Où**: Backend - `BaseService`, `BaseRepository`  
**Quoi**: Définit structure, sous-classes implémentent détails  
**Pourquoi**: Code réutilisable, cohérence

```python
class BaseService(Generic[T]):
    def create(self, **kwargs):
        entity = self.repository.create(**kwargs)
        self.log_operation('created', {'entity_id': entity.id})
        return entity

# Sous-classe utilise template de base
class ProductService(BaseService[Product]):
    # Hérite create() qui log automatiquement
```

**Localisation**:
- [BaseService](code%20source/shopina-env/backend/core/services/base.py)
- [BaseRepository](code%20source/shopina-env/backend/core/repositories/base.py)

---

### 10. Chain of Responsibility Pattern

**Où**: Backend - API request flow  
**Quoi**: Passe requête à travers chaîne de handlers  
**Pourquoi**: Chaque étape a responsabilité unique

```
REQUEST
  ↓ Authentification
  ↓ Permission check
  ↓ Validation
  ↓ Business logic
  ↓ Response
```

**Localisation**:
- [create_product_api](code%20source/shopina-env/backend/shop/views.py#L40-L85)

---

## 📂 STRUCTURE DE FICHIERS COMPLÈTE

### Backend Structure

```
code source/shopina-env/backend/
├── core/                           # Infrastructure commune
│   ├── services/
│   │   └── base.py                 # BaseService (Template Method)
│   ├── repositories/
│   │   └── base.py                 # BaseRepository (Repository Pattern)
│   ├── permissions/
│   │   └── custom_permissions.py
│   └── utils/
│       ├── exceptions.py           # CustomValidationError, etc
│       └── validators.py           # validate_price, validate_quantity
│
├── shop/                           # Module produits
│   ├── models.py                   # Model: Product, Category
│   ├── serializers.py              # DTO: ProductSerializer
│   ├── repositories/
│   │   └── product_repository.py   # Repository: accès données
│   ├── services/
│   │   └── product_service.py      # Service: logique métier
│   ├── views.py                    # Controller: HTTP endpoints
│   └── urls.py                     # Routes
│
├── users/                          # Module utilisateurs
│   ├── models.py                   # Model: User, Profile
│   ├── serializers.py              # DTO: UserSerializer
│   ├── repositories/
│   │   └── user_repository.py      # Repository
│   ├── services/
│   │   └── user_service.py         # Service
│   ├── views.py                    # Controller
│   └── urls.py
│
├── shops/                          # Module boutiques
│   ├── models.py                   # Model: Shop, ShopTheme
│   ├── serializers.py              # DTO
│   ├── views.py                    # Controller
│   └── urls.py
│
├── orders/                         # Module commandes
│   ├── models.py                   # Model: Order, OrderItem
│   ├── services/
│   │   └── order_service.py        # Service
│   ├── views.py                    # Controller
│   └── urls.py
│
└── shopina/                        # Config Django
    ├── settings.py                 # Configuration
    ├── urls.py                     # URL routing principal
    └── wsgi.py
```

### Frontend Structure

```
code source/front/src/
├── context/                        # Model + State (Context API)
│   ├── AuthContext.tsx             # Observer Pattern
│   └── ThemeLanguageContext.tsx
│
├── pages/                          # View: Pages complètes
│   ├── LoginPage.tsx               # Authentification
│   ├── MyShopPage.tsx              # Dashboard boutique
│   ├── ShopPage.tsx                # Affichage boutique
│   ├── TemplatesPage.tsx           # Sélection templates
│   ├── CheckoutPage.tsx            # Paiement
│   └── ...
│
├── components/                     # View: Composants réutilisables
│   ├── Header.tsx                  # Navigation
│   ├── Footer.tsx
│   ├── DashboardHeader.tsx
│   ├── DashboardSidebar.tsx
│   ├── CTA.tsx                     # Call-to-action
│   ├── ui/                         # Composants génériques
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── ...
│   └── ...
│
├── services/                       # Controller: API abstraction
│   └── api.ts                      # Adapter Pattern
│
├── utils/                          # Helpers
│   ├── apiBase.ts                  # Configuration API
│   ├── applyTheme.ts               # Logique thème
│   └── ...
│
├── hooks/                          # Custom React Hooks
│   ├── useAuth.ts                  # Hook authentification
│   └── ...
│
└── App.tsx                         # Routing principal
```

---

## 🔗 FLUX COMPLET EXEMPLE: Ajouter un Produit

### 1. Frontend (myShopPage.tsx)
```tsx
// 1. Utilisateur clique sur "Ajouter un produit"
// 2. Formulaire récupère: pName, pPrice, pStock, pCategory

async function handleAddProduct(e) {
    // Validation frontend
    if (!pName || !pPrice) {
        toast.error("Nom et prix requis");
        return;
    }
    
    // Appel API via service
    const formData = new FormData();
    formData.append("name", pName);
    formData.append("price", pPrice);
    formData.append("stock", pStock || "1");
    formData.append("category", pCategory);
    if (pImage) formData.append("image", pImage);
    
    const res = await fetch(`${API_BASE}/api/shop/create/`, {
        method: "POST",
        body: formData,
        headers: getAuthHeaders(),
    });
    
    if (!res.ok) {
        toast.error("Erreur lors de l'ajout");
        return;
    }
    
    const data = await res.json();
    toast.success("Produit ajouté!");
    setProducts([...products, data]);
}
```

### 2. Backend (views.py)
```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_api(request):
    # Controller: Gère la requête HTTP
    
    try:
        shop = request.user.shop  # 1️⃣ Récupère boutique
    except AttributeError:
        return Response(
            {'detail': "Vous devez créer une boutique..."},
            status=400
        )
    
    # 2️⃣ Récupère données
    name = request.data.get('name')
    price = request.data.get('price')
    category_name = request.data.get('category')
    stock = request.data.get('stock', 1)
    image = request.FILES.get('image')
    
    # 3️⃣ Validation basique
    if not name or not price:
        return Response(
            {'detail': 'name and price required'},
            status=400
        )
    
    # 4️⃣ Utilise Service pour logique métier
    try:
        product_service = ProductService()
        product = product_service.create_product_for_shop(
            shop=shop,
            name=name,
            price=price,
            category_name=category_name,
            stock=stock,
            image=image
        )
        
        # 5️⃣ Sérialise réponse
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=201)
        
    except CustomValidationError as e:
        return Response({'detail': str(e)}, status=400)
    except Exception as e:
        return Response({'detail': str(e)}, status=500)
```

### 3. Backend (services/product_service.py)
```python
class ProductService(BaseService[Product]):
    def create_product_for_shop(self, shop, name, price, 
                               category_name=None, stock=1, image=None):
        # Service: Logique métier
        
        # 1️⃣ Validation métier
        is_valid, error_msg = validate_price(float(price))
        if not is_valid:
            raise CustomValidationError(error_msg)
        
        stock_int = int(stock)
        if stock_int < 0:
            raise CustomValidationError("Stock cannot be negative")
        
        # 2️⃣ Logique métier: créer/récupérer catégorie
        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(
                name=category_name
            )
        
        # 3️⃣ Appel Repository
        product = self.repository.create(
            name=name,
            price=price,
            category=category,
            stock=stock_int,
            shop=shop,
            image=image
        )
        
        # 4️⃣ Audit
        self.log_operation('product_created_for_shop', {
            'product_id': product.id,
            'shop_id': shop.id
        })
        
        return product
```

### 4. Backend (repositories/product_repository.py)
```python
class ProductRepository(BaseRepository[Product]):
    def create(self, **kwargs):
        # Repository: Accès données SEULEMENT
        return Product.objects.create(**kwargs)
```

### 5. Backend (models.py)
```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True)
    
    def save(self, *args, **kwargs):
        # Model: Logique de persistence
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
```

### 6. Backend (serializers.py)
```python
class ProductSerializer(serializers.ModelSerializer):
    # Serializer: DTO + Validation
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'image', 'created_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be positive")
        return value
```

### 7. Response → Frontend
```json
{
    "id": 42,
    "name": "T-Shirt",
    "price": "29.99",
    "stock": 10,
    "image": "/media/products/tshirt.jpg",
    "created_at": "2026-02-03T23:00:00Z"
}
```

### 8. Frontend Update
```tsx
// Response reçue
setProducts([...products, data]);
toast.success("Produit ajouté!");

// UI re-render avec nouveau produit
```

---

## 📊 MATRICE D'ARCHITECTURE

| Aspect | Backend | Frontend |
|--------|---------|----------|
| **MVC** | Views + Services + Repos | Pages + Hooks + Context |
| **SOLID** | ✅ Appliqué | ✅ Appliqué |
| **Main Pattern** | Repository + Service | Context API + Hooks |
| **State** | DB | localStorage + Context |
| **Validation** | Services + Serializers | Client-side + Backend |
| **Error Handling** | Custom Exceptions | Toast + Try-Catch |
| **Auth** | JWT Tokens | localStorage + Context |

---

## 🎓 RÉSUMÉ

### ✅ MVC Appliqué
- **Backend**: Model (Django ORM) → Repository → Service → Serializer → View
- **Frontend**: Model (Context) → Component → Service → Page

### ✅ SOLID Appliqué
- **S**: Chaque classe une responsabilité
- **O**: Extensible sans modification (Inheritance)
- **L**: Polymorphisme fonctionne
- **I**: Interfaces séparées
- **D**: Dépend d'abstractions

### ✅ Design Patterns Utilisés
1. **Repository** - Abstrait données
2. **Service Locator** - Logique métier centralisée
3. **DTO** - Validation + transformation
4. **Dependency Injection** - Couplage faible
5. **Factory** - Création d'objets
6. **Observer** - State management
7. **Adapter** - Wrap fetch()
8. **Decorator** - Adds functionality
9. **Template Method** - Base classes
10. **Chain of Responsibility** - Request flow

---

**Document créé**: 2026-02-03  
**Version**: 1.0  
**Auteur**: Architecture Team
