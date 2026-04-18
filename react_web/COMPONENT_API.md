# Component API Reference

## 📦 Component Overview

All components are located in `src/components/` and use:
- **React 19** functional components
- **Framer Motion** for animations
- **Tailwind CSS** for styling
- **PropTypes** for type validation

---

## ChatBubble

Message bubble component with animations and markdown support.

### Import
```jsx
import { ChatBubble } from './components/ChatBubble'
```

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `object` | ✅ Yes | Message object containing id, role, content, files, createdAt |
| `isStreaming` | `boolean` | ❌ No | Whether the message is currently streaming (shows loading indicator) |

### Message Object Structure
```typescript
{
  id: string              // Unique message identifier
  role: 'user' | 'assistant'  // Message sender
  content: string         // Message text (markdown supported)
  files?: Array<{         // Optional file attachments
    name: string
    size: number
    type: string
  }>
  createdAt: string       // ISO timestamp
}
```

### Usage
```jsx
<ChatBubble 
  message={{
    id: '123',
    role: 'assistant',
    content: '## Hello\nThis is **markdown**',
    createdAt: new Date().toISOString()
  }}
  isStreaming={false}
/>
```

### Features
- ✅ Fade + slide up entry animation
- ✅ Markdown rendering
- ✅ File attachment display
- ✅ Loading indicator when streaming
- ✅ Responsive width (85% mobile, 75% desktop)
- ✅ Role-based styling (user vs assistant)

---

## InputBar

Modern input component with icons and file attachment support.

### Import
```jsx
import { InputBar } from './components/InputBar'
```

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `draft` | `string` | ✅ Yes | Current input text value |
| `setDraft` | `function` | ✅ Yes | Function to update draft text |
| `files` | `Array<File>` | ✅ Yes | Array of attached files |
| `onSelectFiles` | `function` | ✅ Yes | Handler for file selection |
| `removeFile` | `function` | ✅ Yes | Handler to remove a file by name |
| `onSubmit` | `function` | ✅ Yes | Form submit handler |
| `canSend` | `boolean` | ✅ Yes | Whether send button is enabled |
| `isStreaming` | `boolean` | ✅ Yes | Whether currently streaming |

### Usage
```jsx
<InputBar
  draft={draft}
  setDraft={setDraft}
  files={files}
  onSelectFiles={(e) => setFiles([...files, ...e.target.files])}
  removeFile={(name) => setFiles(files.filter(f => f.name !== name))}
  onSubmit={handleSubmit}
  canSend={draft.trim().length > 0}
  isStreaming={false}
/>
```

### Features
- ✅ Pill-shaped design with focus glow
- ✅ Camera and Plus icons with micro-interactions
- ✅ Auto-expanding textarea
- ✅ File attachment management
- ✅ Keyboard shortcuts (Enter to send, Shift+Enter for new line)
- ✅ Disabled state when streaming

---

## LoadingIndicator

Beautiful loading animation with multiple variants.

### Import
```jsx
import { LoadingIndicator, ShimmerLoader, PulsingLoader } from './components/LoadingIndicator'
```

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `variant` | `'light' \| 'dark'` | ❌ No | `'light'` | Color theme for dots |

### Usage

#### Bouncing Dots (Default)
```jsx
<LoadingIndicator variant="light" />
```

#### Shimmer Effect
```jsx
<ShimmerLoader />
```

#### Pulsing Dots with Glow
```jsx
<PulsingLoader />
```

### Features
- ✅ Three animation variants
- ✅ Smooth, seamless loops
- ✅ GPU-accelerated
- ✅ No jitter or layout shift
- ✅ Accessible (role="status")

---

## MarkdownView

Markdown renderer with syntax highlighting.

### Import
```jsx
import { MarkdownView } from './components/MarkdownView'
```

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `content` | `string` | ❌ No | Markdown text to render |
| `isUser` | `boolean` | ❌ No | Whether this is a user message (affects styling) |

### Usage
```jsx
<MarkdownView 
  content="## Hello\nThis is **bold** and *italic*"
  isUser={false}
/>
```

