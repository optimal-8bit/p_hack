# MorphingLoader Quick Reference

## 🚀 Quick Start

```jsx
import MorphingLoader from '@/components/MorphingLoader'

// Basic
<MorphingLoader />

// With options
<MorphingLoader 
  size="lg" 
  color="gradient" 
  message="Loading..."
/>
```

## 📦 Props

| Prop | Type | Default | Options |
|------|------|---------|---------|
| `size` | string | `'md'` | `'sm'` `'md'` `'lg'` `'xl'` |
| `color` | string | `'gradient'` | `'blue'` `'purple'` `'gradient'` |
| `fullScreen` | boolean | `false` | `true` `false` |
| `message` | string | `''` | Any string |

## 🎨 Sizes

- **sm**: 32px - Inline, compact spaces
- **md**: 48px - Default, most use cases
- **lg**: 64px - Main content areas
- **xl**: 80px - Full-screen, hero sections

## 🌈 Colors

- **blue**: Healthcare, professional
- **purple**: Creative, modern
- **gradient**: Premium, eye-catching (default)

## 💡 Common Patterns

### Standard Loading State
```jsx
{loading ? (
  <MorphingLoader size="lg" color="gradient" message="Loading..." />
) : (
  <Content />
)}
```

### Full Screen
```jsx
{initializing && (
  <MorphingLoader 
    fullScreen 
    size="xl" 
    color="gradient" 
    message="Initializing..."
  />
)}
```

### Inline Loading
```jsx
<div style={{ minHeight: '200px', display: 'flex', alignItems: 'center' }}>
  <MorphingLoader size="md" color="blue" message="Loading..." />
</div>
```

### With LoadingWrapper
```jsx
import { LoadingWrapper } from '@/components/MorphingLoader'

<LoadingWrapper loading={isLoading} loaderProps={{ size: 'lg' }}>
  <Content />
</LoadingWrapper>
```

## 🎯 Doctor Pages Usage

| Page | Size | Color | Message |
|------|------|-------|---------|
| Dashboard | `lg` | `gradient` | "Loading dashboard data..." |
| Appointments | `lg` | `blue` | "Loading appointments..." |
| Patients | `lg` | `purple` | "Loading patients..." |
| Prescriptions | `lg` | `purple` | "Loading prescriptions..." |
| Recommendations | `md` | `blue` | "Finding specialists..." |

## ⚡ Performance Tips

✅ **DO**
- Use appropriate size for context
- Keep messages concise (< 30 chars)
- Use `fullScreen` sparingly

❌ **DON'T**
- Use multiple loaders on same page
- Use `xl` for inline loaders
- Nest loaders inside loaders

## ♿ Accessibility

Automatically includes:
- `role="status"`
- `aria-busy="true"`
- `aria-live="polite"`
- Reduced motion support

## 🐛 Troubleshooting

**Loader not showing?**
- Check `loading` state is `true`
- Verify import path
- Ensure CSS is imported

**Animation choppy?**
- Check browser support
- Disable other animations
- Test with reduced motion off

**Flicker on fast loads?**
- Use `LoadingWrapper`
- Implement minimum visible time
- Check network throttling

## 📚 Full Documentation

- **Complete Guide**: `MORPHING_LOADER_GUIDE.md`
- **Implementation**: `MORPHING_LOADER_IMPLEMENTATION.md`
- **Demo Page**: `/morphing-loader-demo`

## 🔗 Related Files

- Component: `src/components/MorphingLoader.jsx`
- Styles: `src/components/MorphingLoader.css`
- Demo: `src/pages/MorphingLoaderDemo.jsx`

---

**Need help?** Check the full guide or demo page!
