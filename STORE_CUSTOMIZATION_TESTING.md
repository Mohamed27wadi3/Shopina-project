# Store Customization - Quick Testing Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Backend running: `python manage.py runserver`
- Frontend running: `npm run dev`
- Logged-in user with a shop

---

## ✅ Test 1: Access Customization Page

```
1. Login to dashboard
2. Look for "Customize Store" button (or navigate to /customize)
3. Should see form with:
   ✓ Color inputs (5 colors)
   ✓ Font dropdown
   ✓ Logo uploader
   ✓ Border radius selector
   ✓ Shadow style selector
   ✓ Live preview panel
```

**Expected:** Page loads with form fields and live preview

---

## ✅ Test 2: Color Customization

```
1. Click primary color picker
2. Change to red (#FF0000)
3. Watch live preview - buttons should turn red
4. Type hex value directly: #00FF00 (green)
5. Live preview updates instantly
6. Repeat for other colors (secondary, accent, background, text)
```

**Expected:** Colors update in real-time in preview

---

## ✅ Test 3: Font Selection

```
1. Open "Primary Font" dropdown
2. Select "Poppins"
3. Watch live preview - text font changes
4. Try other fonts (Roboto, Ubuntu, etc.)
5. Notice font loads from Google Fonts
```

**Expected:** Font dropdown changes preview text appearance

---

## ✅ Test 4: Logo Upload

```
1. Click "Choose File" button
2. Select PNG or JPG image (any size)
3. Watch preview box - logo appears
4. Can see in preview panel at top
5. Click "Save Changes" to persist
```

**Expected:** Logo preview shows immediately, saves to DB

---

## ✅ Test 5: Live Preview Panel

```
1. Change primary color to #FF0000
2. Watch right panel - preview updates
3. See:
   ✓ Logo preview at top
   ✓ Store name (with custom name if set)
   ✓ Primary button (red)
   ✓ Secondary button
   ✓ Accent element (yellow)
   ✓ Text sample
   ✓ Color swatches at bottom
```

**Expected:** Real-time preview of all changes

---

## ✅ Test 6: Save Customization

```
1. Change all customization settings
2. Click "Save Changes" button
3. See loading spinner
4. Success toast message appears
5. Page reloads
6. Verify settings persisted (should still see your changes)
```

**Expected:** Changes saved and persist across page reloads

---

## ✅ Test 7: API Verification (DevTools)

### Open Browser DevTools → Network tab

#### Test GET customization
```
Method: GET
URL: /api/shop/customization/
Status: 200 OK
Response includes: primary_color, secondary_color, etc.
```

#### Test PUT customization
```
Method: PUT
URL: /api/shop/customization/
Headers: Authorization: Bearer <token>
Status: 200 OK
Response: Updated data with new colors/fonts
```

---

## ✅ Test 8: Public Shop Theme Application

```
1. Get your shop slug (e.g., "my-shop")
2. Customize colors (set primary to red, secondary to green)
3. Save customization
4. Visit http://localhost:3000/shop/my-shop
5. Verify:
   ✓ Hero section background = red → green gradient
   ✓ Category buttons use custom colors
   ✓ Add to cart button = primary color (red)
   ✓ Logo shows if uploaded
```

**Expected:** Public shop displays with custom theme colors

---

## ✅ Test 9: Public Customization API

```bash
# In terminal, test public endpoint
curl http://localhost:8000/api/shop/public/my-shop/customization/

# Expected response (no auth required):
{
  "id": 1,
  "primary_color": "#FF0000",
  "secondary_color": "#00FF00",
  "accent_color": "#FFD43B",
  "background_color": "#FFFFFF",
  "text_color": "#0A1A2F",
  "primary_font": "poppins",
  "logo": "http://...",
  "colors": { ... },
  "theme": { ... }
}
```

**Expected:** Returns customization without authentication

---

## ✅ Test 10: Reset to Defaults

```
1. Change all settings to custom values
2. Click "Reset" button
3. Confirm dialog (if shown)
4. All fields return to defaults:
   ✓ Primary: #0077FF (blue)
   ✓ Secondary: #5AC8FA (sky)
   ✓ Font: inter
   ✓ Logo: cleared
```

**Expected:** All defaults restored

---

## ✅ Test 11: Dark Mode Support

```
1. Toggle dark mode (if available)
2. CustomizePage should:
   ✓ Have dark backgrounds
   ✓ Have light text
   ✓ Maintain all functionality
   ✓ Preview panel visible
```

