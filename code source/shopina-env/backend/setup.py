"""
Setup script for Shopina backend.
Run this script to set up the database and load sample data.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from django.contrib.auth import get_user_model
from shop.models import Category, Product
from django.core.management import call_command

User = get_user_model()


def create_superuser():
    """Create admin superuser if it doesn't exist."""
    print("\n📝 Creating superuser...")
    
    if User.objects.filter(username='admin').exists():
        print("✅ Superuser 'admin' already exists")
        return
    
    User.objects.create_superuser(
        username='admin',
        email='admin@shopina.com',
        password='admin123',
        role='ADMIN',
        first_name='Admin',
        last_name='User'
    )
    print("✅ Superuser created: username='admin', password='admin123'")


def create_sample_users():
    """Create sample users for testing."""
    print("\n👥 Creating sample users...")
    
    users_data = [
        {
            'username': 'seller1',
            'email': 'seller@shopina.com',
            'password': 'seller123',
            'role': 'SELLER',
            'first_name': 'John',
            'last_name': 'Seller',
            'shop_name': 'John\'s Electronics'
        },
        {
            'username': 'customer1',
            'email': 'customer@shopina.com',
            'password': 'customer123',
            'role': 'CUSTOMER',
            'first_name': 'Jane',
            'last_name': 'Customer'
        }
    ]
    
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            User.objects.create_user(**user_data)
            print(f"✅ Created user: {user_data['username']}")
        else:
            print(f"⏭️  User '{user_data['username']}' already exists")


def create_categories():
    """Create product categories."""
    print("\n📁 Creating categories...")
    
    categories = [
        'Electronics',
        'Clothing',
        'Books',
        'Home & Garden',
        'Sports & Outdoors',
        'Toys & Games',
        'Health & Beauty',
        'Food & Beverages'
    ]
    
    created_categories = []
    for cat_name in categories:
        category, created = Category.objects.get_or_create(name=cat_name)
        if created:
            print(f"✅ Created category: {cat_name}")
        else:
            print(f"⏭️  Category '{cat_name}' already exists")
        created_categories.append(category)
    
    return created_categories


def create_sample_products(categories):
    """Create sample products."""
    print("\n🛍️  Creating sample products...")
    
    products_data = [
        {
            'name': 'Laptop Pro 15"',
            'category': categories[0],  # Electronics
            'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
            'price': 1299.99,
            'stock': 15,
            'rating': 4.5,
            'reviews': 42
        },
        {
            'name': 'Wireless Headphones',
            'category': categories[0],
            'description': 'Noise-cancelling Bluetooth headphones with 30h battery',
            'price': 199.99,
            'stock': 50,
            'rating': 4.7,
            'reviews': 128
        },
        {
            'name': 'Smart Watch',
            'category': categories[0],
            'description': 'Fitness tracker with heart rate monitor',
            'price': 249.99,
            'stock': 30,
            'rating': 4.3,
            'reviews': 85
        },
        {
            'name': 'Cotton T-Shirt',
            'category': categories[1],  # Clothing
            'description': 'Comfortable 100% cotton t-shirt',
            'price': 19.99,
            'stock': 100,
            'rating': 4.2,
            'reviews': 56
        },
        {
            'name': 'Denim Jeans',
            'category': categories[1],
            'description': 'Classic fit denim jeans',
            'price': 49.99,
            'stock': 75,
            'rating': 4.4,
            'reviews': 34
        },
        {
            'name': 'Python Programming Book',
            'category': categories[2],  # Books
            'description': 'Complete guide to Python programming',
            'price': 39.99,
            'stock': 25,
            'rating': 4.8,
            'reviews': 156
        },
        {
            'name': 'Coffee Maker',
            'category': categories[3],  # Home & Garden
            'description': 'Programmable coffee maker with thermal carafe',
            'price': 89.99,
            'stock': 20,
            'rating': 4.6,
            'reviews': 92
        },
        {
            'name': 'Yoga Mat',
            'category': categories[4],  # Sports
            'description': 'Non-slip yoga mat with carrying strap',
            'price': 29.99,
            'stock': 40,
            'rating': 4.5,
            'reviews': 67
        },
        {
            'name': 'Board Game Set',
            'category': categories[5],  # Toys
            'description': 'Family board game for 2-6 players',
            'price': 34.99,
            'stock': 35,
            'rating': 4.7,
            'reviews': 45
        },
        {
            'name': 'Organic Face Cream',
            'category': categories[6],  # Health & Beauty
            'description': 'Natural moisturizing face cream',
            'price': 24.99,
            'stock': 60,
            'rating': 4.4,
            'reviews': 78
        }
    ]
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"✅ Created product: {product_data['name']}")
        else:
            print(f"⏭️  Product '{product_data['name']}' already exists")


def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 Shopina Backend Setup")
    print("=" * 60)
    
    # Run migrations
    print("\n🔄 Running migrations...")
    call_command('migrate', verbosity=1)
    
    # Create data
    create_superuser()
    create_sample_users()
    categories = create_categories()
    create_sample_products(categories)
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Login Credentials:")
    print("   Admin:    username='admin',    password='admin123'")
    print("   Seller:   username='seller1',  password='seller123'")
    print("   Customer: username='customer1', password='customer123'")
    print("\n🌐 Access Points:")
    print("   API Docs:  http://localhost:8000/api/docs/")
    print("   Admin:     http://localhost:8000/admin/")
    print("\n🚀 Start server: python manage.py runserver")
    print("=" * 60)


if __name__ == '__main__':
    main()
