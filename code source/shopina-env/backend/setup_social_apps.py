"""
Script to setup social applications for OAuth providers.
Run with: python manage.py shell < setup_social_apps.py

You'll need to configure:
1. Google OAuth App: https://console.cloud.google.com/
2. GitHub OAuth App: https://github.com/settings/applications/new

Then update the CLIENT_ID and CLIENT_SECRET values below.
"""

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Update SITE_ID if needed
site = Site.objects.get_or_create(
    pk=1,
    defaults={
        'domain': 'localhost:3003',
        'name': 'Shopina'
    }
)[0]

# Google OAuth2 Configuration
# Get credentials from: https://console.cloud.google.com/
google_app, created = SocialApp.objects.get_or_create(
    provider='google',
    defaults={
        'name': 'Google',
        'client_id': 'YOUR_GOOGLE_CLIENT_ID',  # Replace with your Google Client ID
        'secret': 'YOUR_GOOGLE_CLIENT_SECRET',  # Replace with your Google Client Secret
    }
)
if created:
    google_app.sites.add(site)
    print("✓ Google OAuth app created (update CLIENT_ID and CLIENT_SECRET)")
else:
    print("✓ Google OAuth app already exists")

# GitHub OAuth2 Configuration
# Get credentials from: https://github.com/settings/applications/new
github_app, created = SocialApp.objects.get_or_create(
    provider='github',
    defaults={
        'name': 'GitHub',
        'client_id': 'YOUR_GITHUB_CLIENT_ID',  # Replace with your GitHub Client ID
        'secret': 'YOUR_GITHUB_CLIENT_SECRET',  # Replace with your GitHub Client Secret
    }
)
if created:
    github_app.sites.add(site)
    print("✓ GitHub OAuth app created (update CLIENT_ID and CLIENT_SECRET)")
else:
    print("✓ GitHub OAuth app already exists")

print("\n" + "="*60)
print("NEXT STEPS:")
print("="*60)
print("1. Create Google OAuth2 Credentials:")
print("   - Go to: https://console.cloud.google.com/")
print("   - Create a new OAuth 2.0 Client ID (Web Application)")
print("   - Add Authorized redirect URIs:")
print("     * http://localhost:3003/accounts/google/login/callback/")
print("     * http://localhost:3000/accounts/google/login/callback/")
print("   - Get Client ID and Client Secret")
print()
print("2. Create GitHub OAuth App:")
print("   - Go to: https://github.com/settings/applications/new")
print("   - Fill in:")
print("     * Application name: Shopina")
print("     * Homepage URL: http://localhost:3003")
print("     * Authorization callback URL:")
print("       http://localhost:3003/accounts/github/login/callback/")
print("   - Get Client ID and Client Secret")
print()
print("3. Update credentials in Django Admin:")
print("   - Go to: http://localhost:8000/admin/")
print("   - Update Google and GitHub app credentials")
print("="*60)
