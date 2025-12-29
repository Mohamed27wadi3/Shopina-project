import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopina.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

# Get a user
user = User.objects.first()
print(f"Testing with user: {user.username}")

# Create test client
client = Client()
client.force_login(user)

# Test order detail page
response = client.get('/orders/10/')
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    print(f"Content length: {len(content)} bytes")
    
    # Check if key elements are present
    if 'Commande #10' in content:
        print("✓ Order title found")
    else:
        print("✗ Order title NOT found")
    
    if 'iphone' in content.lower():
        print("✓ Product name found")
    else:
        print("✗ Product name NOT found")
        
    if '92000' in content or '92,000' in content:
        print("✓ Price found")
    else:
        print("✗ Price NOT found")
        
    # Print a snippet
    print("\n--- Content snippet (first 2000 chars) ---")
    print(content[:2000])
else:
    print(f"Error: {response.status_code}")
    print(response.content[:1000])
