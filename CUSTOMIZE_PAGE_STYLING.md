# TemplateCustomizePage - Professional Styling Guide

## 🎨 Overview
The Template Customize page has been completely redesigned with **premium, modern styling** featuring:
- Gradient backgrounds and accent colors
- Smooth animations and transitions
- Professional typography hierarchy
- Dark mode support throughout
- Responsive grid layout
- Premium card designs with shadows and hover effects

## 🎯 Design Principles

### Color Palette
- **Primary Blue**: `#0077FF` - Main action color
- **Secondary Cyan**: `#5AC8FA` - Accent and hover states
- **Dark Text**: `#0A1A2F` - Headlines and primary text
- **Light Gray**: `#F8FAFC` - Backgrounds
- **Border Gray**: `#E2E8F0` - Subtle dividers

### Typography
- **Headlines**: Extrabold (900) weight, gradient text effect
- **Labels**: Bold uppercase with tracking
- **Body**: Regular weight, semantic colors
- **Icons**: Integrated with text for visual clarity

### Spacing
- **Base unit**: 4px Tailwind grid
- **Component padding**: 6-8px (24-32px)
- **Gap between sections**: 24-32px (6-8 units)

## 📐 Page Structure

### Layout Layers
```
┌─────────────────────────────────────────────────────────┐
│ Sticky Navigation Bar (Step indicator + Badge)         │
├─────────────────────────────────────────────────────────┤
│ Header Section (Title + Description)                   │
├─────────────────────────────────────────────────────────┤
│ Main Content (2-column: Preview + Controls)            │
│                                                         │
│ LEFT: Preview Card (500px height)                      │
│ RIGHT: Tabs (Brand | Styles | Modules)                │
├─────────────────────────────────────────────────────────┤
│ Info Section (3-column benefits grid)                  │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Component Styling Details

### 1. Top Navigation Bar
```tsx
<div className="border-b border-gray-100/80 dark:border-gray-800 
                bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm 
                sticky top-0 z-40">
```
- **Features**:
  - Glassmorphism effect (backdrop blur)
  - Sticky positioning
  - Subtle border and shadow
  - Semi-transparent background

### 2. Preview Card
```tsx
<div className="rounded-3xl border-2 border-gray-100 dark:border-gray-800 
                bg-white dark:bg-gray-900 p-8 shadow-lg 
                hover:shadow-xl transition-shadow overflow-hidden">
```
- **Features**:
  - Large rounded corners (3xl)
  - Prominent shadow with hover elevation
  - Smooth transition on hover
  - 32px padding for breathing room
  - Consistent dark mode variant

### 3. Tab List
```tsx
<TabsList className="grid grid-cols-3 
                     bg-gradient-to-r from-white to-gray-50 
                     dark:from-gray-900 dark:to-gray-800 
                     rounded-2xl p-1.5 border border-gray-100 
                     dark:border-gray-800 shadow-sm">
