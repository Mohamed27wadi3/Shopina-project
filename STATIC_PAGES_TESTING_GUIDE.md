# Static Pages Integration - Quick Testing Guide

## 🚀 Quick Start Testing

### Prerequisites
1. Backend running: `python manage.py runserver` (from backend folder)
2. Frontend running: `npm run dev` (from front folder)
3. Access: http://localhost:3000

---

## 🧪 Test Scenarios

### Scenario 1: Guest User (Not Logged In)

#### Hero Section
```
✓ Open http://localhost:3000/
✓ Verify: Email input + "Commencer gratuitement" button shown
✓ Click button → Should navigate to /signup
✓ Email input should be reactive (onChange handler working)
```

#### CTA Section
```
✓ Scroll down to CTA section
✓ Verify: Headline says "Prêt à lancer ta boutique ?"
✓ Verify: Two buttons: "Créer ma boutique maintenant" + "S'inscrire"
✓ Click "Créer ma boutique maintenant" → Navigate to /templates
✓ Click "S'inscrire" → Navigate to /signup
✓ Verify: Message says "Rejoignez des milliers d'entrepreneurs..."
```

#### Shop/Boutique Page
```
✓ Navigate to /shop/{slug} or public shop URL
✓ Verify: Products load from API (should see real products)
✓ Search: Type in search box → Results filter in real-time
✓ Categories: Click category button → Products filter correctly
✓ Add to Cart: Click "Ajouter au panier" 
   - Should open ProductDetailModal
   - Select quantity and confirm
   - Toast notification should appear
   - Product stored in localStorage (guest_cart)
✓ Check cart: Open browser DevTools → Application → localStorage
   - Key: "guest_cart"
   - Value: Array of {product_id, quantity, price}
```

#### Templates Page
```
✓ Navigate to /templates
✓ Verify: Template grid shows all templates
✓ Search: Type search term → Templates filter
✓ Category: Click category → Templates filter
✓ "Choisir" button on any template → Navigate to customize page
✓ All templates are real (no dummy data)
```

---

### Scenario 2: Authenticated User (Logged In)

#### Setup
```bash
# Option A: Use existing account
- Open http://localhost:3000/login
- Enter test credentials
- Should redirect to dashboard

# Option B: Create new account
- Open http://localhost:3000/signup
- Fill form + submit
- Should redirect to dashboard
- Check browser DevTools → Application → localStorage
  - Key: "access_token" should exist
  - Key: "user" should have shop_name
```

#### Hero Section (Authenticated)
```
✓ After login, visit http://localhost:3000/
✓ Verify: Email input HIDDEN
✓ Verify: Two buttons shown: "Créer une boutique" + "Accéder au tableau de bord"
✓ Click "Créer une boutique" → Navigate to /templates
✓ Click "Accéder au tableau de bord" → Navigate to /dashboard
✓ Verify: All buttons functional and navigate correctly
```

#### CTA Section (Authenticated)
```
✓ Scroll down to CTA section
✓ Verify: Headline shows "{{user.shop_name}}, prêt à augmenter tes ventes ?"
   - Replace {{user.shop_name}} with actual shop name from account
✓ Verify: Two buttons: "Choisir un template" + "Tableau de bord"
✓ Click "Choisir un template" → Navigate to /templates
✓ Click "Tableau de bord" → Navigate to /dashboard
✓ Verify: Message says "Explore nos templates, personnalise ta boutique..."
```

#### Shop/Boutique Page (Authenticated)
```
✓ Navigate to /shop/{slug}
✓ Verify: Products load from API
✓ Add to Cart: Click "Ajouter au panier"
   - Should open ProductDetailModal
   - Select quantity and confirm
   - Toast notification: "✅ Product added to cart"
   - Check Network tab: POST /api/carts/items/
   - Status: 201 (Created) or 200 (OK)
✓ Check cart backend:
   - Navigate to /checkout
   - Cart items should appear (from backend)
   - Should match items added while authenticated
```

#### Templates Page (Authenticated)
```
✓ Navigate to /templates
✓ Click "Choisir un template" on any template
✓ Should navigate to /templates/{id}/customize
✓ Verify: Customize page loads with template preview
✓ Test customization form (verify it works)
```

---

## 🔍 API Testing

### Check if Hero Component Works
**DevTools → Console:**
```javascript
// Should print user data
const {user} = useAuth();
console.log(user);
// Output: {id, email, shop_name, plan, ...}
```

### Check if APIs are Called
**DevTools → Network tab:**

1. **Shop Page Load**
   - Filter: XHR/Fetch
   - Should see: GET /api/shop/categories/ → 200
   - Should see: GET /api/shop/products/ → 200
   - Response should contain real product data

2. **Add to Cart (Guest)**
   - No network call (stored in localStorage)
   - Check: localStorage.guest_cart

3. **Add to Cart (Authenticated)**
   - Should see: POST /api/carts/items/ → 201
   - Payload: {product_id, quantity}
   - Response: {id, product, quantity, ...}

4. **User Profile**
   - On app load, should see: GET /api/users/profile/ → 200
   - Contains: id, email, shop_name, plan, etc.

---

## 🎨 Design Verification

