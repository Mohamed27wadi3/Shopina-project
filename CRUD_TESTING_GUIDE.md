# CRUD Operations Testing Guide

## Overview
This document provides comprehensive testing procedures for all CRUD (Create, Read, Update, Delete) operations in the Shopina platform.

## Backend Endpoints

### Users API

#### Create User (Sign Up)
```bash
POST /api/users/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "Jean",
  "last_name": "Dupont"
}

Response: 201 Created
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Jean",
    "last_name": "Dupont"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```bash
POST /api/users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

#### Remember Me Login (30-day session)
```bash
POST /api/users/auth/remember-me/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "remember": true
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..." (30-day lifetime),
  "user": { ... }
}
```

#### Social Login - Google
```bash
POST /api/users/auth/google/
Content-Type: application/json

{
  "access_token": "ya29.a0AfH6SMBx..."
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

#### Social Login - GitHub
```bash
POST /api/users/auth/github/
Content-Type: application/json

{
  "access_token": "gho_16C7e42F292c6912E7710c3f470..."
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

#### Get User Profile (Protected)
```bash
GET /api/users/profile/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jean",
  "last_name": "Dupont",
  "avatar": "https://...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Update User Profile (Protected)
```bash
PUT /api/users/profile/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "first_name": "Jean-Paul",
  "last_name": "Dupont",
  "phone": "+33612345678",
  "avatar": "base64_or_url"
}

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jean-Paul",
  "last_name": "Dupont",
  "phone": "+33612345678",
  "avatar": "https://..."
}
```

### Products API

#### List Products
```bash
GET /api/shop/products/
Query Parameters:
  - page: 1
  - search: "shirt"
  - category: 1
  - min_price: 10
  - max_price: 100
  - sort: "-created_at" or "price"