### Supported Markdown
- ✅ Headers (h1-h6)
- ✅ Bold (`**text**`)
- ✅ Italic (`*text*`)
- ✅ Inline code (`` `code` ``)
- ✅ Code blocks (` ``` `)
- ✅ Lists (ordered and unordered)
- ✅ Links (`[text](url)`)

### Features
- ✅ Syntax highlighting for code blocks
- ✅ Role-based theming
- ✅ XSS protection (HTML escaping)
- ✅ Responsive styling

---

## AnimationShowcase

Demo component displaying all UI features.

### Import
```jsx
import { AnimationShowcase } from './components/AnimationShowcase'
```

### Props
None - standalone component

### Usage
```jsx
<Route path="/showcase" element={<AnimationShowcase />} />
```

### Features
- ✅ Icon interaction demos
- ✅ All loading animation variants
- ✅ Chat bubble examples
- ✅ Input bar demo
- ✅ File chip examples

---

## ChatTemplatePage

Main chat page component.

### Import
```jsx
import ChatTemplatePage from './pages/ChatTemplatePage'
```

### Props
None - standalone page component

### Usage
```jsx
<Route path="/chat" element={<ChatTemplatePage />} />
```

### Features
- ✅ Full chat interface
- ✅ Message management
- ✅ Streaming support
- ✅ File attachments
- ✅ Error handling
- ✅ Responsive layout
- ✅ Auto-scroll

---

## 🎨 Styling Customization

### Tailwind Classes
All components use Tailwind CSS. Customize by modifying classes:

```jsx
// Example: Change bubble color
className="bg-gradient-to-br from-purple-600 to-purple-700"
```

### Animation Timing
Adjust in component files:

```jsx
transition={{ duration: 0.3 }}  // Faster
transition={{ duration: 0.5 }}  // Slower
```

### Colors
Modify in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        DEFAULT: "hsl(221.2 83.2% 53.3%)",
      }
    }
  }
}
```

---

## 🔧 Advanced Usage

### Custom Loading Animation

Create your own in `LoadingIndicator.jsx`:

```jsx
export function CustomLoader() {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full"
    />
  )
}
```

### Custom Message Renderer

Extend `ChatBubble.jsx`:

```jsx
{message.type === 'image' && (
  <img src={message.imageUrl} alt="Attachment" />
)}
```

### Custom Input Actions

Add buttons to `InputBar.jsx`:

```jsx
<motion.button
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95 }}
  className="p-2 text-gray-600 hover:text-blue-600 rounded-full"
>
  <Mic className="w-5 h-5" />
</motion.button>
```

---

## 📊 Performance Tips

### Optimize Re-renders
```jsx
const memoizedMessage = useMemo(() => message, [message.id])
```

### Lazy Load Components
```jsx
const AnimationShowcase = lazy(() => import('./components/AnimationShowcase'))
```

### Debounce Input
```jsx
const debouncedDraft = useDebounce(draft, 300)
```

---

## ♿ Accessibility

### ARIA Labels
All interactive elements have proper labels:

```jsx
<button aria-label="Send message">
  <Send />
</button>
```

### Keyboard Navigation
- Tab through interactive elements
- Enter to send
- Shift+Enter for new line

### Screen Reader Support
- Semantic HTML elements
- Role attributes
- Live regions for updates

---

## 🐛 Common Issues

### Issue: Animations not smooth
**Solution**: Ensure GPU acceleration:
```jsx
style={{ transform: 'translateZ(0)' }}
```

### Issue: Icons not rendering
**Solution**: Check import:
```jsx
import { Camera } from 'lucide-react'
```

### Issue: Tailwind classes not applying
**Solution**: Verify `tailwind.config.js` content paths:
```javascript
content: ["./src/**/*.{js,jsx,ts,tsx}"]
```

---

## 📚 Resources

- [Framer Motion API](https://www.framer.com/motion/)
- [Lucide Icons](https://lucide.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Docs](https://react.dev/)

---

**Last Updated**: 2026-04-19
**Version**: 1.0.0
