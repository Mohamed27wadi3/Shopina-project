# Styling & Layout Consistency Guide

## Color Scheme

### Primary Colors
- Primary Blue: `#0077FF` - Main brand color
- Secondary Blue: `#5AC8FA` - Accent color
- Dark Bg: `#0A1A2F` - Dark mode background

### Text Colors
- Primary Text (Light): `#0A1A2F` (dark background)
- Primary Text (Dark): `white` (light background)
- Secondary Text: `#0A1A2F/60` or `#0A1A2F/70`
- Muted Text: `#0A1A2F/40`

### Status Colors
- Success: `#34A853` (Green)
- Warning: `#FBBC05` (Yellow)
- Error: `#EA4335` (Red)
- Info: `#4285F4` (Blue)

## Button Styling

### Primary Button
```tsx
className="bg-[#0077FF] hover:bg-[#0077FF]/90 text-white h-12 rounded-xl shadow-lg shadow-[#0077FF]/30"
```

### Secondary Button (Outline)
```tsx
className="border-2 border-gray-200 hover:border-[#0077FF]/30 hover:bg-gray-50 dark:hover:bg-gray-800"
```

### Small Button
```tsx
className="h-10 px-4 rounded-lg text-sm"
```

## Form Input Styling

### Standard Input
```tsx
className="h-12 px-4 rounded-xl border-2 border-gray-200 focus:border-[#0077FF] focus:outline-none"
```

### Input with Icon
```tsx
className="pl-12 pr-12 h-12 rounded-xl border-2 border-gray-200 focus:border-[#0077FF]"
```

## Card Styling

### Standard Card
```tsx
className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-800 p-8"
```

### Compact Card
```tsx
className="bg-white dark:bg-gray-900 rounded-xl shadow-lg border border-gray-100 dark:border-gray-800 p-6"
```

## Typography

### Headings
- H1: `fontSize: '32px', fontWeight: '800'` - Page titles
- H2: `fontSize: '24px', fontWeight: '700'` - Section titles
- H3: `fontSize: '20px', fontWeight: '600'` - Subsection titles

### Body Text
- Regular: `fontWeight: '400'` - Default
- Medium: `fontWeight: '500'` - Emphasis
- SemiBold: `fontWeight: '600'` - Strong emphasis

## Spacing System

```
xs: 0.25rem (4px)
sm: 0.5rem (8px)
md: 1rem (16px)
lg: 1.5rem (24px)
xl: 2rem (32px)
2xl: 2.5rem (40px)
3xl: 3rem (48px)
```

## Layout Guidelines

### Page Container
```tsx
className="min-h-screen bg-gradient-to-br from-[#0077FF]/5 via-[#5AC8FA]/5 to-white dark:from-[#0A0A0A] dark:via-[#1A1A1A] dark:to-[#0A0A0A]"
```

### Content Wrapper
```tsx
className="w-full max-w-7xl mx-auto px-6 py-12"
```

### Responsive Grid
- Mobile: `grid-cols-1`
- Tablet: `md:grid-cols-2`
- Desktop: `lg:grid-cols-3` or `xl:grid-cols-4`

## Dark Mode Toggle

Dark mode is controlled by the `.dark` class on the root element. Use CSS-in-JS or Tailwind's `dark:` prefix.

### Example
```tsx
<div className="bg-white dark:bg-gray-900">
  <h1 className="text-[#0A1A2F] dark:text-white">Title</h1>
  <p className="text-[#0A1A2F]/60 dark:text-gray-400">Description</p>
</div>
```

## Common Component Fixes

### Dashboard Header
- Background: `bg-white dark:bg-gray-900`
- Border: `border-b border-gray-200 dark:border-gray-800`
- Padding: `px-8 py-6`
- Height: `h-20` (80px)

### Sidebar
- Width: `w-64` (256px)
- Background: `bg-[#0A1A2F]`
- Text: `text-white`
- Hover Items: `hover:bg-white/10`

### Product Card
```tsx
className="bg-white dark:bg-gray-900 rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-shadow"
```

### Form Section
```tsx
className="space-y-4"
```
- Gap between inputs: `4` (1rem)

### Alert/Notification
```tsx
className="rounded-lg p-4 border-l-4 border-[#0077FF] bg-[#0077FF]/10"
```

## Responsive Breakpoints

```
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### Mobile-First Approach
```tsx
// Mobile (base)
className="px-4 py-6"
// Tablet and up
className="px-4 py-6 md:px-8 md:py-12"
// Desktop and up
className="px-4 py-6 md:px-8 md:py-12 lg:px-12"
```

## Animation & Transitions

### Smooth Transitions
```tsx
className="transition-all duration-300"
```

### Hover Effects
```tsx
className="hover:scale-105 hover:shadow-lg transition-all duration-300"
```

### Fade In
```tsx
className="animate-fade-in opacity-0 animate-in"
```

## Accessibility Guidelines

1. Maintain color contrast ≥ 4.5:1 for text
2. Use focus rings: `focus:ring-2 focus:ring-[#0077FF] focus:ring-offset-2`
3. Add aria-labels for icon-only buttons
4. Ensure keyboard navigation works
5. Use semantic HTML (buttons, links, forms)

## Common Issues & Fixes

### Issue: Button text overlap
**Fix**: Ensure h-12 height and appropriate padding

### Issue: Form inputs not aligned
**Fix**: Use consistent h-12 or h-10, border-2

### Issue: Dark mode text invisible
**Fix**: Always use `dark:text-white` or `dark:text-gray-400`

### Issue: Responsive not working
**Fix**: Remember Tailwind is mobile-first (base = mobile)

### Issue: Shadow not visible in dark mode
**Fix**: Use `dark:shadow-gray-900` or adjust shadow color

## Testing Checklist

- [ ] All buttons have consistent height (h-12 or h-10)
- [ ] All inputs have consistent styling
- [ ] Dark mode works on all pages
- [ ] Hover states are visible
- [ ] Text contrast is sufficient
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] No horizontal scroll on mobile
- [ ] Touch targets are ≥ 44px
- [ ] Forms have proper spacing
- [ ] Icons and text are aligned
- [ ] Loading states are clear
- [ ] Error messages are visible
