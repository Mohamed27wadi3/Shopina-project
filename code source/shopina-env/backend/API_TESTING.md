# API Testing Examples

This document provides examples of how to test the Shopina API using curl commands.

## Authentication

### Register a New User

```bash
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

### Login (Get JWT Token)

```bash
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Save the access token for subsequent requests!**

### Get User Profile

```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Profile

```bash
curl -X PATCH http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "phone_number": "+1234567890",
    "city": "Paris"
  }'
```

## Products

### List All Products

```bash
curl -X GET http://localhost:8000/api/shop/products/
```

### Search Products

```bash
curl -X GET "http://localhost:8000/api/shop/products/?search=laptop"
```

### Filter by Category

```bash
curl -X GET "http://localhost:8000/api/shop/products/?category__name=Electronics"
```

### Get Product Details

```bash
curl -X GET http://localhost:8000/api/shop/products/1/
```

### List Categories

```bash
curl -X GET http://localhost:8000/api/shop/categories/
```

## Shopping Cart

### Get Cart

```bash
curl -X GET http://localhost:8000/api/carts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Add Item to Cart

```bash
curl -X POST http://localhost:8000/api/carts/items/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### Update Cart Item Quantity

```bash
curl -X PATCH http://localhost:8000/api/carts/items/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 3
  }'
```

### Remove Item from Cart

```bash
curl -X DELETE http://localhost:8000/api/carts/items/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Clear Cart

```bash
curl -X DELETE http://localhost:8000/api/carts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Validate Cart for Checkout

```bash
curl -X GET http://localhost:8000/api/carts/validate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Orders

### Create Order from Cart

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### List User Orders

```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Order Details

```bash
curl -X GET http://localhost:8000/api/orders/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Reviews

### List Product Reviews

```bash
curl -X GET "http://localhost:8000/api/reviews/?product=1"
```

### Create Review

```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "rating": 4.5,
    "comment": "Great product! Highly recommended."
  }'
```

### Update Review

```bash
curl -X PATCH http://localhost:8000/api/reviews/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5.0,
    "comment": "Updated: Excellent product!"
  }'
```

### Delete Review

```bash
curl -X DELETE http://localhost:8000/api/reviews/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Notifications

### List Notifications

```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Mark Notification as Read

```bash
curl -X POST http://localhost:8000/api/notifications/1/read/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Mark All Notifications as Read

```bash
curl -X POST http://localhost:8000/api/notifications/mark-all-read/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Password Management

### Request Password Reset

```bash
curl -X POST http://localhost:8000/api/users/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com"
  }'
```

### Confirm Password Reset

```bash
curl -X POST http://localhost:8000/api/users/password-reset/confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "RESET_TOKEN_FROM_EMAIL",
    "new_password": "NewPass123!",
    "new_password_confirm": "NewPass123!"
  }'
```

### Change Password (Authenticated)

```bash
curl -X POST http://localhost:8000/api/users/change-password/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "OldPass123!",
    "new_password": "NewPass123!",
    "new_password_confirm": "NewPass123!"
  }'
```

## Admin Endpoints

### List All Users (Admin Only)

```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### Get User Statistics (Admin Only)

```bash
curl -X GET http://localhost:8000/api/users/statistics/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

## Testing Workflow

### Complete Purchase Flow

1. **Register and Login:**
```bash
# Register
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "buyer1", "email": "buyer@test.com", "password": "Pass123!", "password_confirm": "Pass123!"}'

# Login and save token
TOKEN=$(curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "buyer1", "password": "Pass123!"}' | jq -r '.access')
```

2. **Browse and Add to Cart:**
```bash
# List products
curl -X GET http://localhost:8000/api/shop/products/

# Add to cart
curl -X POST http://localhost:8000/api/carts/items/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

3. **Review Cart and Checkout:**
```bash
# View cart
curl -X GET http://localhost:8000/api/carts/ \
  -H "Authorization: Bearer $TOKEN"

# Validate cart
curl -X GET http://localhost:8000/api/carts/validate/ \
  -H "Authorization: Bearer $TOKEN"

# Create order
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

4. **Review Order:**
```bash
# List orders
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer $TOKEN"
```

## Notes

- Replace `YOUR_ACCESS_TOKEN` with the actual JWT token from login
- Replace `ADMIN_ACCESS_TOKEN` with admin user's token
- All timestamps are in UTC
- Prices are in USD (or configured currency)
- Stock is automatically managed on order creation/cancellation

## Using Postman

Import these examples into Postman:
1. Create a new collection
2. Set up environment variables for `base_url` and `access_token`
3. Add requests from examples above
4. Use `{{base_url}}` and `{{access_token}}` in requests

## Using Python Requests

```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/api/users/token/',
    json={'username': 'admin', 'password': 'admin123'}
)
token = response.json()['access']

# Get products
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(
    'http://localhost:8000/api/shop/products/',
    headers=headers
)
products = response.json()
```
