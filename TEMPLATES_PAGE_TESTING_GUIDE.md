# 🧪 Templates Page Testing Guide

## Quick Verification Steps

### 1. Start the Development Server
```bash
cd "d:\Shopina Project\code source\front"
npm run dev
```
Navigate to: **http://localhost:3000/templates**

### 2. Visual Inspection ✅

**Header Section**:
- [ ] Title: "Choisissez votre template"
- [ ] Subtitle: "Sélectionnez et personnalisez un design professionnel..."
- [ ] Sparkles icon with blue-cyan gradient background
- [ ] Search input field with Search icon
- [ ] Category filter buttons visible

**Template Cards**:
- [ ] 6 templates displayed in grid
- [ ] 3 columns on desktop (or responsive on mobile)
- [ ] Each card shows:
  - [ ] Template image
  - [ ] Category badge (top-left)
  - [ ] Title in bold
  - [ ] Description text
  - [ ] Feature count ("• X variantes • Y palettes • Z sections")
  - [ ] Two action buttons (Variantes, Personnaliser)

### 3. Interaction Testing 🎯

**Search Functionality**:
- [ ] Type in search field (e.g., "Fashion")
- [ ] Verify templates filter in real-time
- [ ] Template count updates
- [ ] Clear search to see all templates again

**Category Filtering**:
- [ ] Click "Tous" button → All templates show
- [ ] Click category button (e.g., "Mode") → Only that category shows
- [ ] Button highlight changes to blue gradient
- [ ] Click another category → Switches correctly
- [ ] Count updates correctly

**Card Hover Effects**:
- [ ] Hover over template card
- [ ] Verify:
  - [ ] Shadow increases (card lifts)
  - [ ] Image zooms slightly
  - [ ] Gradient overlay appears on image
  - [ ] Two floating buttons appear:
    - [ ] "Aperçu" (with eye icon)
    - [ ] "Variantes" (with settings icon)

### 4. Preview Modal Testing 📺

**Open Preview**:
- [ ] Hover over card
- [ ] Click "Aperçu" button
- [ ] Modal opens with:
  - [ ] Template name & description
  - [ ] Category badge
  - [ ] Device selector buttons (Monitor/Tablet/Phone)
  - [ ] Mock store preview
  - [ ] "Personnaliser" button
  - [ ] "Fermer" button
  - [ ] X close button (top-right)

**Device Selector**:
- [ ] Click Desktop icon → Full width preview
- [ ] Click Tablet icon → Medium width (max-w-3xl)
- [ ] Click Mobile icon → Narrow width (max-w-sm)
- [ ] All devices show mock store content

**Preview Content**:
- [ ] Shows hero section with template title
- [ ] Shows "Bienvenue sur [Template Name]"
- [ ] Shows "Découvrez notre collection exclusive"
- [ ] "Explorer maintenant" button visible
- [ ] Products grid with 6 mock products
- [ ] Each product shows image placeholder, name, price

**Close Modal**:
- [ ] Click "Fermer" button → Modal closes
- [ ] Click X button → Modal closes
- [ ] Click outside modal → Modal closes
- [ ] Click "Personnaliser" → Goes to customize page AND closes

### 5. Variants Panel Testing 📋

**Open Variants**:
- [ ] Hover over card
- [ ] Click "Variantes" button OR
- [ ] Click "Variantes" button on card itself
- [ ] Right-side sheet slides in from right
- [ ] Shows:
  - [ ] "Variantes - [Template Name]"
  - [ ] "Explorez les différentes variantes..."
  - [ ] Variants section with list

**Variants Display**:
- [ ] Each variant card shows:
  - [ ] Preview image (if available)
  - [ ] Name (bold)
  - [ ] Description
  - [ ] Feature highlights as badges
- [ ] Can scroll through variants

**Customization Options**:
- [ ] "Options de personnalisation" section visible
- [ ] Shows "Palettes colorimétriques" with badges
- [ ] Shows "Sections disponibles" with badges
- [ ] All badges styled consistently

