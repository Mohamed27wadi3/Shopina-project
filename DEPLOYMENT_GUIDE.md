# 🚀 Guide de Déploiement - Shopina 3D System

## ⚡ Quick Start

### 1. **Vérifier l'Installation**
```bash
# Navigate to project root
cd "d:\Shopina Project"

# Run verification script
python verify_system.py

# Expected: ✅ All checks passed
```

### 2. **Démarrer le Serveur Django**
```bash
cd "code source/shopina-env/backend"

# Activate environment
shopina-env\Scripts\activate

# Run server
python manage.py runserver 8000

# Check: http://localhost:8000/dashboard/ ✅
```

### 3. **Tester les Routes**

**Dashboard:**
```
http://localhost:8000/dashboard/          ✅
```

**Orders:**
```
http://localhost:8000/orders/             ✅
```

**Settings (NEW):**
```
http://localhost:8000/profile-settings/   ✅
```

---

## 📋 Pre-Deployment Checklist

### Frontend
- [ ] Dashboard loads without errors
- [ ] Orders page displays correctly
- [ ] Settings page shows forms
- [ ] Theme toggle works
- [ ] Avatar dropdown opens/closes
- [ ] Responsive design works on mobile
- [ ] No console errors (F12)
- [ ] All links functional
- [ ] Images load correctly
- [ ] Animations smooth

### Backend
- [ ] Django DEBUG = False (production)
- [ ] ALLOWED_HOSTS configured
- [ ] STATIC_FILES collected
- [ ] Database migrations complete
- [ ] CSRF middleware enabled
- [ ] Security headers configured
- [ ] Email backend configured
- [ ] Session timeout set
- [ ] Logging configured
- [ ] Error pages (404, 500) custom

### APIs (To implement)
- [ ] POST /api/users/change-password/
- [ ] POST /api/users/profile/
- [ ] Error handling implemented
- [ ] Rate limiting configured
- [ ] CORS headers set
- [ ] Request validation complete

### Security
- [ ] HTTPS enabled
- [ ] CSRF tokens working
- [ ] No sensitive data in logs
- [ ] Password validation strong
- [ ] SQL injection protected
- [ ] XSS protection enabled
- [ ] CORS properly configured
- [ ] Session secure (HTTPS only)
- [ ] HSTS headers set
- [ ] Clickjacking protection

### Performance
- [ ] CSS minified
- [ ] JavaScript minified
- [ ] Images optimized
- [ ] Caching configured
- [ ] Database queries optimized
- [ ] Static files served from CDN
- [ ] Compression enabled (gzip)
- [ ] Load time < 3s
- [ ] Lighthouse score > 80
- [ ] Mobile performance good

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Cross-browser tested
- [ ] Mobile tested
- [ ] Accessibility tested
- [ ] Performance tested
- [ ] Security tested
- [ ] Load tested

---

## 🔧 Production Configuration

### settings.py
```python
# SECURITY
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),
    'style-src': ("'self'", "'unsafe-inline'", "fonts.googleapis.com"),
}

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopina_prod',
        'USER': 'shopina_user',
        'PASSWORD': 'secure_password',
        'HOST': 'db.example.com',
        'PORT': '5432',
    }
}

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/shopina/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/shopina/media/'

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/shopina/django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}

# CACHING
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'app_password'
```

---

