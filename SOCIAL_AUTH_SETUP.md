# Social Authentication Setup Guide

## Overview
This guide covers the complete setup for Google and GitHub OAuth integration in Shopina using django-allauth.

## Prerequisites
- Django 5.2.7
- django-allauth 65.13.1 (already installed)
- cryptography library (already installed)
- React frontend running on port 3003
- Django backend running on port 8000

## Step 1: Google OAuth Setup

### 1.1 Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API"
   - Click and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Choose "Web application"
   - Name: "Shopina"
   - Authorized redirect URIs:
     - `http://localhost:3003/accounts/google/login/callback/`
     - `http://localhost:8000/accounts/google/login/callback/`
     - `http://127.0.0.1:8000/accounts/google/login/callback/`
     - (Add your production domain when deployed)
   - Save and copy the Client ID and Client Secret

### 1.2 Add Google Credentials to Django Admin

1. Start Django development server:
   ```bash
   cd "d:\Shopina Project\code source\shopina-env\backend"
   python manage.py runserver 0.0.0.0:8000
   ```

2. Create a superuser (if not exists):
   ```bash
   python manage.py shell
   >>> from users.models import User
   >>> User.objects.create_superuser(email='admin@shopina.com', password='admin123')
   >>> exit()
   ```

3. Access Django Admin:
   - Open browser: `http://localhost:8000/admin/`
   - Login with superuser credentials

4. Add Google OAuth App:
   - Go to "Sites" > Add Site:
     - Domain name: `localhost:3003`
     - Display name: `Shopina`
     - Save
   - Go to "Social Applications" > Add Social Application:
     - Provider: **Google**
     - Name: Google
     - Client ID: (paste from Google Console)
     - Secret key: (paste from Google Console)
     - Sites: Select "localhost:3003"
     - Save

## Step 2: GitHub OAuth Setup

### 2.1 Create GitHub OAuth App

1. Go to [GitHub Settings - Developer Settings - OAuth Apps](https://github.com/settings/applications/new)
2. Fill in the form:
   - **Application name**: Shopina
   - **Homepage URL**: `http://localhost:3003`
   - **Authorization callback URL**: `http://localhost:8000/accounts/github/login/callback/`
   - Click "Register application"
3. Save the Client ID and Client Secret from the app page

### 2.2 Add GitHub Credentials to Django Admin

1. In Django Admin, go to "Social Applications" > Add Social Application:
   - Provider: **GitHub**
   - Name: GitHub
   - Client ID: (paste from GitHub)
   - Secret key: (paste from GitHub)
   - Sites: Select "localhost:3003"
   - Save

## Step 3: Frontend Integration

### 3.1 Social Login Flow

The frontend components have already been updated to include:

**LoginPage.tsx** - Functions for social login:
```typescript
const handleGoogleLogin = () => {
  window.location.href = `${backendUrl}/accounts/google/login/?process=login`;
};

const handleGitHubLogin = () => {
  window.location.href = `${backendUrl}/accounts/github/login/?process=login`;
};
```

**SignupPage.tsx** - Functions for social signup:
```typescript
const handleGoogleSignup = () => {
  window.location.href = `${backendUrl}/accounts/google/login/?process=signup`;
};

const handleGitHubSignup = () => {
  window.location.href = `${backendUrl}/accounts/github/login/?process=signup`;
};
```

### 3.2 Remember Me Feature

The LoginPage now includes a "Remember Me" checkbox that extends the session to 30 days:

```typescript
const handleSubmit = async (e) => {
  if (rememberMe) {
    // Calls /api/users/auth/remember-me/ endpoint
    // Returns tokens with 30-day lifetime
  }
};
```

## Step 4: Testing Social Authentication

### 4.1 Test Google Login

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run dev`
3. Navigate to `http://localhost:3003/login`
4. Click "Google" button
5. Sign in with Google account
6. Verify redirect back to dashboard
7. Check localStorage for tokens

### 4.2 Test GitHub Login

1. Navigate to `http://localhost:3003/login`
2. Click "GitHub" button
3. Authorize the application
4. Verify redirect back to dashboard
5. Check localStorage for tokens

### 4.3 Test Remember Me

1. Navigate to `http://localhost:3003/login`
2. Enter credentials
3. Check "Remember Me (30 days)" checkbox
4. Click "Sign In"
5. Verify tokens are stored in localStorage
6. Close browser and reopen later to test persistence

## Step 5: Backend API Endpoints

### Remember Me Login
```bash
POST /api/users/auth/remember-me/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "remember": true
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

Note: The refresh token has a 30-day lifetime instead of the default 7 days.

### Social Login Endpoints

The social login flow is handled by allauth's built-in endpoints:
- `/accounts/google/login/`
- `/accounts/google/login/callback/`
- `/accounts/github/login/`
- `/accounts/github/login/callback/`

## Step 6: Environment Configuration

### Django Settings (Already Configured)

The following settings have been configured in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
        ],
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    # ... other settings
}
```

## Step 7: Production Deployment

### 7.1 Environment Variables

Create a `.env` file:
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 7.2 Update Redirect URIs

For production domain (e.g., `shopina.com`):

**Google Console:**
- Add redirect URIs:
  - `https://shopina.com/accounts/google/login/callback/`

**GitHub Settings:**
- Change authorization callback URL to:
  - `https://shopina.com/accounts/github/login/callback/`

**Django Admin:**
- Create new Site with your domain
- Update Social Applications to use the production site

### 7.3 Enable HTTPS

Ensure your production domain uses HTTPS. Update:
```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Troubleshooting

### Issue: "Redirect URI mismatch"
**Solution**: Verify redirect URIs exactly match in OAuth provider settings (case-sensitive)

### Issue: "Invalid Client ID"
**Solution**: Check that Client ID and Secret are correctly copied without spaces

### Issue: "allauth middleware not found"
**Solution**: Ensure `allauth.account.middleware.AccountMiddleware` is in MIDDLEWARE list

### Issue: "Site matching query does not exist"
**Solution**: Go to Django Admin > Sites and ensure SITE_ID = 1 exists

### Issue: Social buttons not working
**Solution**: 
1. Check browser console for errors
2. Verify backend is running on port 8000
3. Check CORS settings include frontend origin

### Issue: Tokens not stored after login
**Solution**: 
1. Check browser localStorage is enabled
2. Verify AuthContext.tsx is importing tokens correctly
3. Check network tab for successful token response

## Testing Checklist

- [ ] Google OAuth credentials created
- [ ] GitHub OAuth credentials created
- [ ] Django Social Applications configured
- [ ] Sites table has correct domain
- [ ] Google login works on frontend
- [ ] GitHub login works on frontend
- [ ] Remember Me checkbox stores 30-day tokens
- [ ] Tokens persist in localStorage
- [ ] Dashboard accessible after social login
- [ ] Social buttons redirect correctly
- [ ] Logout clears tokens properly
- [ ] Error messages display appropriately

## Next Steps

1. **Test all CRUD operations** - See [CRUD_TESTING_GUIDE.md](./CRUD_TESTING_GUIDE.md)
2. **Verify styling consistency** - See [STYLING_CONSISTENCY_GUIDE.md](./STYLING_CONSISTENCY_GUIDE.md)
3. **Load testing** - Run performance tests on endpoints
4. **Security audit** - Review CORS, CSRF, and token handling
5. **User testing** - Test with real users across different browsers
6. **Deployment** - Follow production deployment checklist

## Additional Resources

- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
