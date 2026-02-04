# 🎯 INDEX DE LOCALISATION: MVC + SOLID + DESIGN PATTERNS

## 📍 OÙ TROUVER QUOI?

---

## 🏗️ ARCHITECTURE MVC

### BACKEND

#### **MODEL LAYER** (Django ORM)
| Composant | Chemin | Description |
|-----------|--------|-------------|
| **Product Model** | [shop/models.py](code%20source/shopina-env/backend/shop/models.py#L12-L42) | Modèle produit avec slug unique |
| **Shop Model** | [shops/models.py](code%20source/shopina-env/backend/shops/models.py#L9-L95) | Modèle boutique (OneToOne avec User) |
| **User Model** | [users/models.py](code%20source/shopina-env/backend/users/models.py#L8-L50) | Utilisateur avec rôles |
| **Category Model** | [shop/models.py](code%20source/shopina-env/backend/shop/models.py#L1-L10) | Catégorie produits |
| **Order Model** | [orders/models.py](code%20source/shopina-env/backend/orders/models.py) | Gestion commandes |

---

#### **REPOSITORY LAYER** (Data Access)
| Pattern | Chemin | Responsabilité |
|---------|--------|---|
| **BaseRepository** | [core/repositories/base.py](code%20source/shopina-env/backend/core/repositories/base.py) | Template générique `BaseRepository[T]` |
| **ProductRepository** | [shop/repositories/product_repository.py](code%20source/shopina-env/backend/shop/repositories/product_repository.py#L1-L50) | Requêtes Product: `get_by_slug()`, `search_products()` |
| **UserRepository** | [users/repositories/user_repository.py](code%20source/shopina-env/backend/users/repositories/user_repository.py) | Requêtes User: `get_by_email()`, `get_by_username()` |
| **CategoryRepository** | [shop/repositories/product_repository.py](code%20source/shopina-env/backend/shop/repositories/product_repository.py#L100-L120) | Requêtes Category |

**Métiers clés du Repository**:
- `get_by_id(id)` - Récupère par ID
- `get_active_products()` - Filtre produits actifs
- `search_products(query)` - Recherche
- `update_stock(product, quantity)` - Mise à jour stock

---

#### **SERVICE LAYER** (Business Logic)
| Pattern | Chemin | Logique Métier |
|---------|--------|---|
| **BaseService** | [core/services/base.py](code%20source/shopina-env/backend/core/services/base.py) | Template générique `BaseService[T]` |
| **ProductService** | [shop/services/product_service.py](code%20source/shopina-env/backend/shop/services/product_service.py#L1-L100) | `create_product_for_shop()`, `update_product()`, `decrease_stock()` |
| **UserService** | [users/services/user_service.py](code%20source/shopina-env/backend/users/services/user_service.py) | `create_user()`, `change_password()` |
| **OrderService** | [orders/services/order_service.py](code%20source/shopina-env/backend/orders/services/order_service.py) | `create_order()`, `update_status()` |

**Validations dans Service**:
- `validate_price(price)` - Prix > 0
- `validate_stock(stock)` - Stock ≥ 0
- Logique métier complexe

---

#### **SERIALIZER LAYER** (DTO)
| DTO | Chemin | Validation |
|-----|--------|------------|
| **ProductSerializer** | [shop/serializers.py](code%20source/shopina-env/backend/shop/serializers.py#L1-L30) | Valide `price > 0`, sérialize Product |
| **UserSerializer** | [users/serializers.py](code%20source/shopina-env/backend/users/serializers.py#L10-L40) | Valide email unique, password |
| **OrderSerializer** | [orders/serializers.py](code%20source/shopina-env/backend/orders/serializers.py) | Sérialize Order avec items |

---

#### **VIEW/CONTROLLER LAYER** (HTTP)
| Endpoint | Chemin | Responsabilité |
|----------|--------|---|
| **POST /api/shop/create/** (Ajouter produit) | [shop/views.py](code%20source/shopina-env/backend/shop/views.py#L40-L85) | `create_product_api()` |
| **PUT/PATCH /api/shop/product/{id}/** (Modifier produit) | [shop/views.py](code%20source/shopina-env/backend/shop/views.py#L104-L150) | `update_product_api()` |
| **DELETE /api/shop/product/{id}/** (Supprimer produit) | [shop/views.py](code%20source/shopina-env/backend/shop/views.py#L152-L185) | `delete_product_api()` |
| **POST /api/users/token/** (Login) | [users/views.py](code%20source/shopina-env/backend/users/views.py) | JWT authentication |
| **POST /api/shop/api/create/** (Créer boutique) | [shops/views.py](code%20source/shopina-env/backend/shops/views.py) | `create_shop_api()` |

---

### FRONTEND

#### **MODEL LAYER** (State Management)
| Context | Chemin | État Géré |
|---------|--------|-----------|
| **AuthContext** | [src/context/AuthContext.tsx](code%20source/front/src/context/AuthContext.tsx#L1-L50) | `user`, `tokens`, `login()`, `logout()`, `refreshProfile()` |
| **ThemeLanguageContext** | [src/context/ThemeLanguageContext.tsx](code%20source/front/src/context/ThemeLanguageContext.tsx) | `theme`, `language`, `toggleTheme()` |

---

#### **VIEW LAYER** (Composants)
| Page/Composant | Chemin | Affichage |
|---|---|---|
| **LoginPage** | [src/pages/LoginPage.tsx](code%20source/front/src/pages/LoginPage.tsx) | Formulaire connexion |
| **MyShopPage** | [src/pages/MyShopPage.tsx](code%20source/front/src/pages/MyShopPage.tsx#L1-L50) | Dashboard boutique - Gestion produits |
| **ShopPage** | [src/pages/ShopPage.tsx](code%20source/front/src/pages/ShopPage.tsx) | Affichage public boutique |
| **TemplatesPage** | [src/pages/TemplatesPage.tsx](code%20source/front/src/pages/TemplatesPage.tsx) | Sélection templates |
| **Header** | [src/components/Header.tsx](code%20source/front/src/components/Header.tsx) | Navigation top |
| **Footer** | [src/components/Footer.tsx](code%20source/front/src/components/Footer.tsx) | Footer |

---

#### **CONTROLLER LAYER** (API Service)
| Couche | Chemin | Fonction |
|-------|--------|----------|
| **API Service** | [src/services/api.ts](code%20source/front/src/services/api.ts#L1-L50) | `handleResponse()`, `getAuthHeaders()`, fetch wrapper |
| **API Base** | [src/utils/apiBase.ts](code%20source/front/src/utils/apiBase.ts) | Configuration URL API: `normalize()`, `API_BASE` |
| **Theme Utils** | [src/utils/applyTheme.ts](code%20source/front/src/utils/applyTheme.ts) | `applyThemeStyles()` - Applique CSS variables |

---

## ✅ PRINCIPES SOLID

### 🔴 **Single Responsibility**

| Classe/Fonction | Responsabilité Unique | Chemin |
|---|---|---|
| `ProductRepository` | Requêtes Product SEULEMENT | [product_repository.py](code%20source/shopina-env/backend/shop/repositories/product_repository.py) |
| `ProductService` | Logique métier Product SEULEMENT | [product_service.py](code%20source/shopina-env/backend/shop/services/product_service.py) |
| `ProductSerializer` | Sérialisation Product SEULEMENT | [shop/serializers.py](code%20source/shopina-env/backend/shop/serializers.py) |
| `create_product_api()` | HTTP handling SEULEMENT | [shop/views.py](code%20source/shopina-env/backend/shop/views.py#L40-L85) |
| `MyShopPage` | Dashboard boutique SEULEMENT | [MyShopPage.tsx](code%20source/front/src/pages/MyShopPage.tsx) |

---

### 🟠 **Open/Closed Principle**

| Pattern | Localisation | Ouvert À |
|---------|---|---|
| **BaseService[T]** | [core/services/base.py](code%20source/shopina-env/backend/core/services/base.py) | Héritage (ProductService, UserService) |
| **BaseRepository[T]** | [core/repositories/base.py](code%20source/shopina-env/backend/core/repositories/base.py) | Héritage (ProductRepository, UserRepository) |
| **Composants React** | [src/components/](code%20source/front/src/components/) | Props (variant, size, etc.) |

**Exemple**: BaseService peut être étendu par ProductService sans modifier le code de base.

---

### 🟡 **Liskov Substitution**

| Situation | Classe Parent | Sous-classe | Chemin |
|---|---|---|---|
| Repository | `BaseRepository[T]` | `ProductRepository` | [repositories/](code%20source/shopina-env/backend/shop/repositories/) |
| Service | `BaseService[T]` | `ProductService` | [services/](code%20source/shopina-env/backend/shop/services/) |
| Django View | `generics.CreateAPIView` | `RegisterView` | [users/views.py](code%20source/shopina-env/backend/users/views.py) |

---

### 🟢 **Interface Segregation**

| Interface | Utilisateurs | Chemin |
|---|---|---|
| `ProductRepository` | ProductService + Tests | [product_repository.py](code%20source/shopina-env/backend/shop/repositories/product_repository.py) |
| `AuthContext` | Pages + Composants | [AuthContext.tsx](code%20source/front/src/context/AuthContext.tsx) |
| `UserService` | Views + Admin | [user_service.py](code%20source/shopina-env/backend/users/services/user_service.py) |

---

### 🔵 **Dependency Inversion**

| Dépendance | Abstraction | Concrétisation | Chemin |
|---|---|---|---|
| View → Service | `ProductService()` | Crée ProductRepository() | [views.py](code%20source/shopina-env/backend/shop/views.py#L40-L85) |
| Service → Repository | `self.repository` | ProductRepository instance | [product_service.py](code%20source/shopina-env/backend/shop/services/product_service.py#L20-L30) |
| Page → Context | `useAuth()` | AuthContext.Provider | [AuthContext.tsx](code%20source/front/src/context/AuthContext.tsx) |

---

## 🎯 DESIGN PATTERNS

### 1. 📦 **Repository Pattern**
```
Abstrait l'accès aux données
↓
Localisation: [shop/repositories/](code%20source/shopina-env/backend/shop/repositories/)
↓
Classe: ProductRepository
↓
Méthodes: get_by_slug(), search_products(), update_stock()
```

**Où**: Backend - tout app  
**Bénéfice**: Changeable (SQL → NoSQL)  
**Fichier Clé**: [product_repository.py](code%20source/shopina-env/backend/shop/repositories/product_repository.py#L1-L50)

---

### 2. 🏢 **Service Locator Pattern**
```
Centralise logique métier
↓
Localisation: [shop/services/](code%20source/shopina-env/backend/shop/services/)
↓
Classe: ProductService
↓
Méthodes: create_product_for_shop(), update_product(), delete_product()
```

**Où**: Backend - tout app  
**Bénéfice**: Réutilisable, testable  
**Fichier Clé**: [product_service.py](code%20source/shopina-env/backend/shop/services/product_service.py#L30-L80)

---

### 3. 📊 **DTO Pattern** (Data Transfer Object)
```
Valide + transforme données
↓
Localisation: [shop/serializers.py](code%20source/shopina-env/backend/shop/serializers.py)
↓
Classe: ProductSerializer
↓
Méthodes: validate_price(), to_representation(), to_internal_value()
```

**Où**: Backend - sérializers.py  
**Bénéfice**: Validation + sécurité  
**Fichier Clé**: [shop/serializers.py](code%20source/shopina-env/backend/shop/serializers.py#L1-L30)

---

### 4. 💉 **Dependency Injection Pattern**
```
Injecte dépendances
↓
Backend: Constructor injection
↓
Frontend: Props + React Hooks
```

**Où**: Partout  
**Bénéfice**: Découplé, testable  
**Exemples**:
- [Backend](code%20source/shopina-env/backend/shop/services/product_service.py#L25-L30)
- [Frontend](code%20source/front/src/context/AuthContext.tsx#L150-L200)

---

### 5. 🏭 **Factory Pattern**
```
Crée objets sans spécifier classe exacte
↓
Localisation: [product_service.py](code%20source/shopina-env/backend/shop/services/product_service.py#L50-L80)
↓
get_or_create(Category)
```

**Où**: Backend - Services  
**Bénéfice**: Encapsule logique création  
**Fichier Clé**: [product_service.py](code%20source/shopina-env/backend/shop/services/product_service.py#L60-L65)

---

### 6. 👁️ **Observer Pattern**
```
Notifie quand état change
↓
Localisation: [AuthContext.tsx](code%20source/front/src/context/AuthContext.tsx)
↓
Context.Provider observé par useAuth()
```

**Où**: Frontend - Context API  
**Bénéfice**: Synchronisation auto  
**Fichier Clé**: [AuthContext.tsx](code%20source/front/src/context/AuthContext.tsx#L1-L50)

---

### 7. 🔌 **Adapter Pattern**
```
Adapte fetch() à projet
↓
Localisation: [services/api.ts](code%20source/front/src/services/api.ts)
↓
Fonction: handleResponse()
```

**Où**: Frontend - api.ts  
**Bénéfice**: Centralize erreurs, auth  
**Fichier Clé**: [services/api.ts](code%20source/front/src/services/api.ts#L1-L30)

---

### 8. 🎨 **Decorator Pattern**
```
Ajoute fonctionnalité sans modifier
↓
Localisation: [shop/views.py](code%20source/shopina-env/backend/shop/views.py#L40)
↓
@api_view(['POST'])
@permission_classes([IsAuthenticated])
```

**Où**: Backend - Views  
**Bénéfice**: Clean, composable  
**Fichiers Clés**:
- [create_product_api](code%20source/shopina-env/backend/shop/views.py#L38-L45)
- [update_product_api](code%20source/shopina-env/backend/shop/views.py#L104-L111)

---

### 9. 📋 **Template Method Pattern**
```
Définit structure, sous-classes détails
↓
Localisation: [core/services/base.py](code%20source/shopina-env/backend/core/services/base.py)
↓
BaseService.create() → log automatique
```

**Où**: Backend - Base classes  
**Bénéfice**: Code réutilisable  
**Fichier Clé**: [core/services/base.py](code%20source/shopina-env/backend/core/services/base.py#L1-L50)

---

### 10. ⛓️ **Chain of Responsibility Pattern**
```
Requête passe via chaîne handlers
↓
Auth → Permission → Validation → Logic
↓
Localisation: [shop/views.py](code%20source/shopina-env/backend/shop/views.py#L40-L85)
```

**Où**: Backend - Request flow  
**Bénéfice**: Séparation responsabilités  
**Fichier Clé**: [create_product_api](code%20source/shopina-env/backend/shop/views.py#L40-L85)

---

## 📁 FICHIERS PAR TOPIC

### **Authentification & Autorisation**
- [AuthContext.tsx](code%20source/front/src/context/AuthContext.tsx) - Frontend state
- [users/models.py](code%20source/shopina-env/backend/users/models.py) - User model
- [users/views.py](code%20source/shopina-env/backend/users/views.py) - Auth endpoints
- [users/services/user_service.py](code%20source/shopina-env/backend/users/services/user_service.py) - Business logic

### **Gestion Produits**
- [shop/models.py](code%20source/shopina-env/backend/shop/models.py) - Product model
- [shop/repositories/product_repository.py](code%20source/shopina-env/backend/shop/repositories/product_repository.py) - Data access
- [shop/services/product_service.py](code%20source/shopina-env/backend/shop/services/product_service.py) - Business logic
- [shop/serializers.py](code%20source/shopina-env/backend/shop/serializers.py) - DTO
- [shop/views.py](code%20source/shopina-env/backend/shop/views.py) - API endpoints
- [MyShopPage.tsx](code%20source/front/src/pages/MyShopPage.tsx) - Dashboard produits

### **Gestion Boutiques**
- [shops/models.py](code%20source/shopina-env/backend/shops/models.py) - Shop model
- [ShopPage.tsx](code%20source/front/src/pages/ShopPage.tsx) - Affichage boutique
- [TemplatesPage.tsx](code%20source/front/src/pages/TemplatesPage.tsx) - Sélection templates

### **Infrastructure Commune**
- [core/services/base.py](code%20source/shopina-env/backend/core/services/base.py) - BaseService template
- [core/repositories/base.py](code%20source/shopina-env/backend/core/repositories/base.py) - BaseRepository template
- [core/utils/exceptions.py](code%20source/shopina-env/backend/core/utils/exceptions.py) - Custom exceptions
- [core/utils/validators.py](code%20source/shopina-env/backend/core/utils/validators.py) - Validation utilities

---

## 🔗 FLUX D'EXÉCUTION COMPLET

### Ajouter un Produit (Exemple)

**1. Frontend Click**
```
MyShopPage.tsx (L50-100)
    ↓ handleAddProduct()
    ↓ fetch() + FormData
```

**2. Backend Route**
```
urls.py → POST /api/shop/create/ → create_product_api()
```

**3. View/Controller**
```
shop/views.py (L40-85)
    ├─ Check auth ✓
    ├─ Validate basic ✓
    └─ Call ProductService.create_product_for_shop()
```

**4. Service**
```
shop/services/product_service.py (L50-100)
    ├─ Validate price ✓
    ├─ Validate stock ✓
    ├─ Get/Create category
    └─ Call ProductRepository.create()
```

**5. Repository**
```
shop/repositories/product_service.py
    └─ Product.objects.create()
```

**6. Model**
```
shop/models.py
    └─ save() → Generate slug
```

**7. Serializer**
```
shop/serializers.py
    └─ ProductSerializer(product).data
```

**8. Response**
```
Response(data, status=201) → Frontend
```

**9. Frontend Update**
```
MyShopPage.tsx
    ├─ setProducts([...products, data])
    ├─ toast.success()
    └─ UI re-render
```

---

## 📚 DOCUMENTATION DE RÉFÉRENCE

| Document | Chemin | Contenu |
|---|---|---|
| Architecture Complète | [ARCHITECTURE_COMPLETE_MVC_SOLID_PATTERNS.md](ARCHITECTURE_COMPLETE_MVC_SOLID_PATTERNS.md) | MVC + SOLID + 10 Patterns détaillés |
| Index Localisation | [ARCHITECTURE_INDEX_LOCALISATION.md](ARCHITECTURE_INDEX_LOCALISATION.md) | Ce fichier - Où trouver quoi |
| Backend README | [code source/shopina-env/backend/README.md](code%20source/shopina-env/backend/README.md) | Architecture backend, setup, API docs |
| My Store Architecture | [ARCHITECTURE_MY_STORE.md](ARCHITECTURE_MY_STORE.md) | Architecture composants dashboard |

---

**Créé**: 2026-02-03  
**Dernière mise à jour**: 2026-02-03  
**Auteur**: Team Architecture
