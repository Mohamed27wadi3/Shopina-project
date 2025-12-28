# Shopina Backend - Quick Start Guide

## 🚀 Quick Setup (Windows)

### Option 1: Automated Setup (Recommended)

1. **Run the quick setup script:**
```bash
cd "d:\Shopina Project\code source\backend"
quick_setup.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Set up fresh database
- Create sample data (users, categories, products)

2. **Start the server:**
```bash
shopina-env\Scripts\activate
python manage.py runserver
```

3. **Access the application:**
- API Documentation: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/

### Option 2: Manual Setup

1. **Create virtual environment:**
```bash
cd "d:\Shopina Project\code source\backend"
python -m venv shopina-env
shopina-env\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup database:**
```bash
# Delete old database
del db.sqlite3

# Run setup script
python setup.py
```

4. **Start server:**
```bash
python manage.py runserver
```

## 🔑 Default Credentials

After running setup, you can login with:

- **Admin:** username=`admin`, password=`admin123`
- **Seller:** username=`seller1`, password=`seller123`
- **Customer:** username=`customer1`, password=`customer123`

## 📚 Next Steps

1. **Explore the API:**
   - Visit http://localhost:8000/api/docs/ for interactive API documentation
   - Try the example requests in [API_TESTING.md](API_TESTING.md)

2. **Admin Panel:**
   - Visit http://localhost:8000/admin/
   - Login with admin credentials
   - Manage users, products, orders, etc.

3. **Test the API:**
   - See [API_TESTING.md](API_TESTING.md) for curl examples
   - Use Postman or any HTTP client
   - Try the complete purchase flow

## 📖 Documentation

- **[README.md](README.md)** - Complete project documentation
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Database migration guide
- **[API_TESTING.md](API_TESTING.md)** - API testing examples

## 🛠️ Common Commands

```bash
# Activate virtual environment
shopina-env\Scripts\activate

# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test

# Create admin user via shell
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.create_superuser('admin', 'admin@shopina.com', 'admin123', role='ADMIN')
```

## 🔍 Troubleshooting

### Port already in use
```bash
# Use different port
python manage.py runserver 8001
```

### Database locked
```bash
# Close all connections and restart server
# Or delete db.sqlite3 and run setup.py again
```

### Module not found
```bash
# Ensure virtual environment is activated
shopina-env\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

## 🎯 Quick Test

Test if everything works:

```bash
# 1. Start server
python manage.py runserver

# 2. In another terminal, test API
curl http://localhost:8000/api/shop/products/

# 3. Should return list of products
```

## 📞 Support

- Check logs in terminal for errors
- Review [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for database issues
- See [API_TESTING.md](API_TESTING.md) for API examples

---

**Ready to go! 🚀**
