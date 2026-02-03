# Template Variants System - Architecture & Structure

## Overview
The template variants system has been refactored to use a **reusable, component-based architecture** with proper separation of concerns. All data flows through the `TemplateSelectionContext` for state management and persistence.

## Component Hierarchy

### Pages
- **TemplateVariantsPage** (`src/pages/TemplateVariantsPage.tsx`)
  - Entry point for template variant selection
  - Orchestrates data flow and routing
  - Imports and uses smaller, focused components
  - Handles context updates and state synchronization

### Reusable Components

#### 1. **VariantCard** 
- **Path**: `src/components/VariantCard.tsx`
- **Purpose**: Display individual template variant with preview and selection
- **Props**:
  - `variant: TemplateVariant` - The variant to display
  - `isSelected: boolean` - Whether this variant is currently selected
  - `onSelect: (id: string) => void` - Callback when variant is selected
- **Renders**:
  - Preview image with hover scaling
  - Checkmark overlay when selected
  - Title, description, and highlights badges
- **Styling**: Conditional borders/shadows based on selection state

#### 2. **CustomizationSection**
- **Path**: `src/components/CustomizationSection.tsx`
- **Purpose**: Display a customization category with color-coded styling
- **Props**:
  - `title: string` - Section title (e.g., "Palettes colorimétriques")
  - `icon: LucideIcon` - Icon to display
  - `color: "purple" | "blue" | "emerald"` - Color variant
  - `items: string[]` - List of customization options
- **Features**:
  - Color-coded backgrounds and dots
  - Icon support with lucide-react
  - Responsive grid layout

#### 3. **CustomizationPreview**
- **Path**: `src/components/CustomizationPreview.tsx`
- **Purpose**: Display all customization categories in a grouped section
- **Props**:
  - `customization: TemplateCustomization` - Full customization data
- **Renders**:
  - CustomizationSection × 3 (Palettes, Sections, Interactions)
  - Automatically maps template customization to UI

#### 4. **TemplateInfoCard**
- **Path**: `src/components/TemplateInfoCard.tsx`
- **Purpose**: Display template metadata in sidebar
- **Props**:
  - `template: Template` - Template to display info for
- **Shows**:
  - Category badge
  - Variant count
  - Template description

#### 5. **ActiveVariantDisplay**
- **Path**: `src/components/ActiveVariantDisplay.tsx`
- **Purpose**: Show detailed info about currently selected variant
- **Props**:
  - `variant: TemplateVariant | undefined` - Active variant
- **Renders**:
  - Variant name and description
  - Highlights badges
  - Highlighted selection box styling

#### 6. **TemplateActionButtons**
- **Path**: `src/components/TemplateActionButtons.tsx`
- **Purpose**: Action buttons for navigation
- **Props**:
  - `templateId: number` - ID for customize page navigation
- **Buttons**:
  - "Continue Customization" → `/templates/:id/customize`
  - "View Other Templates" → `/templates`

## Data Flow & State Management

### Context: TemplateSelectionContext
- **Location**: `src/context/TemplateSelectionContext.tsx`
- **Provides**:
  - `templateId` - Currently selected template
  - `variantId` - Currently selected variant
  - `selectedOptions` - Customization choices
  - `shopConfig` - Shop configuration
- **Methods**:
  - `setTemplate(id, sections, options)` - Initialize template
  - `setVariant(id)` - Update selected variant
  - `setOption(category, value)` - Update customization option
- **Persistence**: Auto-saves to localStorage

### Data Structure: templates.ts
```typescript
interface TemplateVariant {
  id: string;
  name: string;
  description: string;
  preview: string;
  highlights: string[];
}

interface TemplateCustomization {
  palettes: string[];
  sections: string[];
  interactions: string[];
}

interface Template {
  id: number;
  title: string;
  category: string;
  description: string;
  image: string;
  variants: TemplateVariant[];
  customization: TemplateCustomization;
}
```

## Page Layout: TemplateVariantsPage

