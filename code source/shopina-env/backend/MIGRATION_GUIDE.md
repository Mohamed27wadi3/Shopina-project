# Database Migration Guide for Shopina Backend

## Overview

This guide provides instructions for setting up a fresh database with all the new models and enhancements.

## Prerequisites

- Python 3.8+
- Django 5.2.7
- All dependencies installed (`pip install -r requirements.txt`)

## Option 1: Fresh Database Setup (Recommended for Development)

### Step 1: Backup Existing Database (if needed)

```bash
cd "d:\Shopina Project\code source\backend"
copy db.sqlite3 db.sqlite3.backup
```

### Step 2: Delete Existing Database and Migrations

```bash
# Delete the database
del db.sqlite3

# Delete migration files (keep __init__.py)
del users\migrations\0001_initial.py
del shop\migrations\0001_initial.py
del orders\migrations\0001_initial.py
del payments\migrations\0001_initial.py
```

### Step 3: Create Fresh Migrations

```bash
python manage.py makemigrations users
python manage.py makemigrations shop
python manage.py makemigrations carts
python manage.py makemigrations orders
python manage.py makemigrations payments
python manage.py makemigrations reviews
python manage.py makemigrations notifications
```

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user with:
- Username
- Email
- Password

### Step 6: Load Sample Data (Optional)

Create a file `load_sample_data.py` in the management commands directory or use Django shell:

```bash
python manage.py shell
```

Then run:

```python
from django.contrib.auth import get_user_model
from shop.models import Category, Product

User = get_user_model()

# Create categories
electronics = Category.objects.create(name="Electronics")
clothing = Category.objects.create(name="Clothing")
books = Category.objects.create(name="Books")

# Create sample products
Product.objects.create(
    name="Laptop",
    category=electronics,
    description="High-performance laptop",
    price=999.99,
    stock=10,
    rating=4.5,
    reviews=25
)

Product.objects.create(
    name="T-Shirt",
    category=clothing,
    description="Comfortable cotton t-shirt",
    price=19.99,
    stock=50,
    rating=4.2,
    reviews=15
)

print("Sample data loaded successfully!")
```

## Option 2: Incremental Migration (For Production)

### Step 1: Create Migration for User Model Changes

Since the User model has significant changes, you need to create a custom migration:

```bash
python manage.py makemigrations users --name add_user_fields
```

### Step 2: Edit the Migration File

Open the generated migration file and ensure it handles:
- Adding new fields with default values
- Converting avatar from URLField to ImageField

### Step 3: Create Migrations for New Apps

```bash
python manage.py makemigrations carts
python manage.py makemigrations reviews
python manage.py makemigrations notifications
```

### Step 4: Apply All Migrations

```bash
python manage.py migrate
```

## Verification

### Check Migration Status

```bash
python manage.py showmigrations
```

All apps should show `[X]` for applied migrations.

### Test the API

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

3. Test authentication:
```bash
# Register a new user
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

## Troubleshooting

### Migration Conflicts

If you encounter migration conflicts:

1. **Check dependencies:**
```bash
python manage.py showmigrations
```

2. **Fake migrations if needed:**
```bash
python manage.py migrate users --fake
```

3. **Squash migrations:**
```bash
python manage.py squashmigrations users 0001 0002
```

### Database Locked Error

If you get "database is locked" error:
1. Close all connections to the database
2. Restart the development server
3. Try the migration again

### Field Type Changes

For the avatar field change (URLField → ImageField):
1. Ensure Pillow is installed: `pip install Pillow`
2. Create a data migration to handle existing URLs
3. Or use a fresh database (Option 1)

## Post-Migration Tasks

### 1. Update Admin Interface

The admin interface is already configured for all models. Access it at:
http://localhost:8000/admin/

### 2. Configure Media Files

Ensure `MEDIA_ROOT` and `MEDIA_URL` are properly configured in settings.py:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 3. Test All Endpoints

Use the Swagger UI to test all API endpoints:
- User registration and authentication
- Cart operations
- Product browsing
- Order creation
- Reviews
- Notifications

## Database Schema Overview

After migration, you'll have these tables:

- `users_user` - Enhanced user model with roles and address
- `shop_category` - Product categories
- `shop_product` - Products with stock and ratings
- `carts_cart` - User shopping carts
- `carts_cartitem` - Items in carts
- `orders_order` - Customer orders
- `orders_orderitem` - Items in orders
- `payments_payment` - Payment records
- `reviews_review` - Product reviews
- `notifications_notification` - User notifications

## Next Steps

1. Run the development server
2. Test all API endpoints
3. Create sample data for testing
4. Configure email settings for password reset
5. Set up Stripe for payments
6. Deploy to staging environment

## Support

If you encounter issues:
1. Check Django logs
2. Verify all dependencies are installed
3. Ensure Python version compatibility
4. Review migration files for conflicts
