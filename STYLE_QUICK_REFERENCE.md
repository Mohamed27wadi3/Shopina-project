# ⚡ Quick Style Reference Card

## Color Shortcuts
```
Primary:        text-[#0077FF] / bg-[#0077FF]
Secondary:      text-[#5AC8FA] / bg-[#5AC8FA]
Dark Text:      text-[#0A1A2F]
Card BG:        bg-white dark:bg-gray-900
Border:         border-gray-100 dark:border-gray-800
```

## Common Patterns

### Premium Card
```tsx
className="rounded-3xl border-2 border-gray-100 dark:border-gray-800 
           bg-white dark:bg-gray-900 p-8 shadow-lg 
           hover:shadow-xl transition-shadow"
```

### Primary Button
```tsx
className="h-14 rounded-xl bg-gradient-to-r from-[#0077FF] to-[#5AC8FA]
           hover:shadow-lg hover:shadow-[#0077FF]/40 text-white 
           font-bold transition-all duration-300 transform hover:scale-105"
```

### Input Field
```tsx
className="h-12 rounded-xl border-2 border-gray-200 dark:border-gray-700 
           focus:border-[#0077FF] focus:shadow-lg focus:shadow-[#0077FF]/20 
           transition-all"
```

### Active Button (Gradient)
```tsx
className="rounded-full border-2 font-semibold transition-all duration-300
           bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] 
           text-white border-[#0077FF] shadow-lg shadow-[#0077FF]/30"
```

### Inactive Button (Outline)
```tsx
className="rounded-full border-2 border-gray-200 dark:border-gray-700 
           text-gray-700 dark:text-gray-300 
           hover:border-[#0077FF] hover:text-[#0077FF]"
```

### Section Title
```tsx
className="text-sm font-bold uppercase tracking-wider 
           text-gray-700 dark:text-gray-300"
```

### Dark Mode Pair
```
Light:  className="..."
Dark:   className="... dark:bg-gray-900 dark:text-white dark:border-gray-800"
```

## Responsive Grid
```tsx
{/* 2 Column */}
className="grid gap-8 lg:grid-cols-[1.15fr,0.85fr]"

{/* 3 Column */}
className="grid md:grid-cols-3 gap-6"

{/* Flexible */}
className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"
```

## Icon Helpers
```tsx
{/* Icon + Text */}
<div className="flex items-center gap-2">
  <Icon className="w-5 h-5 text-[#0077FF]" />
  <span>Label</span>
</div>

{/* Icon Sizes */}
w-4 h-4  // Small (default)
w-5 h-5  // Medium
w-6 h-6  // Large
```

## Animation Classes
```
Smooth:         transition-all duration-300
Colors:         transition-colors
Shadows:        transition-shadow
Scale:          hover:scale-105
Translate:      hover:-translate-y-1
No Motion:      data-[prefer-reduced-motion]:duration-0
```

## Dark Mode Variants
```
Text:           dark:text-white / dark:text-gray-300
Background:     dark:bg-gray-900 / dark:bg-gray-800
Border:         dark:border-gray-800 / dark:border-gray-700
Shadow:         dark:shadow-gray-900/50
Gradient from:  dark:from-gray-900
Gradient to:    dark:to-gray-800
```

## Accessibility
```
Focus Ring:     focus:ring-2 focus:ring-[#0077FF]
Focus Offset:   focus:ring-offset-2
Label:          <label className="text-xs font-bold uppercase">
Alt Text:       alt="descriptive text"
ARIA:           aria-label="descriptive"
```

## Spacing Quick Ref
```
Padding:        p-4 (16px) | p-6 (24px) | p-8 (32px)
Gap:            gap-2 (8px) | gap-4 (16px) | gap-8 (32px)
Margin:         m-4 (16px) | mx-auto (center)
Height Input:   h-12 (48px) - standard form
Height Button:  h-14 (56px) - primary action
```

## Text Classes
```
Headlines:      text-4xl font-extrabold
Section:        text-2xl font-bold
Subsection:     text-xl font-bold
Body:           text-base text-gray-600
Small:          text-sm text-gray-500
Label:          text-xs font-bold uppercase
```

## Ready-to-Copy Components

### Loading State
```tsx
<div className="flex items-center justify-center gap-2">
  <div className="w-3 h-3 bg-[#0077FF] rounded-full animate-pulse"></div>
  <span>Chargement...</span>
</div>
```

### Empty State
```tsx
<div className="text-center py-12">
  <p className="text-5xl mb-4">📭</p>
  <h3 className="text-xl font-bold text-gray-700">Aucun élément</h3>
  <p className="text-gray-500 mt-2">Créez-en un pour commencer</p>
</div>
```

### Success Message
```tsx
<div className="rounded-2xl border-2 border-green-200 
                bg-green-50 dark:bg-green-900/20 p-4 
                text-green-700 dark:text-green-300">
  ✓ Opération réussie
</div>
```

### Badge
```tsx
<span className="px-3 py-1 rounded-full bg-[#0077FF]/10 
                 text-[#0077FF] text-xs font-bold">
  Badge
</span>
```

## Performance Tips
1. Use Tailwind's `group` for hover states
2. Apply `transition-all duration-300` for smooth effects
3. Use `dark:` prefix for dark mode
4. Minimize custom CSS (use Tailwind first)
5. Hardware-accelerate with `transform`
6. Lazy load images with loading="lazy"
7. Use `backdrop-blur-sm` for glass effects (has fallback)

## Mobile-First Breakpoints
```
Default:    Mobile (< 768px)
md:         Tablet (768px+)
lg:         Desktop (1024px+)
xl:         Large (1280px+)
2xl:        Extra Large (1536px+)
```

## Testing Colors
```
Light Mode: #FFFFFF (white) background
Dark Mode:  #1F2937 (gray-800) background
Text on light:     #0A1A2F (98% readability)
Text on dark:      #FFFFFF (100% readability)
Links:             #0077FF (WCAG AA compliant)
```

---

**Print this for quick reference!**
**Save as bookmark for quick access**
**Share with team members**
