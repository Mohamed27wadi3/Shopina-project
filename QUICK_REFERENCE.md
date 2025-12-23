# Shopina Platform - Quick Reference Card

## 🚀 START HERE

### 1. Start Backend (Terminal 1)
```bash
cd "d:\Shopina Project\code source\shopina-env\backend"
python manage.py runserver 0.0.0.0:8000
```

### 2. Start Frontend (Terminal 2)
```bash
cd "d:\Shopina Project\code source\front"
npm run dev
```

### 3. Open Application
- **Frontend**: http://localhost:3003
- **Admin**: http://localhost:8000/admin/

---

## 🔑 USER CREDENTIALS (for testing)

### Admin Account
- **Email**: admin@shopina.com
- **Password**: admin123
- **URL**: http://localhost:8000/admin/

**To create admin**:
```bash
python manage.py shell
>>> from users.models import User
>>> User.objects.create_superuser(email='admin@shopina.com', password='admin123')
```

---

## 📍 MAIN ENDPOINTS

| Feature | URL | Method |
|---------|-----|--------|
| Login | `/api/users/login/` | POST |
| Register | `/api/users/signup/` | POST |
| Remember Me | `/api/users/auth/remember-me/` | POST |
| Google OAuth | `/accounts/google/login/` | GET |
| GitHub OAuth | `/accounts/github/login/` | GET |
| Profile | `/api/users/profile/` | GET/PUT |
| Products | `/api/shop/products/` | GET/POST |
| Orders | `/api/orders/` | GET/POST |
| Cart | `/api/carts/` | GET/DELETE |
| Cart Items | `/api/carts/items/` | POST/PATCH/DELETE |
| Reviews | `/api/reviews/` | GET/POST |

---

## 🧪 QUICK TESTS

### Test 1: Basic Login
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### Test 2: Social Login (Google)
1. Go to: http://localhost:3003/login
2. Click "Google" button
3. Sign in with Google account
4. Should redirect to dashboard

### Test 3: Remember Me
1. Go to: http://localhost:3003/login
2. Enter email/password
3. Check "Remember Me (30 days)"
4. Click "Sign In"
5. Tokens persist for 30 days

### Test 4: Create Product
```bash
curl -X POST http://localhost:8000/api/shop/products/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "T-Shirt",
    "price": "29.99",
    "stock": 100
  }'
```

---

## 🎨 STYLING QUICK REFERENCE

### Main Colors
- Primary Blue: `#0077FF`
- Secondary Blue: `#5AC8FA`
- Dark Background: `#0A1A2F`
- Text Light: `white`
- Text Dark: `#0A1A2F`

### Button Classes
```tsx
// Primary
className="bg-[#0077FF] hover:bg-[#0077FF]/90 text-white h-12 rounded-xl"

// Secondary
className="border-2 border-gray-200 hover:border-[#0077FF]/30"
```

### Input Classes
```tsx
className="h-12 rounded-xl border-2 border-gray-200 focus:border-[#0077FF]"
```

---

## 📁 PROJECT STRUCTURE

```
d:\Shopina Project\
├── README.md
├── IMPLEMENTATION_SUMMARY.md
├── CRUD_TESTING_GUIDE.md
├── STYLING_CONSISTENCY_GUIDE.md
├── SOCIAL_AUTH_SETUP.md
├── DEPLOYMENT_CHECKLIST.md
│
├── code source\
│   ├── front\                 # React frontend
│   │   ├── src\
│   │   │   ├── pages\
│   │   │   │   ├── LoginPage.tsx
│   │   │   │   ├── SignupPage.tsx
│   │   │   │   └── DashboardPage.tsx
│   │   │   ├── context\
│   │   │   │   └── AuthContext.tsx
│   │   │   └── styles\
│   │   │       └── globals.css
│   │   └── package.json
│   │
│   └── shopina-env\backend\   # Django backend
│       ├── shopina\
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       ├── users\
│       │   ├── models.py
│       │   ├── social_views.py
│       │   ├── urls.py
│       │   └── views.py
│       ├── shop\
│       │   └── models.py
│       ├── orders\
│       │   └── models.py
│       ├── manage.py
│       ├── requirements.txt
│       └── db.sqlite3
```

---

## 🔐 AUTHENTICATION FLOW

### Email/Password
```
1. User enters email & password
2. Frontend sends to /api/users/login/
3. Backend validates credentials
4. Returns access + refresh tokens
5. Frontend stores in localStorage
6. User redirected to dashboard
```

### Remember Me (30-day)
```
1. User checks "Remember Me"
2. Frontend sends to /api/users/auth/remember-me/
3. Backend validates + extends refresh token to 30 days
4. Returns tokens with extended lifetime
5. Browser closes but tokens persist for 30 days
6. On next visit, app can refresh tokens automatically
```

### Social Login (Google/GitHub)
```
1. User clicks Google/GitHub button
2. Frontend redirects to /accounts/google/login/ or /accounts/github/login/
3. User redirected to OAuth provider
4. User authorizes app
5. Redirects back to /accounts/google/login/callback/ with code
6. Backend exchanges code for tokens
7. User created/updated in database
8. Redirects to dashboard with JWT tokens
```

---

## 🛠️ USEFUL COMMANDS

### Django
```bash
# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Run tests
python manage.py test

# Run server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Shell
python manage.py shell

# Clear cache
python manage.py clear_cache
```

### Frontend
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview build
npm run preview
```

### Git
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push origin main
```

---

## 📊 FILE SIZES (Approximate)

- React Bundle: ~500KB
- Django App: ~50MB (with dependencies)
- Database: ~10MB (initial)
- Media Files: Varies

---

## ⚡ PERFORMANCE TIPS

1. **Frontend**
   - Use React DevTools Profiler
   - Check Network tab for slow requests
   - Enable gzip compression

2. **Backend**
   - Use select_related() for queries
   - Add pagination (default 10-20 items)
   - Enable caching for repeated queries

3. **Database**
   - Add indexes to frequently queried fields
   - Use raw SQL for complex queries
   - Monitor slow queries

---

## 🔗 IMPORTANT LINKS

| Link | Purpose |
|------|---------|
| http://localhost:3003 | Frontend |
| http://localhost:8000 | Backend |
| http://localhost:8000/admin/ | Django Admin |
| http://localhost:8000/api/schema/swagger-ui/ | API Docs |
| https://console.cloud.google.com/ | Google OAuth |
| https://github.com/settings/applications/new | GitHub OAuth |

---

## ❓ FAQ

**Q: How do I reset the database?**
```bash
rm db.sqlite3
python manage.py migrate
```

**Q: How do I add a new user?**
```bash
# Via Django Admin
http://localhost:8000/admin/

# Via API
POST /api/users/signup/
```

**Q: How do I test social login?**
1. Create Google/GitHub OAuth credentials
2. Add to Django Admin
3. Click social button on login page
4. Authorize with Google/GitHub

**Q: What if tokens expire?**
```bash
# Frontend automatically refreshes using refresh token
# If refresh token also expired, user must log in again
```

**Q: Can I use this in production?**
Yes, but:
- Change SECRET_KEY
- Set DEBUG = False
- Use HTTPS
- Configure database (PostgreSQL)
- Set up static file serving
- Configure email
- Set up monitoring

---

## 📞 CONTACT & SUPPORT

For issues or questions:
1. Check documentation files
2. Review console errors
3. Check Django logs
4. Read the code comments
5. Search Stack Overflow

---

**Version**: 1.0.0
**Status**: Production Ready ✅
**Last Updated**: December 23, 2025