Response: 200 OK
{
  "count": 150,
  "next": "http://localhost:8000/api/shop/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Blue T-Shirt",
      "description": "High-quality cotton t-shirt",
      "price": "29.99",
      "category": 1,
      "image": "https://...",
      "stock": 50,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Product (Protected - Shop Owner)
```bash
POST /api/shop/products/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Blue T-Shirt",
  "description": "High-quality cotton t-shirt",
  "price": "29.99",
  "category": 1,
  "stock": 50,
  "image": "base64_or_url"
}

Response: 201 Created
{
  "id": 1,
  "name": "Blue T-Shirt",
  "description": "High-quality cotton t-shirt",
  "price": "29.99",
  "category": 1,
  "image": "https://...",
  "stock": 50,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Product Detail
```bash
GET /api/shop/products/{id}/

Response: 200 OK
{
  "id": 1,
  "name": "Blue T-Shirt",
  "description": "High-quality cotton t-shirt",
  "price": "29.99",
  "category": 1,
  "image": "https://...",
  "stock": 50,
  "reviews_count": 5,
  "average_rating": 4.5,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Update Product (Protected - Owner)
```bash
PUT /api/shop/products/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Blue T-Shirt Premium",
  "price": "39.99",
  "stock": 40
}

Response: 200 OK
{ ... updated product ... }
```

#### Delete Product (Protected - Owner)
```bash
DELETE /api/shop/products/{id}/
Authorization: Bearer {access_token}

Response: 204 No Content
```

### Orders API

#### Create Order (Protected)
```bash
POST /api/orders/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "items": [
    {
      "product": 1,
      "quantity": 2
    },
    {
      "product": 3,
      "quantity": 1
    }
  ],
  "shipping_address": "123 Main St, Paris, 75001",
  "payment_method": "stripe"
}

Response: 201 Created
{
  "id": 1,
  "items": [ ... ],
  "total": "89.97",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List Orders (Protected)
```bash
GET /api/orders/
Authorization: Bearer {access_token}
Query Parameters:
  - status: "pending" | "completed" | "cancelled"
  - page: 1

Response: 200 OK
{
  "count": 5,
  "results": [ ... ]
}
```

#### Get Order Detail (Protected)
```bash
GET /api/orders/{id}/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "items": [
    {
      "product": 1,
      "product_name": "Blue T-Shirt",
      "quantity": 2,
      "price": "29.99"
    }
  ],
  "total": "89.97",
  "status": "completed",
  "tracking": "TRK123456",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Update Order Status (Protected - Admin)
```bash
PATCH /api/orders/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "shipped",
  "tracking": "TRK123456"
}

Response: 200 OK
{ ... updated order ... }
```

#### Cancel Order (Protected)
```bash
POST /api/orders/{id}/cancel/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "status": "cancelled",
  "refund_status": "pending"
}
```

### Cart API

#### Add to Cart (Protected)
```bash
POST /api/carts/items/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "product": 1,
  "quantity": 2
}

Response: 201 Created
{
  "id": 1,
  "product": 1,
  "quantity": 2,
  "price": "29.99",
  "subtotal": "59.98"
}
```

#### Get Cart (Protected)
```bash
GET /api/carts/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": 1,
      "product_name": "Blue T-Shirt",
      "quantity": 2,
      "price": "29.99",
      "subtotal": "59.98"
    }
  ],
  "total": "89.97",
  "item_count": 3
}
```

#### Update Cart Item (Protected)
```bash
PATCH /api/carts/items/{item_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "quantity": 3
}

Response: 200 OK
{ ... updated item ... }
```

#### Remove from Cart (Protected)
```bash
DELETE /api/carts/items/{item_id}/
Authorization: Bearer {access_token}

Response: 204 No Content
```

#### Clear Cart (Protected)
```bash
DELETE /api/carts/
Authorization: Bearer {access_token}

Response: 204 No Content
```

### Reviews API

#### Create Review (Protected)
```bash
POST /api/reviews/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "product": 1,
  "rating": 5,
  "comment": "Excellent product, highly recommended!"
}

Response: 201 Created
{
  "id": 1,
  "product": 1,
  "rating": 5,
  "comment": "Excellent product, highly recommended!",
  "author": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List Product Reviews
```bash
GET /api/reviews/?product={product_id}
Query Parameters:
  - rating: 5
  - page: 1

Response: 200 OK
{
  "count": 10,
  "results": [ ... ]
}
```

#### Update Review (Protected - Author)
```bash
PUT /api/reviews/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "rating": 4,
  "comment": "Good product, but could be better"
}

Response: 200 OK
{ ... updated review ... }
```

#### Delete Review (Protected - Author/Admin)
```bash
DELETE /api/reviews/{id}/
Authorization: Bearer {access_token}

Response: 204 No Content
```

## Testing with cURL

### Example: Complete User Flow

```bash
# 1. Sign up
curl -X POST http://localhost:8000/api/users/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Store the access token from response
export TOKEN="your_access_token_here"

# 2. Get profile
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Update profile
curl -X PUT http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "phone": "+33612345678"
  }'

# 4. Add product to cart
curl -X POST http://localhost:8000/api/carts/items/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "quantity": 2
  }'

# 5. Create order
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product": 1, "quantity": 2}],
    "shipping_address": "123 Main St, Paris",
    "payment_method": "stripe"
  }'
```

## Testing with Postman

1. Import the endpoints from this documentation
2. Set up environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: (populate after login)
3. Run tests in sequence
4. Use Postman's test scripts to validate responses

## Error Handling

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Resource deleted or action completed
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Example Error Response

```json
{
  "error": "Invalid credentials",
  "detail": "Email and password combination is incorrect"
}
```

## Performance Testing

### Load Testing
Use Apache Bench or Locust for load testing:

```bash
# Test product list endpoint
ab -n 1000 -c 10 http://localhost:8000/api/shop/products/

# Test with authentication
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/orders/
```

## Checklist for Complete Testing

- [ ] User Registration & Login
- [ ] Social Login (Google, GitHub)
- [ ] Remember Me functionality
- [ ] User Profile CRUD
- [ ] Product CRUD
- [ ] Order CRUD
- [ ] Cart operations
- [ ] Reviews CRUD
- [ ] Permission checks (401, 403)
- [ ] Data validation
- [ ] Error messages
- [ ] Performance under load
