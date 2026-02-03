# Dynamic Template System - Integration Guide

## 🎯 Objective
Transform the static template system into a fully dynamic, well-structured architecture where all data flows from a centralized source and components reuse logic across the application.

## ✅ What Has Been Completed

### 1. Reusable Component Creation

#### VariantCard.tsx
- Displays individual template variants
- Manages selection state visually
- Accepts variant data via props
- Reusable across different pages

#### CustomizationSection.tsx
- Generic component for displaying customization categories
- Color-coded styling (purple/blue/emerald)
- Icon support with lucide-react
- Can be reused for any category list

#### CustomizationPreview.tsx
- Aggregates all CustomizationSection components
- Maps template customization to UI
- Single responsibility: layout of sections

#### TemplateInfoCard.tsx
- Displays template metadata
- Shows category, variant count, description
- Reusable in different pages/contexts

#### ActiveVariantDisplay.tsx
- Shows details of selected variant
- Displays highlights and description
- Handles undefined state gracefully

#### TemplateActionButtons.tsx
- Navigation buttons wrapper
- Encapsulates routing logic
- Accepts only necessary props (templateId)

### 2. Page Refactoring

#### TemplateVariantsPage.tsx
- **Before**: ~310 lines with hardcoded JSX
- **After**: ~130 lines using composed components
- **Benefits**:
  - 60% less code
  - All logic extracted to components
  - Dynamic data mapping
  - Better readability

### 3. Data Flow Architecture

```
templates.ts (Data Source)
     ↓
TemplateSelectionContext (State Management)
     ↓
TemplateVariantsPage (Orchestration)
     ↓
Reusable Components (Rendering)
```

### 4. State Persistence

- TemplateSelectionContext manages all state
- localStorage auto-saves to browser
- State survives page refreshes
- Shared across multiple pages

## 🔄 Current Data Flow

### Navigation Flow
```
Templates Page
    ↓ (Click "Voir les variantes")
Template Variants Page
    ↓ (URL: /templates/:id/variants)
Load template by ID from templates.ts
    ↓
Initialize context with template data
    ↓
Render variant cards dynamically
    ↓ (User selects variant)
Update context state
    ↓ (Click "Continuer")
Navigate to /templates/:id/customize
```

### Component Composition
```
TemplateVariantsPage
├── Header
├── Navigation (Sticky)
├── Main Content
│   ├── LEFT (2/3)
│   │   ├── Variants Section
│   │   │   └── VariantCard (×n, mapped)
│   │   └── ActiveVariantDisplay
│   └── RIGHT (1/3 Sidebar)
│       ├── TemplateInfoCard
│       ├── CustomizationPreview
│       │   └── CustomizationSection (×3)
│       └── TemplateActionButtons
└── Footer
```

## 🚀 Next Steps for Full Dynamization

### Phase 1: Complete TemplateCustomizePage Refactoring
**Goal**: Extract hardcoded sections into reusable components

1. Create **TabSection** component
   - Wraps common tab structure
   - Accepts content as children
   
2. Create **ShopConfigForm** component
   - Shop name, tagline, colors inputs
   - Encapsulates form logic
   
3. Create **ColorPresetsGrid** component
   - Extract color preset selection
   - Reusable for other color selections

4. Create **SectionToggleList** component
   - Checkboxes for enabling/disabling sections
   - Drag-and-drop support

### Phase 2: Add Dynamic Customization Options

1. Extend TemplateCustomization data structure
   ```typescript
   interface TemplateCustomization {
     palettes: { id: string; name: string; colors: string[] }[];
     sections: { id: string; name: string; icon: string }[];
     interactions: { id: string; name: string; preview: string }[];
   }
   ```

2. Create UI for selecting from options
   - Visual preview for each option
   - Grouped by category
   - Quick toggle interface

### Phase 3: Live Preview System

1. Create **TemplatePreviewBuilder** component
   - Real-time preview as user customizes
   - Shows changes immediately
   - Uses context data

2. Add preview state management
   - Track which preview to show
   - Update on context changes

### Phase 4: Complete Integration

1. Hook all pages together
   - Templates → Variants → Customize → Review → Publish

2. Add confirmation screen before publishing
   - Review all selections
   - Final preview
   - Confirm action

## 📝 Component Development Checklist

