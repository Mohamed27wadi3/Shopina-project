# Design Patterns Implémentés dans le Projet Shopina

## 📋 Résumé Rapide des 10 Design Patterns

### 1️⃣ Observer Pattern 🔍
**Utilisation:** Django Signals
**Localisation:** Partout où on écoute les événements
**Concept:** Écoute automatique des changements
```
Événement (Product.save) → Observers (signal handlers) → Actions
```

### 2️⃣ Strategy Pattern 🎯
**Utilisation:** `core/utils/validators.py`
**Localisation:** Chaque validateur est une stratégie
**Concept:** Changer l'algorithme selon le contexte
```
validate_price() | validate_quantity() | validate_rating() 
→ Choisir la bonne stratégie
```

### 3️⃣ Proxy Pattern 🛡️
**Utilisation:** Django ORM QuerySet
**Localisation:** Toutes les requêtes BDD
**Concept:** Accès contrôlé et optimisé aux données
```
Product.objects.filter(...).select_related(...) 
→ Lazy evaluation + Optimisation N+1
```

### 4️⃣ Facade Pattern 🎭
**Utilisation:** `shop/services/product_service.py`
**Localisation:** Toutes les classes Service
**Concept:** Interface simple pour logique complexe
```
ProductService.create_product()
→ Validation + Check catégorie + Création + Log (tout en un!)
```

### 5️⃣ Adapter Pattern 🔌
**Utilisation:** `shop/admin.py` (ModelAdmin)
**Localisation:** Toutes les admin classes
**Concept:** Adapter Model → Admin interface
```
ProductAdmin adapte Product Model
→ list_display, search_fields, filters
```

### 6️⃣ Prototype Pattern 🔄
**Utilisation:** Django `deepcopy()` pour cloner models
**Localisation:** Quand on veut copier un objet
**Concept:** Créer une copie rapidement
```
original = Product.objects.get(id=1)
cloned = deepcopy(original)
→ Nouveau produit identique
```

### 7️⃣ Builder Pattern 🏗️
**Utilisation:** Django QueryBuilder, Serializers
**Localisation:** Construire des requêtes complexes
**Concept:** Construire étape par étape
```
query = Product.objects.all()
if category: query = query.filter(category_id=...)
if stock: query = query.filter(stock__gt=0)
if order: query = query.order_by(order)
→ Requête construite progressivement
```

### 8️⃣ Singleton Pattern 👁️
**Utilisation:** Django Settings, Database Connection
**Localisation:** Partout dans l'app
**Concept:** Une seule instance pour tout
```
settings.DEBUG → Même Settings
connection → Même connexion BDD
→ Pas de duplication
```

### 9️⃣ Factory Method Pattern 🏭
**Utilisation:** Django `objects.create()`, ViewSets
**Localisation:** Toute création d'objets
**Concept:** Créer sans spécifier la classe
```
Product.objects.create(name="...", price=...)
→ Factory crée, initialise, sauvegarde
```

### 🔟 Abstract Factory Pattern 🏢
**Utilisation:** Django Apps (shop, users, orders)
**Localisation:** Structure de l'application
**Concept:** Familles d'objets liés
```
shop/ → Products, Categories, Serializers
users/ → Users, Auth, Verification
orders/ → Orders, Items, Payment
→ Chaque app = une factory
```

---

## 🗺️ Où Trouver Chaque Pattern

| # | Pattern | Fichier | Ligne | Description |
|---|---------|---------|-------|-------------|
| 1 | Observer | `models.py` avec signals | - | Django Signals post_save |
| 2 | Strategy | `core/utils/validators.py` | - | Chaque fonction validateur |
| 3 | Proxy | `shop/repositories/product_repository.py` | - | QuerySet.filter().select_related() |
| 4 | Facade | `shop/services/product_service.py` | create_product_for_shop | Une méthode qui fait tout |
| 5 | Adapter | `shop/admin.py` | ProductAdmin | ModelAdmin adapte Model |
| 6 | Prototype | `models.py` | - | deepcopy pour cloner |
| 7 | Builder | `shop/repositories/product_repository.py` | - | QuerySet construction |
| 8 | Singleton | `settings.py` | - | Configuration unique |
| 9 | Factory | `models.py` | objects.create() | ORM factory |
| 10 | Abstract | `apps/` | AppConfig | Chaque app = factory |

---

## 💡 Exemples Code Réels

### 1. Observer - Mettre à jour la note quand un review est créé
```python
# signals.py
@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.update_rating()
```

### 2. Strategy - Choisir le validateur
```python
# validators.py
is_valid, error = validate_price(9.99)
is_valid, error = validate_quantity(5)
```

### 3. Proxy - Requête optimisée
```python
# product_repository.py
products = self.model.objects.filter(stock__gt=0).select_related('category')
# select_related = proxy qui évite N+1 queries
```

### 4. Facade - Une méthode qui fait tout
```python
# product_service.py
product = product_service.create_product_for_shop(
    shop=shop,
    name=name,
    price=price,
    # Derrière: validation + check catégorie + création + log
)
```

### 5. Adapter - Adapter pour l'admin
```python
# admin.py
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    # Adapter transforme Product en interface admin
```

### 6. Prototype - Cloner un produit
```python
original = Product.objects.get(id=1)
clone = deepcopy(original)
clone.id = None
clone.name = "Clone"
clone.save()
```

### 7. Builder - Requête progressive
```python
query = Product.objects.all()
if category_id:
    query = query.filter(category_id=category_id)
if in_stock_only:
    query = query.filter(stock__gt=0)
products = query[:10]
```

### 8. Singleton - Settings unique
```python
from django.conf import settings
print(settings.DEBUG)  # Même instance partout
```

### 9. Factory - Créer via factory
```python
product = Product.objects.create(name="Laptop", price=999.99)
# Factory crée, initialise, sauvegarde
```

### 10. Abstract Factory - Apps comme factories
```
shop/
  - models.py (Product, Category)
  - serializers.py (ProductSerializer)
  - views.py (ProductViewSet)

users/
  - models.py (User, TwoFactor)
  - serializers.py (UserSerializer)
  - views.py (UserViewSet)

# Chaque app = une factory complète
```

---

## 🎯 Avantages Résumés

| Pattern | Avantages Clés |
|---------|-----------------|
| **Observer** | Découplage, Automatisation, Extensibilité |
| **Strategy** | Flexibilité, Testabilité, Réutilisabilité |
| **Proxy** | Optimisation, Lazy evaluation, Contrôle |
| **Facade** | Simplicité, Cohérence, Réutilisabilité |
| **Adapter** | Transformation, Personnalisation, Réutilisabilité |
| **Prototype** | Rapidité, Variation, Réutilisabilité |
| **Builder** | Flexibilité, Lisibilité, Optionnalité |
| **Singleton** | Unicité, Efficacité, Cohérence |
| **Factory** | Simplicité, Flexibilité, Cohérence |
| **Abstract** | Organisation, Cohérence, Extensibilité |

---

## 📚 À Retenir

Chaque pattern résout un problème spécifique:

- **Observer** - Je veux écouter les changements
- **Strategy** - Je veux changer l'algorithme
- **Proxy** - Je veux optimiser l'accès
- **Facade** - Je veux simplifier l'interface
- **Adapter** - Je veux adapter deux interfaces
- **Prototype** - Je veux copier rapidement
- **Builder** - Je veux construire progressivement
- **Singleton** - Je veux une seule instance
- **Factory** - Je veux créer sans détails
- **Abstract** - Je veux des familles d'objets
