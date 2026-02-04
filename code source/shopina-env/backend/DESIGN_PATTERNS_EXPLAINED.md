# Design Patterns dans le Projet Shopina

## 1. Observer Pattern 🔍
**Où:** Django Signals
**Fichier:** `core/signals.py` (ou utilisé dans les models)

```python
# Django Signals = Observer Pattern
# Écoute les événements (save, delete, m2m_changed)
# Permet de déclencher des actions automatiquement

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Product)
def update_product_rating(sender, instance, created, **kwargs):
    """
    Observer Pattern: Observateur qui écoute l'événement 'post_save' du Model Product
    Quand un Product est sauvegardé → Met à jour la note automatiquement
    """
    if not created:
        # Le product a été modifié, recalculer la note
        instance.update_rating()
```

**Avantages:**
- ✅ Découplage: Le Model ne connaît pas ce qui écoute les événements
- ✅ Automatisation: Actions déclenchées automatiquement
- ✅ Extensible: Ajouter de nouveaux observateurs sans modifier le Model

**Exemple réel:**
- Quand un produit est créé → Envoyer email au marchand
- Quand une commande change → Mettre à jour l'inventaire
- Quand un avis est ajouté → Recalculer la note moyenne

---

## 2. Strategy Pattern 🎯
**Où:** `core/utils/validators.py`
**Fichier:** Chaque validateur est une stratégie différente

```python
# Strategy Pattern: Chaque validateur = une stratégie
# On peut changer la stratégie selon le contexte

def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """Stratégie 1: Valider le prix"""
    if price < 0:
        return False, "Price cannot be negative"
    return True, None

def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """Stratégie 2: Valider la quantité"""
    if quantity < 1:
        return False, "Quantity must be at least 1"
    return True, None

# Utilisation: Choisir la bonne stratégie
def create_product(price, quantity):
    is_valid, error = validate_price(price)
    if not is_valid:
        raise ValidationError(error)
    
    is_valid, error = validate_quantity(quantity)
    if not is_valid:
        raise ValidationError(error)
```

**Avantages:**
- ✅ Flexibilité: Changer facilement la stratégie
- ✅ Testabilité: Chaque stratégie se teste seule
- ✅ Réutilisabilité: La même stratégie pour plusieurs contextes

---

## 3. Proxy Pattern 🛡️
**Où:** Django ORM QuerySet
**Concept:** Le QuerySet est un proxy vers la base de données

```python
# Proxy Pattern: Le QuerySet n'exécute pas la requête immédiatement
# Il la prépare et l'exécute seulement quand nécessaire (lazy evaluation)

# Préparation (pas d'exécution):
query = Product.objects.filter(price__gt=100)  # Pas encore exécuté!

# Exécution (maintenant):
products = list(query)  # Maintenant la requête s'exécute

# Utilité: Optimisation des requêtes
products = Product.objects.filter(stock__gt=0).select_related('category')
# select_related = proxy qui optimise pour éviter N+1 queries
```

**Avantages:**
- ✅ Lazy evaluation: Exécuter seulement quand nécessaire
- ✅ Optimisation: Combiner plusieurs requêtes en une seule
- ✅ Contrôle: Modifier la requête avant exécution

---

## 4. Facade Pattern 🎭
**Où:** `shop/services/product_service.py`
**Concept:** Interface simple pour une logique complexe

```python
# Facade Pattern: ProductService masque la complexité

class ProductService(BaseService[Product]):
    """
    Facade Pattern: Interface simple pour toute la logique produit
    Simplifie l'interaction avec les repositories, validateurs, modèles
    """
    
    def create_product_for_shop(self, shop, name, price, ...):
        """
        Facade Method: Fait plusieurs choses en une seule méthode
        1. Valider le prix
        2. Valider le stock
        3. Vérifier la catégorie
        4. Créer le produit
        5. Logger l'opération
        """
        # Validation
        is_valid, error = validate_price(price)
        if not is_valid:
            raise ValidationError(error)
        
        # Vérifier la catégorie
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ResourceNotFoundError("Category not found")
        
        # Créer le produit
        product = Product.objects.create(...)
        
        # Logger
        self.log_operation('product_created', {...})
        
        return product
```

**Avantages:**
- ✅ Simplicité: Une seule méthode au lieu de 5
- ✅ Cohérence: Logique centralisée
- ✅ Réutilisabilité: Utilisée par Views, API, CLI

---

## 5. Adapter Pattern 🔌
**Où:** `shop/admin.py`
**Concept:** Adapter un Model pour l'interface Admin

```python
# Adapter Pattern: Adapter Product pour l'interface Django Admin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Adapter Pattern: Adapte Product Model pour l'interface Admin
    Transforme le Model en interface utilisateur (liste, formulaire, filtres)
    """
    list_display = ('id', 'name', 'category', 'price', 'stock')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

# Sans cet adapter, Product ne serait pas visible dans Admin
# Avec cet adapter, on peut l'administrer facilement
```

**Avantages:**
- ✅ Transformation: Model → Interface Admin
- ✅ Personnalisation: Affichage sur mesure
- ✅ Réutilisabilité: Plusieurs admins pour le même Model

---

## 6. Prototype Pattern 🔄
**Où:** Django Model clone
**Concept:** Copier un objet pour créer une variante

```python
# Prototype Pattern: Copier un produit existant

from copy import deepcopy

# Créer un prototype
original_product = Product.objects.get(id=1)

# Cloner le prototype pour créer une variante
cloned_product = deepcopy(original_product)
cloned_product.id = None  # Réinitialiser l'ID
cloned_product.name = "Product Copy"
cloned_product.save()

# Résultat: Nouveau produit identique au premier
```

