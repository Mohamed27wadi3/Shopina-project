# 🚀 Templates Page - Quick Reference Card

## 📍 Location
- **File**: `src/pages/TemplatesPage.tsx`
- **Route**: `/templates`
- **Related Routes**:
  - `/templates/:id/variants` - Customize page
  - `/templates/:id/customize` - Advanced customize
  - `/templates/:id/customize-advanced` - Extended options

---

## 🎯 Key Features

| Feature | Shortcut | Behavior |
|---------|----------|----------|
| **Search** | Type in search field | Real-time filtering of templates |
| **Category Filter** | Click category button | Filter by single category |
| **Clear Filter** | Click "Tous" | Show all templates |
| **Preview** | Hover → Click "Aperçu" | Open full preview modal |
| **Device Switch** | Desktop/Tablet/Mobile icons | Change preview size |
| **View Variants** | Hover → Click "Variantes" | Open variants side panel |
| **Customize** | Click "Personnaliser" button | Go to customize page |
| **Close Modal** | Click X or "Fermer" | Close preview modal |
| **Close Panel** | Click outside or back button | Close variants panel |

---

## 🎨 Color Reference

```
Primary Blue:     #0077FF
Accent Cyan:      #5AC8FA
Dark Background:  #0A1A2F
Light Gray:       #F3F4F6 (gray-50)
Dark Gray:        #1F2937 (gray-900)
```

---

## 📱 Responsive Breakpoints

```
Mobile:    < 768px   → 1 column grid
Tablet:    768px+    → 2 column grid
Desktop:   1024px+   → 3 column grid
```

---

## 🔧 State Variables

```typescript
searchQuery: string                    // Search input value
selectedCategory: string | null        // Active category filter
variantsPanelOpen: boolean            // Variants panel visibility
livePreviewOpen: boolean              // Preview modal visibility
previewDevice: 'desktop'|'tablet'|'mobile'  // Device size
selectedTemplate: Template | null     // Active template
```

---

## 🎯 Main Functions

```typescript
// Open variants panel
handleViewVariants(template: Template)
  └─ setSelectedTemplate(template)
  └─ setVariantsPanelOpen(true)

// Open preview modal
handleLivePreview(template: Template)
  └─ setSelectedTemplate(template)
  └─ setLivePreviewOpen(true)

// Navigate to customize page
handleCustomize(templateId: number)
  └─ navigate(`/templates/${templateId}/variants`)

// Calculate preview width
getDeviceWidth(): string
  └─ Returns: 'w-full' | 'max-w-3xl' | 'max-w-sm'
```

---

## 📊 Data Flow

```
Templates Array (data/templates.ts)
        ↓
Filter 1: Search Query
        ↓
Filter 2: Category Selection
        ↓
Filtered Templates Array
        ↓
Map to Card Components
        ↓
User Interaction
  ├─ Search/Filter: Update state → Re-filter
  ├─ Hover: Show action buttons
  ├─ Preview: Show modal
  ├─ Variants: Show panel
  └─ Customize: Navigate to page
```

---

## 🛠️ Component Dependencies

```
TemplatesPage
├── External
│   ├── Header
│   ├── Footer
│   └── ImageWithFallback
├── UI Components
│   ├── Card
│   ├── Button
│   ├── Badge
│   ├── Input
│   └── Sheet
└── Hooks
    ├── useState
    └── useNavigate
```

---

## 📋 Template Structure

```typescript
{
  id: 1,
  title: "Fashion Store",
  category: "Mode",
  image: "url",
  description: "Template élégant...",
  variants: [
    {
      id: "editorial",
      name: "Édition Éditoriale",
      description: "...",
      preview: "url",
      highlights: ["Feature 1", "Feature 2"]
    }
  ],
  customization: {
    palettes: ["Bleu & ivoire", ...],
    sections: ["Lookbook", ...],
    interactions: ["CTA flottant", ...]
  }
}
```

---

## 🎬 User Journey Map

