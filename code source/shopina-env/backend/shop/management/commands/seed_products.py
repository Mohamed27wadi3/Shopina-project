from django.core.management.base import BaseCommand
from shop.models import Category, Product


SAMPLE_PRODUCTS = [
    { 'name': 'T-shirt Premium', 'category': 'Mode', 'price': 29.99, 'rating': 4.5, 'reviews': 128, 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400', 'stock': 15 },
    { 'name': 'Casque Audio Pro', 'category': 'Électronique', 'price': 149.99, 'rating': 4.8, 'reviews': 342, 'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', 'stock': 8 },
    { 'name': 'Chaise de Bureau', 'category': 'Maison & Jardin', 'price': 199.99, 'rating': 4.6, 'reviews': 89, 'image': 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400', 'stock': 12 },
    { 'name': 'Montre Connectée', 'category': 'Électronique', 'price': 249.99, 'rating': 4.7, 'reviews': 256, 'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400', 'stock': 20 },
    { 'name': 'Ballon de Football', 'category': 'Sport & Loisirs', 'price': 34.99, 'rating': 4.4, 'reviews': 67, 'image': 'https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400', 'stock': 30 },
    { 'name': 'Sérum Visage', 'category': 'Beauté & Santé', 'price': 45.99, 'rating': 4.9, 'reviews': 412, 'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400', 'stock': 25 },
    { 'name': 'Lampe LED Design', 'category': 'Maison & Jardin', 'price': 59.99, 'rating': 4.3, 'reviews': 54, 'image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400', 'stock': 18 },
    { 'name': 'Livre de Cuisine', 'category': 'Livres & Médias', 'price': 24.99, 'rating': 4.6, 'reviews': 134, 'image': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400', 'stock': 40 },
]


class Command(BaseCommand):
    help = 'Seed database with sample categories and products'

    def handle(self, *args, **options):
        for p in SAMPLE_PRODUCTS:
            cat_name = p['category']
            cat, _ = Category.objects.get_or_create(name=cat_name)
            prod, created = Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': cat,
                    'price': p['price'],
                    'rating': p['rating'],
                    'reviews': p['reviews'],
                    'image': p['image'],
                    'stock': p['stock'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product {prod.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product {prod.name} already exists'))
