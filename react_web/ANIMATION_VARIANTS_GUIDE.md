# Animation Variants Guide 🎨

## 🌊 Available Loading Animations

### 1. Wave Dots (Default) ⭐
**Best for**: General use, chat interfaces

**Features:**
- 7 dots in gradient colors
- Wave motion (up and down)
- Scale effect (1 → 1.2 → 1)
- Opacity pulse (0.6 → 1 → 0.6)
- 1.5s duration
- 0.1s stagger between dots

**Colors:**
```
Blue → Light Blue → Indigo → Violet → Purple → Fuchsia → Pink
#3B82F6 → #60A5FA → #818CF8 → #A78BFA → #C084FC → #E879F9 → #F472B6
```

**Usage:**
```jsx
<LoadingIndicator variant="light" />
```

---

### 2. Pulsing Wave with Glow
**Best for**: Premium interfaces, dark backgrounds

**Features:**
- 7 dots with glow effects
- Scale animation (1 → 1.5 → 1)
- Opacity pulse (0.5 → 1 → 0.5)
- Box shadow glow
- 1.8s duration
- 0.12s stagger

**Usage:**
```jsx
<PulsingWaveLoader />
```

---

### 3. Smooth Sine Wave
**Best for**: Mathematical/technical interfaces

**Features:**
- 9 dots following sine curve
- Mathematical wave pattern
- Gradient background per dot
- Smooth continuous motion
- 2s duration
- 0.08s stagger

**Usage:**
```jsx
<SineWaveLoader />
```

---

### 4. Shimmer Effect
**Best for**: Content loading, skeleton screens

**Features:**
- Horizontal bar with gradient
- Shimmer moves left to right
- Linear animation
- 1.5s duration
- Continuous loop

**Usage:**
```jsx
<ShimmerLoader />
```

---

### 5. Pulsing Dots
**Best for**: Simple, clean interfaces

**Features:**
- 3 dots with glow
- Scale and opacity pulse
- Blue color with shadow
- 1.2s duration
- 0.2s stagger

**Usage:**
```jsx
<PulsingLoader />
```

---

## 🎯 When to Use Each

| Animation | Use Case | Feel |
|-----------|----------|------|
| **Wave Dots** | Chat, messaging | Dynamic, colorful |
| **Pulsing Wave** | Premium apps | Elegant, glowing |
| **Sine Wave** | Technical apps | Mathematical, smooth |
| **Shimmer** | Content loading | Fast, efficient |
| **Pulsing Dots** | Minimal UI | Simple, clean |

---

## 🎨 Customization Examples

### Change to Different Animation

**In ChatBubble.jsx:**
```jsx
// Option 1: Wave Dots (default)
import { LoadingIndicator } from './LoadingIndicator'
<LoadingIndicator variant="light" />

// Option 2: Pulsing Wave
import { PulsingWaveLoader as LoadingIndicator } from './LoadingIndicator'
<LoadingIndicator />

// Option 3: Sine Wave
import { SineWaveLoader as LoadingIndicator } from './LoadingIndicator'
<LoadingIndicator />
```

### Create Custom Colors

**Edit LoadingIndicator.jsx:**
```jsx
// Custom gradient
const gradientColors = [
  '#10B981', // Emerald
  '#14B8A6', // Teal
  '#06B6D4', // Cyan
  '#0EA5E9', // Sky
  '#3B82F6', // Blue
]
```

### Adjust Speed

```jsx
transition={{
  duration: 1.0,  // Fast
  duration: 1.5,  // Default
  duration: 2.5,  // Slow
}}
```

### Change Wave Height

```jsx
animate={{
  y: [0, -8, 0],   // Small wave
  y: [0, -12, 0],  // Default
  y: [0, -20, 0],  // Large wave
}}
```

---

## 🔄 Transition Behavior

### Loading Appears
```javascript
initial: { opacity: 0, scale: 0.9 }
animate: { opacity: 1, scale: 1 }
duration: 0.3s
```

### Loading Disappears
```javascript
exit: { opacity: 0, scale: 0.9 }
duration: 0.3s
```

### Content Appears
```javascript
initial: { opacity: 0, y: 10 }
animate: { opacity: 1, y: 0 }
duration: 0.3s
```

---

## 📊 Performance

All animations are:
- ✅ **GPU accelerated** (transform, opacity)
- ✅ **60fps** on modern devices
- ✅ **No layout shift** (proper sizing)
- ✅ **Efficient** (CSS transforms)

---

## 🎬 Demo

Visit the **Animation Showcase** page to see all variants:
```jsx
<Route path="/showcase" element={<AnimationShowcase />} />
```

---

## 💡 Tips

1. **Consistency**: Use the same animation throughout your app
2. **Context**: Match animation to your app's personality
3. **Duration**: Keep under 2 seconds for best UX
4. **Colors**: Match your brand colors
5. **Testing**: Test on different devices

---

**Last Updated**: 2026-04-19  
**Total Variants**: 5  
**Default**: Wave Dots with Gradient