**Expected:** Dark mode works correctly

---

## ✅ Test 12: Responsive Design

```
1. Test on mobile (375px width)
   - Form should stack vertically
   - Live preview hidden or smaller
   - All inputs accessible

2. Test on tablet (768px width)
   - Two columns visible
   - Form + preview side by side

3. Test on desktop (1440px)
   - Full layout with preview on right
```

**Expected:** Responsive layout works at all breakpoints

---

## 🔍 Troubleshooting

### Issue: CustomizePage doesn't load

**Solution:**
```bash
# Check console for errors
# Verify token in localStorage: localStorage.access_token
# Check network tab: Should see /api/shop/customization/
# Verify backend running: python manage.py runserver
```

### Issue: Colors don't update in preview

**Solution:**
```
1. Clear browser cache
2. Reload page (Ctrl+Shift+R)
3. Check console for errors
4. Verify state changes: DevTools → Console
   const state = document.querySelector('[data-customization]')
```

### Issue: Logo not uploading

**Solution:**
```
1. Check file size (should be < 5MB)
2. Verify file type (PNG or JPG)
3. Check browser console for upload errors
4. Verify backend file upload working:
   python manage.py test shop.tests
```

### Issue: Theme doesn't apply to public shop

**Solution:**
```
1. Verify customization was saved: Check DB
2. Visit public shop: /shop/my-shop
3. Check DevTools → Network → /api/shop/public/.../customization/
4. Verify response contains colors
5. Check console for CSS injection errors
```

---

## 📊 Test Results Template

```
Date: _______________
Tester: _______________

✓ Test 1: Page Access ___
✓ Test 2: Colors ___
✓ Test 3: Fonts ___
✓ Test 4: Logo Upload ___
✓ Test 5: Live Preview ___
✓ Test 6: Save ___
✓ Test 7: API ___
✓ Test 8: Public Theme ___
✓ Test 9: Public API ___
✓ Test 10: Reset ___
✓ Test 11: Dark Mode ___
✓ Test 12: Responsive ___

Issues Found:
1. _______________
2. _______________

Status: [ ] PASS [ ] FAIL [ ] PARTIAL
```

---

## 🎯 Advanced Testing

### Test Concurrent Users
```
1. Login as User A, customize with red colors
2. Open incognito: Login as User B, customize with blue
3. Check /shop/user-a-shop → Red theme
4. Check /shop/user-b-shop → Blue theme
Verify: Independent customizations
```

### Test Logo Edge Cases
```
1. Upload very large image (5MB)
2. Upload various formats (PNG, JPG, GIF)
3. Upload with special characters in filename
4. Upload multiple times (should replace)
Verify: All handled gracefully
```

### Test Color Validation
```
1. Try invalid hex: "invalid" → Should show error
2. Try hex without #: "FF0000" → Should handle or show error
3. Try partial hex: "#FF00" → Should show error
4. Try valid hex: "#FF0000" → Should accept
```

### Test Performance
```
1. Open CustomizePage → Measure load time
2. Change color → Measure preview update time
3. Upload logo → Measure upload time
4. Save → Measure save time
Expected: All under 2 seconds
```

---

## 🚀 Full Integration Test

```
1. LOGIN
   - Signup or login to dashboard
   - Verify user has shop

2. CUSTOMIZE
   - Navigate to /customize
   - Change all settings
   - Save customization
   - Verify saved in DB

3. VIEW PUBLIC SHOP
   - Visit /shop/{slug}
   - Verify custom theme applied
   - Check logo, colors, fonts

4. VERIFY API
   - Call /api/shop/customization/ → Shows saved data
   - Call /api/shop/public/{slug}/customization/ → Shows data

5. PERSISTENCE
   - Refresh shop page → Theme still applied
   - Close browser, reopen → Theme still there
   - Visit from different browser → Theme visible

6. MULTIPLE SHOPS
   - Create second shop
   - Customize differently
   - Verify each shop has own theme
```

**Expected Result:** ✅ PASS - All tests successful

---

## ✅ Sign-off Checklist

Before deployment:

- [ ] All 12 tests pass
- [ ] No console errors
- [ ] No network errors
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] API endpoints accessible
- [ ] Authentication working
- [ ] Images uploading
- [ ] Live preview updating
- [ ] Save functionality working
- [ ] Public shops displaying theme
- [ ] Dark mode working
- [ ] Responsive design verified
- [ ] Permissions enforced
- [ ] Documentation complete

---

**Ready for Production:** When all tests pass ✅

