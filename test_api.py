#!/usr/bin/env python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test token endpoint
print("Testing /api/users/token/ endpoint...")
response = requests.post(
    f"{BASE_URL}/api/users/token/",
    json={"identifier": "mohamed", "password": "mohamed@2004"},
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Body: {response.text}")

if response.status_code == 200:
    data = response.json()
    print("\nParsed JSON:")
    print(json.dumps(data, indent=2))
    if 'access' in data:
        print(f"\n✅ Access token generated: {data['access'][:50]}...")
else:
    print(f"\n❌ Error: {response.status_code}")
    try:
        print("Error details:", json.dumps(response.json(), indent=2))
    except:
        print("Could not parse error response")