## 🐳 Docker Deployment (Optional)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run server
CMD ["gunicorn", "shopina.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=localhost,127.0.0.1
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=shopina_prod
      - POSTGRES_USER=shopina_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7

volumes:
  postgres_data:
```

---

## 📱 Static Files Collection

```bash
# Collect all static files
python manage.py collectstatic --noinput --clear

# Verify collection
ls -la /path/to/static/

# Expected:
# ✅ /static/admin/
# ✅ /static/css/
# ✅ /static/js/
# ✅ /static/images/
```

---

## 🗄️ Database Migration

```bash
# Check migration status
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Load sample data (if needed)
python manage.py loaddata fixtures/initial_data.json
```

---

## 🧪 Pre-Production Tests

```bash
# Run tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report

# Check for security issues
python -m bandit -r .

# Check for code quality
python -m flake8 .

# Check for type issues (if using mypy)
mypy .
```

---

## 🔍 Post-Deployment Verification

### Check Django
```bash
# Check admin access
curl -u admin:password http://localhost:8000/admin/

# Check API endpoint
curl http://localhost:8000/api/docs/

# Check static files
curl http://localhost:8000/static/css/style.css
```

### Check Logs
```bash
# View Django logs
tail -f /var/log/shopina/django.log

# View system logs
sudo journalctl -u shopina -f
```

### Monitor Performance
```bash
# Check uptime
uptime

# Check memory usage
free -h

# Check disk usage
df -h

# Check CPU usage
top -b -n 1 | head -20
```

---

## 🚨 Troubleshooting

### Issue: Dashboard not loading
**Solution:**
```bash
# Check Django is running
ps aux | grep django

# Check port is open
netstat -tuln | grep 8000

# Check logs
python manage.py runserver 8000 --verbosity 3
```

### Issue: Theme not persisting
**Solution:**
```javascript
// Check localStorage
console.log(localStorage.getItem('theme'))

// Clear and reset
localStorage.clear()
location.reload()
```

### Issue: Avatar dropdown not working
**Solution:**
```javascript
// Check element exists
console.log(document.getElementById('profileDropdown'))

// Check event listeners
document.addEventListener('click', console.log)
```

### Issue: Static files not loading
**Solution:**
```bash
# Collect static files again
python manage.py collectstatic --noinput --clear --verbosity 3

# Check Django DEBUG setting
grep DEBUG settings.py

# Check STATIC_URL and STATIC_ROOT
grep STATIC settings.py
```

### Issue: Database connection error
**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -h localhost -U shopina_user -d shopina_prod

# Check migrations
python manage.py showmigrations | grep '[X]'
```

---

## 📊 Monitoring & Maintenance

### Daily Checks
- [ ] Server uptime
- [ ] Error logs
- [ ] Database size
- [ ] Disk space
- [ ] Memory usage

### Weekly Checks
- [ ] User activity
- [ ] Performance metrics
- [ ] Security updates
- [ ] Backup verification
- [ ] SSL certificate status

### Monthly Checks
- [ ] Database optimization
- [ ] Old logs cleanup
- [ ] Security audit
- [ ] Performance review
- [ ] User feedback

### Quarterly Checks
- [ ] Code review
- [ ] Security testing
- [ ] Load testing
- [ ] Disaster recovery test
- [ ] Team knowledge update

---

## 🔐 Backup & Recovery

### Backup Strategy
```bash
# Daily database backup
0 2 * * * pg_dump shopina_prod | gzip > /backups/db_$(date +\%Y\%m\%d).sql.gz

# Weekly full backup
0 3 * * 0 tar -czf /backups/full_$(date +\%Y\%m\%d).tar.gz /var/www/shopina/

# Retention: Keep last 30 days
find /backups -name "*.sql.gz" -mtime +30 -delete
```

### Recovery Procedure
```bash
# Restore database
gunzip < /backups/db_20240101.sql.gz | psql shopina_prod

# Restore files
tar -xzf /backups/full_20240101.tar.gz -C /

# Restart services
sudo systemctl restart shopina
```

---

## 📞 Support & SLA

**Response Time:**
- Critical: 1 hour
- High: 4 hours
- Medium: 24 hours
- Low: 48 hours

**Availability Target:**
- Production: 99.9% (8.76 hours downtime/year)
- Staging: 99.0% (87.6 hours downtime/year)

---

## 📚 Documentation

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Security Documentation](./SYSTEM_IMPROVEMENTS_COMPLETE.md)
- [Testing Guide](./TESTING_GUIDE_3D_SYSTEM.md)
- [Modifications Summary](./MODIFICATIONS_SUMMARY.md)

---

**Last Updated:** 2024  
**Status:** Ready for Production  
**Version:** 1.0.0