**Action**:
- [ ] "Personnaliser ce template" button at bottom
- [ ] Click button → Navigates to customize page
- [ ] Panel closes automatically

### 6. Empty State Testing 🔍

- [ ] Search for: "xyz123notfound"
- [ ] Verify:
  - [ ] No templates display
  - [ ] Search icon in circle shows
  - [ ] "Aucun template trouvé" message
  - [ ] "Essayez d'ajuster votre recherche..." suggestion
  - [ ] "Tous" button still works to reset

### 7. Navigation Testing 🔗

**From Template Cards**:
- [ ] Click "Personnaliser" button → Goes to `/templates/:id/variants`
- [ ] Verify URL updates
- [ ] Go back to templates → Page reloads correctly

**From Preview Modal**:
- [ ] Open preview
- [ ] Click "Personnaliser" → Goes to customize page
- [ ] Modal closes
- [ ] URL updates to `/templates/:id/customize`

**From Variants Panel**:
- [ ] Open variants panel
- [ ] Click "Personnaliser ce template" → Goes to customize page
- [ ] Panel closes
- [ ] URL updates to `/templates/:id/customize`

### 8. Dark Mode Testing 🌙

- [ ] Open DevTools or use system dark mode
- [ ] Verify:
  - [ ] Background is dark gray (gray-950)
  - [ ] Cards have dark background (gray-800)
  - [ ] Text is white/light gray
  - [ ] All components are readable
  - [ ] Borders are visible in dark mode
  - [ ] Shadows work properly

### 9. Responsive Design Testing 📱

**Desktop (> 1024px)**:
- [ ] 3-column grid
- [ ] Search + filters in one row
- [ ] Full-width layout

**Tablet (768px - 1024px)**:
- [ ] 2-column grid
- [ ] Layout adapts smoothly
- [ ] Buttons still functional

**Mobile (< 768px)**:
- [ ] 1-column grid
- [ ] Search + filters stack vertically
- [ ] Cards take full width
- [ ] Touch-friendly button sizes
- [ ] All text readable

### 10. Performance Testing ⚡

- [ ] Page loads quickly
- [ ] No console errors
- [ ] Smooth animations (no stuttering)
- [ ] Interactions are responsive
- [ ] No memory leaks (check DevTools)

### 11. Browser Compatibility ✓

Test in:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

---

## Expected Results

| Feature | Expected Behavior |
|---------|-------------------|
| Search | Real-time filtering, case-insensitive |
| Categories | Single selection, highlight changes |
| Cards Hover | Smooth animation, buttons appear |
| Preview Modal | Opens/closes smoothly, device selector works |
| Variants Panel | Slides in from right, content displays |
| Navigation | Routes update correctly |
| Empty State | Shows when no results found |
| Dark Mode | Colors adapt, readable in both modes |
| Responsive | Adapts to all screen sizes |

---

## Troubleshooting

### Issue: Cards not showing
- Clear browser cache (Ctrl+Shift+Delete)
- Reload page (F5 or Cmd+R)
- Check DevTools console for errors

### Issue: Modals not opening
- Ensure JavaScript is enabled
- Check browser console for errors
- Try different browser

### Issue: Images not loading
- Check network tab in DevTools
- Verify image URLs are valid
- Clear cache and reload

### Issue: Styling looks wrong
- Check dark mode settings
- Clear browser cache
- Try different screen size

### Issue: Navigation not working
- Check React Router setup in App.tsx
- Verify route paths match (/templates/:id/variants)
- Check browser console for routing errors

---

## Success Checklist ✅

- [ ] All 6 templates visible
- [ ] Search filters templates
- [ ] Categories filter correctly
- [ ] Preview modal opens and closes
- [ ] Device selector works
- [ ] Variants panel opens and closes
- [ ] All buttons navigate correctly
- [ ] Dark mode works
- [ ] Responsive on all screen sizes
- [ ] No console errors
- [ ] Build completes successfully

---

**Status**: Ready for testing  
**Build**: ✅ 1784 modules, 0 errors  
**Last Updated**: 2025-01-15