### Each Component Should Have:
- ✅ Clear purpose and single responsibility
- ✅ Typed props interface
- ✅ No hardcoded data
- ✅ Proper error handling
- ✅ Reusable logic
- ✅ Consistent styling

### Component Template:
```tsx
import { [required imports] } from "[packages]";
import type { [required types] } from "[local files]";

interface [ComponentName]Props {
  // Only essential props
  // No derived/computed props
  prop1: Type;
  prop2: Type;
  onAction?: (value: Type) => void;
}

export function [ComponentName]({ prop1, prop2, onAction }: [ComponentName]Props) {
  // Minimal logic - mostly rendering
  
  return (
    // JSX - simple structure
  );
}
```

## 🎨 Styling Strategy

### Consistency Rules
- Use Tailwind CSS utility classes
- Primary color: `#0077FF` (stored as `[#0077FF]`)
- Secondary color: `#5AC8FA` (stored as `[#5AC8FA]`)
- Dark mode: `dark:` prefixed classes
- Spacing: 4px grid base unit

### Component Styling Pattern
```tsx
<div className="rounded-2xl border-2 border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 p-6">
  {/* Content */}
</div>
```

## 🔗 Integration Points for Future Features

### Color Customization
- Use `selectedOptions.palettes` from context
- Create color picker component
- Live update preview

### Section Management
- Use `shopConfig.sections` array
- Add drag-and-drop reordering
- Show/hide sections dynamically

### Template Association
- Store selected template ID in context
- POST to `/api/shop/templates/associate` on publish
- Handle response and navigation

## 📊 State Structure Reference

### TemplateSelectionContext
```typescript
{
  templateId: number | null;
  variantId: string | null;
  selectedOptions: {
    palettes: string;
    sections: string;
    interactions: string;
  };
  shopConfig: {
    shopName: string;
    tagline: string;
    primaryColor: string;
    accentColor: string;
    sections: string[]; // enabled sections
  };
}
```

## 🧪 Testing Strategy

### Component Tests
1. Render with different props
2. Test callback functions
3. Verify styling states

### Integration Tests
1. Navigation flow
2. Context updates
3. localStorage persistence

### E2E Tests
1. Full user journey
2. Selection and customization
3. Publishing workflow

## 🎯 Success Metrics

- [ ] All hardcoded JSX extracted to components
- [ ] No duplicate code across pages
- [ ] Data flows from single source (templates.ts)
- [ ] All components accept data via props
- [ ] State management isolated in Context
- [ ] ~30% reduction in total component code
- [ ] All pages under 150 lines
- [ ] 100% TypeScript compliance
- [ ] Dark mode works in all components
- [ ] Mobile responsive layout maintained

## 📚 File Reference

### New Components Created
- `src/components/VariantCard.tsx` ✅
- `src/components/CustomizationSection.tsx` ✅
- `src/components/CustomizationPreview.tsx` ✅
- `src/components/TemplateInfoCard.tsx` ✅
- `src/components/ActiveVariantDisplay.tsx` ✅
- `src/components/TemplateActionButtons.tsx` ✅

### Refactored Pages
- `src/pages/TemplateVariantsPage.tsx` ✅ (130 lines, 60% reduction)
- `src/pages/TemplateCustomizePage.tsx` (pending refactor)

### Data Source
- `src/data/templates.ts` (unchanged, single source of truth)

### State Management
- `src/context/TemplateSelectionContext.tsx` (unchanged, fully functional)

## 🚢 Deployment Checklist

- [ ] All components build successfully
- [ ] No TypeScript errors
- [ ] No console warnings
- [ ] Mobile layout verified
- [ ] Dark mode tested
- [ ] localStorage verified
- [ ] Navigation tested
- [ ] Component props documented
- [ ] Code review completed

## 💡 Pro Tips

1. **Always check the data structure first** before creating components
2. **Minimize component props** - pass only what's needed
3. **Use TypeScript interfaces** for type safety
4. **Keep components under 100 lines** for readability
5. **Test components in isolation** before integration
6. **Use Storybook** for component documentation (future)
7. **Document component props** clearly
8. **Version components** as app evolves

---

**Last Updated**: Current Session
**Build Status**: ✅ 1780 modules, No errors
**Dev Server**: ✅ Running on http://localhost:3000/
