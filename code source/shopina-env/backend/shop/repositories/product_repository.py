"""
Product repository for data access operations.

PRINCIPES SOLID APPLIQUÉS DANS CE FICHIER:
==========================================

1. S - Single Responsibility (Responsabilité Unique):
   - Ce fichier a UNE SEULE responsabilité: accéder aux données Product
   - Il ne fait PAS de logique métier (c'est dans ProductService)
   - Il ne gère PAS les requêtes HTTP (c'est dans les Views)

2. O - Open/Closed (Ouvert/Fermé):
   - ProductRepository HÉRITE de BaseRepository
   - On AJOUTE des méthodes (get_by_slug, get_active_products)
   - On ne MODIFIE PAS BaseRepository

3. L - Liskov Substitution (Substitution de Liskov):
   - ProductRepository peut REMPLACER BaseRepository partout
   - Les méthodes retournent le même type que BaseRepository attend
   - get_by_id() retourne Optional[Product] comme le parent

4. D - Dependency Inversion (Inversion de Dépendance):
   - Ce repository est une ABSTRACTION entre Service et Model
   - ProductService dépend de ProductRepository, PAS du Model directement
   - On peut changer la base de données sans toucher le Service
"""
from typing import Optional, List
from django.db.models import QuerySet, Q, Avg
from core.repositories.base import BaseRepository
from shop.models import Product, Category


# O - Open/Closed: Cette classe ÉTEND BaseRepository sans le modifier
# L - Liskov: ProductRepository peut remplacer BaseRepository partout
class ProductRepository(BaseRepository[Product]):
    """
    Repository for Product model data access.
    
    PRINCIPE S - RESPONSABILITÉ UNIQUE:
    Ce repository a UNE SEULE responsabilité: gérer l'accès aux données Product
    """
    
    def __init__(self):
        # On appelle le constructeur parent avec le model Product
        super().__init__(Product)
    
    # O - Open/Closed: On AJOUTE cette méthode sans modifier BaseRepository
    # S - Responsabilité Unique: Cette méthode fait UNE CHOSE: chercher par slug
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """
        Get product by slug.
        
        Args:
            slug: Product slug
            
        Returns:
            Product instance or None
        """
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None
    
    # S - Responsabilité Unique: Cette méthode fait UNE CHOSE: récupérer produits actifs
    def get_active_products(self) -> QuerySet[Product]:
        """
        Get all active products.
        
        Returns:
            QuerySet of active products
        """
        # Optimisation: select_related évite les requêtes multiples (N+1 problem)
        return self.model.objects.filter(stock__gt=0).select_related('category')
    
    # S - Une seule responsabilité: filtrer par catégorie
    def get_by_category(self, category_id: int) -> QuerySet[Product]:
        """
        Get products by category.
        
        Args:
            category_id: Category ID
            
        Returns:
            QuerySet of products
        """
        return self.model.objects.filter(category_id=category_id).select_related('category')
    
    # S - Une seule responsabilité: rechercher des produits
    def search_products(self, query: str) -> QuerySet[Product]:
        """
        Search products by name or description.
        
        Args:
            query: Search query
            
        Returns:
            QuerySet of matching products
        """
        # Q objects permettent de faire des OR dans les requêtes Django
        return self.model.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).select_related('category')
    
    # S - Une seule responsabilité: obtenir les produits les mieux notés
    def get_top_rated(self, limit: int = 10) -> QuerySet[Product]:
        """
        Get top rated products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            QuerySet of top rated products
        """
        return self.model.objects.order_by('-rating')[:limit]
    
    # S - Une seule responsabilité: obtenir les produits mis en avant
    def get_featured_products(self, limit: int = 10) -> QuerySet[Product]:
        """
        Get featured products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            QuerySet of featured products
        """
        # Pour l'instant, retourne les mieux notés. On peut ajouter un champ 'featured' plus tard
        # O - Open/Closed: Facile d'étendre sans modifier le code existant
        return self.get_top_rated(limit)
    
    # S - Une seule responsabilité: mettre à jour le stock
    # Cette méthode fait UNIQUEMENT la mise à jour, pas de validation
    # La validation est dans ProductService (séparation des responsabilités)
    def update_stock(self, product: Product, quantity_change: int) -> Product:
        """
        Update product stock.
        
        Args:
            product: Product instance
            quantity_change: Change in stock (positive or negative)
            
        Returns:
            Updated product
        """
        product.stock += quantity_change
        product.save()
        return product
    
    # S - Une seule responsabilité: mettre à jour la note moyenne
    def update_rating(self, product: Product) -> Product:
        """
        Update product rating based on reviews.
        
        Args:
            product: Product instance
            
        Returns:
            Updated product
        """
        # Import local pour éviter les imports circulaires
        from reviews.models import Review
        
        # Calcul de la moyenne des notes
        avg_rating = Review.objects.filter(product=product).aggregate(
            avg=Avg('rating')
        )['avg']
        
        if avg_rating:
            product.rating = round(avg_rating, 1)
            product.reviews = Review.objects.filter(product=product).count()
            product.save()
        
        return product


# O - Open/Closed: CategoryRepository ÉTEND BaseRepository
# L - Liskov: CategoryRepository peut remplacer BaseRepository
class CategoryRepository(BaseRepository[Category]):
    """
    Repository for Category model data access.
    
    PRINCIPE S - RESPONSABILITÉ UNIQUE:
    Ce repository a UNE SEULE responsabilité: gérer l'accès aux données Category
    """
    
    def __init__(self):
        # On appelle le constructeur parent avec le model Category
        super().__init__(Category)
    
    # O - Open/Closed: On AJOUTE cette méthode sans modifier BaseRepository
    # S - Responsabilité Unique: chercher une catégorie par nom
    def get_by_name(self, name: str) -> Optional[Category]:
        """
        Get category by name.
        
        Args:
            name: Category name
            
        Returns:
            Category instance or None
        """
        try:
            # iexact = insensible à la casse (case-insensitive)
            return self.model.objects.get(name__iexact=name)
        except self.model.DoesNotExist:
            return None
    
    # S - Une seule responsabilité: obtenir catégories avec comptage
    def get_with_product_count(self):
        """
        Get categories with product count.
        
        Returns:
            QuerySet with annotations
        """
        from django.db.models import Count
        # Annotation = ajouter un champ calculé au QuerySet
        return self.model.objects.annotate(product_count=Count('products'))