```
┌─────────────────────────────────────────────────────────────┐
│ Header                                                      │
├─────────────────────────────────────────────────────────────┤
│ Sticky Navigation Bar (Title + Close Button)              │
├─────────────────────────────────────────────────────────────┤
│ Main Content (2/3 column + 1/3 sidebar)                   │
│                                                             │
│ LEFT COLUMN (2/3):                                         │
│ • Variants Section (VariantCard × n)                      │
│ • Active Variant Display                                   │
│                                                             │
│ RIGHT SIDEBAR (1/3):                                       │
│ • Template Info Card                                       │
│ • Customization Preview (CustomizationSection × 3)        │
│ • Action Buttons                                           │
├─────────────────────────────────────────────────────────────┤
│ Footer                                                      │
└─────────────────────────────────────────────────────────────┘
```

## Component Usage in TemplateVariantsPage

```tsx
// Variants Grid (Dynamic mapping)
<div className="grid gap-4">
  {template.variants?.map((variant) => (
    <VariantCard
      key={variant.id}
      variant={variant}
      isSelected={selectedVariantId === variant.id}
      onSelect={(id) => {
        setSelectedVariantId(id);
        persistVariant(id);
      }}
    />
  ))}
</div>

// Active Variant Details
<ActiveVariantDisplay variant={activeVariant} />

// Sidebar Components
<TemplateInfoCard template={template} />
<div className="rounded-2xl border-2 ...">
  <h3>Personnalisations</h3>
  <CustomizationPreview customization={template.customization} />
</div>
<TemplateActionButtons templateId={template.id} />
```

## Key Improvements

### ✅ Reusability
- Components accept data as props
- No hardcoded values in component logic
- Easy to reuse across different pages

### ✅ Maintainability
- Single Responsibility Principle applied
- Each component has clear purpose
- ~100 lines per component (manageable)

### ✅ Type Safety
- Full TypeScript interfaces
- Props properly typed
- Type inference for callbacks

### ✅ Dynamic Content
- All data flows from template data source
- Automatic UI updates when data changes
- Context keeps state synchronized

### ✅ Separation of Concerns
- Page handles routing and context updates
- Components handle only rendering/UI
- State management isolated in Context

## File Structure

```
src/
├── components/
│   ├── VariantCard.tsx (NEW)
│   ├── CustomizationSection.tsx (NEW)
│   ├── CustomizationPreview.tsx (NEW)
│   ├── TemplateInfoCard.tsx (NEW)
│   ├── ActiveVariantDisplay.tsx (NEW)
│   ├── TemplateActionButtons.tsx (NEW)
│   └── ... (existing components)
├── pages/
│   ├── TemplateVariantsPage.tsx (REFACTORED)
│   └── ... (existing pages)
├── context/
│   └── TemplateSelectionContext.tsx (existing)
├── data/
│   └── templates.ts (data source)
└── ...
```

## Integration Points

### TemplatesPage → TemplateVariantsPage
- Click "Voir les variantes" button
- Navigate to `/templates/:id/variants`
- URL parameter triggers template load

### TemplateVariantsPage → TemplateCustomizePage
- Click "Continuer la personnalisation"
- Navigate to `/templates/:id/customize`
- Pass context data to next page

## Dynamic Data Handling

All data is **pulled from a single source** (`src/data/templates.ts`):
1. Page loads template by ID
2. Components receive template data as props
3. Customization options automatically mapped
4. Variant selection triggers context updates
5. localStorage persists state

## Future Enhancements

### Scalability
- Add more customization categories (just add more CustomizationSection components)
- Create VariantsList component to organize variant selection
- Add filter/search functionality to variants

### State Management
- Consider Redux if state becomes complex
- Add undo/redo functionality for variant selection
- Track user preferences and recommendations

### UI/UX
- Add variant comparison feature
- Create preview modal showing live template preview
- Add carousel for variant browsing
- Implement keyboard navigation

## Testing Considerations

### Unit Tests
- VariantCard: Test selection state, callbacks
- CustomizationSection: Test color variants, item rendering
- TemplateInfoCard: Test data display

### Integration Tests
- TemplateVariantsPage: Test full variant selection flow
- Context updates: Verify state synchronization
- localStorage: Verify persistence

### E2E Tests
- Navigation flow: Templates → Variants → Customize
- Variant selection and persistence
- Context data propagation through pages