**Avantages:**
- ✅ Rapidité: Créer une copie rapidement
- ✅ Variation: Modifier la copie sans toucher l'original
- ✅ Réutilisabilité: Template pour créer plusieurs copies

---

## 7. Builder Pattern 🏗️
**Où:** Django QueryBuilder, ProductSerializer
**Concept:** Construire un objet complexe étape par étape

```python
# Builder Pattern: Construire une requête complexe

query_builder = Product.objects.all()

# Étape 1: Filtrer
if category_id:
    query_builder = query_builder.filter(category_id=category_id)

# Étape 2: Filtrer le stock
if in_stock_only:
    query_builder = query_builder.filter(stock__gt=0)

# Étape 3: Ordonner
if order_by:
    query_builder = query_builder.order_by(order_by)

# Étape 4: Optimiser
query_builder = query_builder.select_related('category')

# Étape 5: Exécuter
products = query_builder[:10]

# Chaque étape ajoute quelque chose, construisant la requête finale
```

**Avantages:**
- ✅ Flexibilité: Construire étape par étape
- ✅ Lisibilité: Code fluide et compréhensible
- ✅ Optionnalité: Certaines étapes peuvent être omises

---

## 8. Singleton Pattern 👁️
**Où:** Django Settings, Database Connection
**Concept:** Une seule instance pour tout l'application

```python
# Singleton Pattern: Django Settings est un Singleton

from django.conf import settings

# Partout dans l'app:
print(settings.DEBUG)  # Même instance partout
print(settings.DATABASES)  # Même configuration

# Django assure qu'il n'y a qu'une seule instance de Settings
# Économise les ressources, garantit la cohérence

# Database Connection: Une seule connexion réutilisée
from django.db import connection
print(connection.connection)  # Même connexion partout
```

**Avantages:**
- ✅ Unicité: Un seul objet pour tout
- ✅ Efficacité: Pas de duplication
- ✅ Cohérence: Même configuration partout

---

## 9. Factory Method Pattern 🏭
**Où:** Django ORM `objects.create()`, ViewSets
**Concept:** Créer des objets sans spécifier leur classe exacte

```python
# Factory Method Pattern: Django ORM create()

# Factory Method: Créer un Product
product = Product.objects.create(
    name="Laptop",
    price=999.99,
    category_id=1
)

# Sous le capot, Django:
# 1. Crée une instance Product
# 2. L'initialise avec les données
# 3. La sauvegarde en BDD
# 4. La retourne

# On ne dit pas "créer l'instance, initialiser, sauvegarder"
# On dit simplement "create()" et ça le fait!

# Factory Method pour les ViewSets:
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Factory: Crée les actions CRUD automatiquement"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

**Avantages:**
- ✅ Simplicité: Créer sans penser à l'implémentation
- ✅ Flexibilité: Changer la création sans toucher au code client
- ✅ Cohérence: Même méthode de création partout

---

## 10. Abstract Factory Pattern 🏢
**Où:** Django Apps (AppConfig), Repository Pattern
**Concept:** Créer des familles d'objets liés

```python
# Abstract Factory Pattern: Django Apps

# Chaque app (shop, users, orders) est une factory
# Crée ses propres Models, Serializers, ViewSets

# shop/ app factory:
# - Models: Product, Category
# - Serializers: ProductSerializer, CategorySerializer
# - ViewSets: ProductViewSet, CategoryViewSetx

# users/ app factory:
# - Models: User, TwoFactor
# - Serializers: UserSerializer
# - ViewSets: UserViewSet

# orders/ app factory:
# - Models: Order, OrderItem
# - Serializers: OrderSerializer
# - ViewSets: OrderViewSet

# Chaque app = une AbstractFactory qui crée sa famille d'objets

# Exemple en code:
class RepositoryFactory:
    """Abstract Factory: Crée les repositories"""
    
    @staticmethod
    def create_product_repository():
        return ProductRepository()
    
    @staticmethod
    def create_order_repository():
        return OrderRepository()
    
    @staticmethod
    def create_user_repository():
        return UserRepository()

# Utilisation:
repo = RepositoryFactory.create_product_repository()
```

**Avantages:**
- ✅ Organisation: Familles d'objets regroupées
- ✅ Cohérence: Objets liés créés ensemble
- ✅ Extensibilité: Ajouter une nouvelle app (nouvelle factory)

---

## Résumé Visuel

```
Observer     ← Écoute les événements (signals)
Strategy     ← Choisir la validateur
Proxy        ← QuerySet lazy evaluation
Facade       ← Interface simple (Service)
Adapter      ← Model → Admin
Prototype    ← Copier un objet
Builder      ← Construire étape par étape
Singleton    ← Une seule instance (Settings)
Factory      ← Créer des objets (create())
Abstract     ← Familles d'objets (Apps)
```

---

## Tableau Comparatif

| Pattern | Problème | Solution | Exemple |
|---------|----------|----------|---------|
| Observer | Découplage événements | Écouter les changements | Django signals |
| Strategy | Flexibilité validation | Changer l'algorithme | Validators |
| Proxy | Optimisation requêtes | Lazy evaluation | QuerySet |
| Facade | Complexité cachée | Interface simple | Service |
| Adapter | Incompatibilité interfaces | Transformer | Admin |
| Prototype | Copie rapide | Clone profond | deepcopy |
| Builder | Objet complexe | Construire étape par étape | QueryBuilder |
| Singleton | Unicité | Une seule instance | Settings |
| Factory | Création flexible | Abstrait la création | create() |
| Abstract | Familles d'objets | Lier les créations | Apps |
