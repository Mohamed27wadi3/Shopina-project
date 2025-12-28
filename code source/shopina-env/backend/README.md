# Shopina Backend - Django REST API

> Complete e-commerce backend built with Django REST Framework following Clean Architecture principles

## 🚀 Features

### ✅ Implemented

- **Clean Architecture** - Service Layer + Repository Pattern
- **User Management** - Registration, authentication (JWT), password reset, role-based access (Admin/Seller/Customer)
- **Shopping Cart** - Full cart functionality with real-time stock validation
- **Product Catalog** - CRUD operations, categories, search, filtering
- **Order Management** - Create from cart, status tracking, cancellation with stock restoration
- **Reviews & Ratings** - Product review system with verified purchases
- **Notifications** - User notification system
- **API Documentation** - Swagger UI and ReDoc
- **Admin Dashboard** - Statistics and management endpoints

### 🏗️ Architecture

```
API Layer (Views) → Serializers (DTOs) → Service Layer (Business Logic) → Repository Layer (Data Access) → Models (ORM)
```

## 📋 Tech Stack

- **Framework:** Django 5.2.7
- **API:** Django REST Framework 3.14+
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Documentation:** drf-spectacular (Swagger/ReDoc)
- **Database:** SQLite (development) / PostgreSQL (production ready)
- **Image Handling:** Pillow
- **CORS:** django-cors-headers

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. **Clone and navigate:**
```bash
cd "d:\Shopina Project\code source\backend"
```

2. **Create virtual environment (if not exists):**
```bash
python -m venv shopina-env
shopina-env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Database setup:**

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions.

Quick start (fresh database):
```bash
# Delete old database
del db.sqlite3

# Create migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

5. **Run development server:**
```bash
python manage.py runserver
```

## 📚 API Documentation

Once the server is running, access:

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **Admin Panel:** http://localhost:8000/admin/

## 🔑 API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/token/` - Login (get JWT tokens)
- `POST /api/users/token/refresh/` - Refresh access token

### User Management
- `GET /api/users/profile/` - Get current user profile
- `PATCH /api/users/profile/` - Update profile
- `POST /api/users/password-reset/` - Request password reset
- `POST /api/users/change-password/` - Change password

### Products
- `GET /api/shop/products/` - List products
- `GET /api/shop/products/{id}/` - Get product details
- `GET /api/shop/categories/` - List categories

### Cart
- `GET /api/carts/` - Get user cart
- `POST /api/carts/items/` - Add item to cart
- `PATCH /api/carts/items/{id}/` - Update item quantity
- `DELETE /api/carts/items/{id}/` - Remove item
- `DELETE /api/carts/` - Clear cart
- `GET /api/carts/validate/` - Validate cart for checkout

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create order from cart
- `GET /api/orders/{id}/` - Get order details

### Reviews
- `GET /api/reviews/` - List reviews (filter by product)
- `POST /api/reviews/` - Create review
- `PATCH /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review

### Notifications
- `GET /api/notifications/` - List user notifications
- `POST /api/notifications/{id}/read/` - Mark as read
- `POST /api/notifications/mark-all-read/` - Mark all as read

## 🏛️ Project Structure

```
backend/
├── core/                      # Core architecture
│   ├── services/             # Base service classes
│   ├── repositories/         # Base repository classes
│   ├── permissions/          # Custom permissions
│   ├── utils/               # Utilities (exceptions, validators)
│   └── middleware/          # Error handling middleware
├── users/                    # User management
│   ├── models.py            # User model with roles
│   ├── services/            # User business logic
│   ├── repositories/        # User data access
│   ├── serializers.py       # User DTOs
│   ├── views.py             # User API endpoints
│   └── urls.py              # User routes
├── shop/                     # Product catalog
│   ├── models.py            # Product, Category models
│   ├── services/            # Product business logic
│   ├── repositories/        # Product data access
│   └── ...
├── carts/                    # Shopping cart
├── orders/                   # Order management
├── payments/                 # Payment processing
├── reviews/                  # Product reviews
├── notifications/            # User notifications
└── shopina/                  # Project settings
    ├── settings.py
    └── urls.py
```

## 🔐 Security Features

- JWT-based authentication
- Password hashing (Django's PBKDF2)
- Role-based access control (RBAC)
- CORS configuration
- Input validation at serializer level
- Business logic validation in service layer
- SQL injection protection (Django ORM)
- XSS protection

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test carts
python manage.py test orders
```

## 📊 Database Models

### User
- Extended Django User with roles (ADMIN, SELLER, CUSTOMER)
- Address fields, phone number
- Email verification and password reset tokens

### Product
- Name, description, price, stock
- Category relationship
- Rating and review count

### Cart & CartItem
- One cart per user
- Items with quantity and price snapshot

### Order & OrderItem
- Order status tracking
- Items with price snapshot
- Total calculation

### Review
- User-product relationship
- Rating (0-5) with validation
- Verified purchase flag

### Notification
- Type-based notifications
- Read/unread status

## 🚀 Deployment

### Environment Variables

Create a `.env` file:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
FRONTEND_URL=https://yourdomain.com
STRIPE_SECRET_KEY=your-stripe-key
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure PostgreSQL database
- [ ] Set up static file serving
- [ ] Configure media file storage (S3/CloudFlare)
- [ ] Set up email backend (SMTP)
- [ ] Configure HTTPS
- [ ] Set up Stripe webhooks
- [ ] Enable logging
- [ ] Set up monitoring (Sentry)
- [ ] Configure CORS for production domain

## 📝 Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints where applicable
- Write docstrings for all classes and methods
- Keep functions small and focused

### Architecture Principles
- **Service Layer:** Business logic only
- **Repository Layer:** Data access only
- **Views:** HTTP handling only
- **Serializers:** Data validation and transformation

### Adding New Features

1. Create models in `models.py`
2. Create repository in `repositories/`
3. Create service in `services/`
4. Create serializers in `serializers.py`
5. Create views in `views.py`
6. Add URLs in `urls.py`
7. Write tests

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Update documentation
5. Submit pull request

## 📄 License

This project is proprietary software for Shopina.

## 👥 Team

- Backend Architecture: Clean Architecture implementation
- API Design: RESTful principles
- Security: JWT + RBAC

## 📞 Support

For issues or questions:
- Check the [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- Review API documentation at `/api/docs/`
- Check Django logs for errors

---

**Built with ❤️ using Django REST Framework**