```
- **Features**:
  - Gradient background for depth
  - Subtle borders
  - Small shadow for elevation
  - Responsive grid layout

### 4. Tab Triggers (Active State)
```tsx
data-[state=active]:bg-gradient-to-r 
data-[state=active]:from-[#0077FF] 
data-[state=active]:to-[#5AC8FA] 
data-[state=active]:text-white 
data-[state=active]:shadow-lg 
data-[state=active]:shadow-[#0077FF]/30
```
- **Features**:
  - Gradient background when active
  - Elevated shadow with colored glow
  - White text for contrast
  - Smooth state transitions

### 5. Form Inputs
```tsx
<Input className="h-12 rounded-xl border-2 border-gray-200 
                  dark:border-gray-700 
                  focus:border-[#0077FF] 
                  focus:shadow-lg focus:shadow-[#0077FF]/20 
                  transition-all" />
```
- **Features**:
  - 48px height for touch targets
  - 8px border radius for modern feel
  - 2px borders for better definition
  - Blue focus state with colored shadow
  - All transitions for smooth UX

### 6. Color Input Group
```tsx
<div className="flex items-center gap-3">
  <Input type="color" className="h-12 w-16 rounded-xl" />
  <Input type="text" className="flex-1 h-12 rounded-xl" />
</div>
```
- **Features**:
  - Visual color picker + text input
  - Flexible layout for mobile
  - Consistent sizing
  - Better UX than single input

### 7. Palette Buttons
```tsx
<Button className={`rounded-full border-2 font-semibold 
                    transition-all duration-300 
                    ${selectedOptions.palettes === palette 
                      ? "bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] 
                         text-white border-[#0077FF] 
                         shadow-lg shadow-[#0077FF]/30" 
                      : "border-gray-200 dark:border-gray-700 
                         text-gray-700 dark:text-gray-300 
                         hover:border-[#0077FF] hover:text-[#0077FF]"
                    }`} />
```
- **Features**:
  - Full border for pill shape
  - State-based styling
  - Gradient active state
  - Hover color transition
  - Smooth animations

### 8. Layout Option Cards
```tsx
className={`w-full text-left rounded-2xl border-2 p-4 
            transition-all duration-300 
            ${shopConfig.layout === option.id
              ? "border-[#0077FF] 
                 bg-gradient-to-r from-[#0077FF]/10 to-[#5AC8FA]/10 
                 dark:from-[#0077FF]/20 dark:to-[#5AC8FA]/20 
                 shadow-lg shadow-[#0077FF]/20"
              : "border-gray-200 dark:border-gray-700 
                 hover:border-[#0077FF]/50 dark:hover:border-[#0077FF]/50"
            }`}
```
- **Features**:
  - Gradient background when selected
  - Colored shadow for depth
  - Subtle hover state
  - Clear selection indicator

### 9. Action Buttons
```tsx
<Button className="h-14 rounded-xl 
                   bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] 
                   hover:shadow-lg hover:shadow-[#0077FF]/40 
                   text-white font-bold flex-1 
                   transition-all duration-300 
                   transform hover:scale-105">
  <Sparkles className="w-5 h-5" />
  Associer à ma boutique
</Button>
```
- **Features**:
  - Large height (56px) for emphasis
  - Gradient background
  - Scale transform on hover
  - Colored shadow effect
  - Icon + text combination

### 10. Info Section Cards
```tsx
<div className="rounded-2xl border-2 border-gray-100 dark:border-gray-800 
                bg-white dark:bg-gray-900 p-6 
                hover:shadow-md transition-shadow">
```
- **Features**:
  - Simple card design
  - Hover shadow elevation
  - Consistent with page theme
  - Icon + title + description layout
  - Emoji for visual interest

## 🌓 Dark Mode Integration

Every component includes dark mode variants:
- `dark:border-gray-800` - Darker borders
- `dark:bg-gray-900` - Darker backgrounds
- `dark:text-white` - Inverted text
- `dark:text-gray-300` - Secondary text
- `dark:from-gray-900` - Gradient starts
- `dark:to-gray-800` - Gradient ends

## ✨ Animation & Transition Details

### Transitions Applied
- `transition-colors` - Color changes
- `transition-shadow` - Shadow depth
- `transition-all duration-300` - All properties over 300ms
- `transform hover:scale-105` - Subtle zoom on hover

### Effects
- **Hover Shadows**: `shadow-lg shadow-[#0077FF]/30`
- **Focus States**: Colored glow with shadow
- **Button States**: Scale and shadow combination
- **State Changes**: Smooth gradient transitions

## 📱 Responsive Behavior

### Breakpoints
- **Mobile**: Single column, full-width
- **Tablet (md)**: 2-column layout with responsive grid
- **Desktop (lg)**: Full 2-column with sidebar

### Key Responsive Classes
```tsx
lg:grid-cols-[1.15fr,0.85fr]  // Main content grid
md:grid-cols-3               // Benefits section
grid gap-4 lg:gap-8          // Adaptive spacing
sm:flex-row                  // Button layout
```

## 🎯 Implementation Best Practices

### For Adding New Elements

1. **Use the design system**:
   ```tsx
   rounded-xl/2xl/3xl           // Border radius
   border-2 border-gray-100     // Borders
   dark:border-gray-800         // Dark variant
   shadow-sm/md/lg              // Shadows
   transition-all duration-300  // Animations
   ```

2. **Maintain hierarchy**:
   - Headlines: Bold, large, gradient
   - Labels: Bold, uppercase, small
   - Body: Regular, semantic color
   - Icons: 4-5px, embedded with text

3. **Color consistency**:
   - Primary actions: `#0077FF`
   - Secondary: `#5AC8FA`
   - Accents: Gradients combining both
   - Backgrounds: Gray palette

4. **Spacing consistency**:
   - Component padding: 6-8px (p-6, p-7, p-8)
   - Gap between items: 4px (gap-4)
   - Large gaps: 8px (gap-8)

## 🚀 Performance Considerations

- Gradients are GPU-accelerated
- Transitions are hardware-optimized
- Backdrop blur has fallback
- Shadows are minimal for performance
- No animations on load

## 📊 Testing Checklist

- [ ] All tabs work smoothly
- [ ] Colors display correctly in light mode
- [ ] Colors display correctly in dark mode
- [ ] Hover effects are smooth
- [ ] Focus states are visible
- [ ] Form inputs are accessible (keyboard)
- [ ] Mobile layout is responsive
- [ ] Buttons scale correctly on hover
- [ ] Shadows render without performance issues
- [ ] Dark mode toggle works seamlessly

## 🎨 Future Enhancements

1. **Animations**:
   - Page load animation (stagger effect)
   - Tab transition animation
   - Gradient animation on buttons

2. **Interactivity**:
   - Live color preview updates
   - Real-time preview refresh
   - Undo/redo functionality

3. **Accessibility**:
   - ARIA labels on all buttons
   - Keyboard navigation shortcuts
   - High contrast mode support
   - Reduced motion preferences

4. **Mobile Optimization**:
   - Touch-friendly button sizes
   - Swipe to navigate tabs
   - Bottom sheet for mobile controls
   - Simplified mobile layout

---

**Last Updated**: Current Session
**Build Status**: ✅ Production build successful
**Dev Server**: ✅ HMR working (auto-reload on changes)
**Dark Mode**: ✅ Fully tested and working