### Visual Elements
```
✓ Hero section: Email input styled correctly
✓ CTA section: Headline font size and weight match design
✓ Buttons: Colors, shadows, hover effects working
✓ Responsive: Mobile view (375px), Tablet (768px), Desktop (1440px)
✓ Dark mode: Toggle dark mode, verify colors adapt
✓ Animations: Smooth transitions, no janky effects
```

### Theme Customization (ShopPage)
```
✓ Shop hero section: Uses theme colors from API
✓ Category buttons: Highlight color matches theme
✓ Add to cart button: Gradient matches theme primary color
✓ Search bar: Border color matches theme
```

---

## 🐛 Common Issues & Solutions

### Issue: Hero shows email form even when logged in
**Solution:**
```javascript
// Check if token exists
console.log(localStorage.getItem('access_token'));
// Check if useAuth hook working
const {isAuthenticated} = useAuth();
console.log(isAuthenticated);
```

### Issue: Shop products not loading
**Solution:**
- Check Network tab: GET /api/shop/products/ should return 200
- Check Response: Should contain array of products
- If 401/403: Token may be expired, try logout/login

### Issue: Cart not working after adding product
**Solution:**
- If authenticated: Check Network → POST /api/carts/items/ status
- If guest: Check localStorage → key should be "guest_cart"
- Check console for errors

### Issue: CTA doesn't show shop name
**Solution:**
```javascript
// Check user object
const {user} = useAuth();
console.log(user?.shop_name);
// Should print actual shop name, not undefined
```

---

## 📊 Verification Checklist

- [ ] Hero shows different UI for authenticated vs. guest users
- [ ] CTA personalizes headline with user's shop_name (when logged in)
- [ ] Shop page fetches real products from `/api/shop/products/`
- [ ] Add to cart works (backend API for auth, localStorage for guest)
- [ ] Navigation works: All buttons navigate to correct routes
- [ ] No dummy data visible anywhere
- [ ] Design matches original (no CSS changes)
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Dark mode toggles without breaking anything
- [ ] Animations are smooth
- [ ] API calls show correct endpoints in DevTools
- [ ] Tokens are managed correctly (localStorage, refresh)
- [ ] Email input in Hero works (state changes on type)
- [ ] Category filtering in Shop works
- [ ] Search in Shop and Templates works
- [ ] Product stock indicators show correctly
- [ ] Toast notifications appear for cart actions

---

## 🚀 Performance Testing

### Load Times
```
✓ Hero page: < 2 seconds initial load
✓ Shop page: < 3 seconds (loading products from API)
✓ Templates page: < 2 seconds
✓ CTA section: < 1 second
```

### API Calls
```
✓ HomePage:
  - GET /api/users/profile/ (once on app load)
  - GET /api/shop/categories/ (optional)
  - GET /api/shop/products/ (optional)

✓ ShopPage:
  - GET /api/shop/categories/ (on mount)
  - GET /api/shop/products/ (on mount)
  - POST /api/carts/items/ (on cart add)

✓ TemplatesPage:
  - No API calls (uses local data)
```

---

## 🔐 Security Testing

### Authentication
```
✓ Token stored in localStorage (not exposed in HTML)
✓ Token sent in Authorization header: "Bearer {token}"
✓ Credentials: include in fetch calls
✓ Token refreshed: Every 50 minutes automatically
✓ Invalid token: Redirects to login page
```

### Data Protection
```
✓ User email: Only shown to user (not logged in view)
✓ User profile: Protected behind /api/users/profile/ auth
✓ Cart: Uses credentials to ensure user owns cart items
✓ Admin/seller features: Not visible to guest users
```

---

## 📝 Testing Notes

### For Each Test Session
1. **Clear localStorage before testing guest flow**
   ```javascript
   localStorage.clear();
   ```

2. **Clear localStorage before testing auth flow**
   ```javascript
   localStorage.removeItem('access_token');
   localStorage.removeItem('user');
   ```

3. **Check Network tab is open**
   - DevTools → Network
   - Filter by "XHR" or "Fetch"
   - Watch for API calls

4. **Check Console for errors**
   - DevTools → Console
   - No red errors should appear
   - Warnings are OK

---

## ✅ Test Results Template

```
Date: _______________
Tester: _______________
Browser: Chrome / Firefox / Safari
OS: Windows / Mac / Linux

### Guest Flow
- [ ] Hero email form visible
- [ ] CTA shows signup messaging
- [ ] Shop products load
- [ ] Add to cart works
- [ ] Navigation correct

### Auth Flow
- [ ] Hero shows dashboard button
- [ ] CTA shows personalized headline
- [ ] All buttons navigate correctly
- [ ] Cart uses backend API
- [ ] Templates page customization works

### Design
- [ ] No CSS changes from original
- [ ] Responsive on mobile (375px)
- [ ] Responsive on tablet (768px)
- [ ] Responsive on desktop (1440px)
- [ ] Dark mode works

### API
- [ ] Correct endpoints called
- [ ] 200/201 status codes
- [ ] No 401/403 errors
- [ ] Response data correct

### Issues Found:
1. _______________
2. _______________
3. _______________

Status: [ ] PASS / [ ] FAIL / [ ] NEEDS FIXES
```

---

*Last Updated: 2024*
*Test Framework: Manual Browser Testing*
*Tools: Browser DevTools, Postman (optional)*