```
1. LANDING
   User visits /templates
   └─ Sees all 6 templates

2. DISCOVERY
   User searches OR filters
   └─ Narrows down templates

3. EXPLORATION
   User hovers over card
   └─ Sees action buttons

4. PREVIEW (Optional)
   User clicks "Aperçu"
   └─ Opens full device preview

5. VARIANTS (Optional)
   User clicks "Variantes"
   └─ Opens side panel details

6. CUSTOMIZATION
   User clicks "Personnaliser"
   └─ Navigates to customize page

7. CUSTOMIZE
   User customizes template
   └─ Creates their store
```

---

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Cards not showing | Search too specific | Clear search bar |
| Filter not working | Category capitalization | Use exact category name |
| Modal stuck | CSS transition issue | Refresh page (F5) |
| Images not loading | CDN down | Check network tab |
| Navigation fails | Route config | Verify App.tsx routes |
| Styling wrong | Dark mode conflict | Clear cache (Ctrl+Shift+Del) |

---

## ✅ Build & Deployment

```bash
# Development
npm run dev
# → http://localhost:3000/templates

# Production Build
npm run build
# → 1784 modules, 0 errors ✅

# Check Errors
npm run build 2>&1 | grep error
```

---

## 📊 Performance Stats

- **Build Modules**: 1784
- **CSS Bundle**: 71.16 kB (gzip: 12.65 kB)
- **JS Bundle**: 737.98 kB (gzip: 208.14 kB)
- **Build Time**: 20.24s
- **Compilation Errors**: 0
- **Warnings**: 1 (chunk size - not critical)

---

## 🎯 Success Checklist

Before deploying:

- [ ] All 6 templates visible
- [ ] Search filters in real-time
- [ ] Categories filter correctly
- [ ] Preview modal opens/closes
- [ ] Device selector works
- [ ] Variants panel opens/closes
- [ ] Navigation routes correctly
- [ ] Dark mode works
- [ ] Responsive on mobile/tablet/desktop
- [ ] No console errors
- [ ] Build completes successfully

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `TEMPLATES_PAGE_REPLACEMENT_SUMMARY.md` | Overview of changes |
| `TEMPLATES_PAGE_TECHNICAL_DETAILS.md` | Technical implementation |
| `TEMPLATES_PAGE_BEFORE_AFTER.md` | Comparison with old version |
| `TEMPLATES_PAGE_TESTING_GUIDE.md` | Step-by-step testing guide |
| `TEMPLATES_PAGE_QUICK_REFERENCE.md` | This file |

---

## 🔗 Quick Links

| Item | Location |
|------|----------|
| Main File | `src/pages/TemplatesPage.tsx` |
| Data | `src/data/templates.ts` |
| Routing | `src/App.tsx` (line 64-68) |
| Header | `src/components/Header.tsx` |
| Footer | `src/components/Footer.tsx` |
| UI Components | `src/components/ui/` |

---

## 🆘 Quick Debugging

```typescript
// Check if templates loaded
console.log(templates)  // Should show array of 6

// Check active state
console.log({ searchQuery, selectedCategory, selectedTemplate })

// Check filtering
console.log(filteredTemplates)  // Should update on search

// Check navigation
console.log(location.pathname)  // Should be /templates
```

---

## 🚀 Next Steps

1. **Test Locally**
   ```bash
   npm run dev
   # Visit http://localhost:3000/templates
   # Test all features in TESTING_GUIDE.md
   ```

2. **Build & Verify**
   ```bash
   npm run build
   # Check for errors (should be 0)
   ```

3. **Deploy**
   - Push to repository
   - Deploy to production
   - Monitor for issues

4. **Monitor**
   - Check browser console
   - Monitor analytics
   - Gather user feedback

---

## 📞 Support

**Issue?** Check:
1. Console for errors (F12)
2. Network tab for failed requests
3. Testing guide for expected behavior
4. Technical details for implementation info

---

**Last Updated**: 2025-01-15  
**Status**: ✅ Production Ready  
**Version**: 1.0
