# Architecture - Mental Health Chatbot UI

## Component Hierarchy

```
App
└── AppRouter
    └── Route: /chat (Protected)
        └── MentalHealthChatPage
            └── ChatContainer
                ├── WelcomeScreen (conditional: !hasMessages)
                │   ├── <h1> Title
                │   └── <p> Subtitle
                │
                ├── MessagesContainer (conditional: hasMessages)
                │   ├── MessageBubble (user) ×N
                │   ├── MessageBubble (bot) ×N
                │   ├── TypingIndicator (conditional: isTyping)
                │   └── <div ref={messagesEndRef}> (scroll anchor)
                │
                └── ChatInput
                    ├── <form>
                    │   ├── <textarea> (auto-expand)
                    │   └── <button> Send (with icon)
                    └── <p> Hint text (conditional: !hasMessages)
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   MentalHealthChatPage                      │
│                                                             │
│  State:                                                     │
│  ├── messages: Message[]                                   │
│  ├── isTyping: boolean                                     │
│  └── inputDisabled: boolean                                │
│                                                             │
│  Refs:                                                      │
│  ├── messagesEndRef (scroll target)                        │
│  └── abortControllerRef (cancel streaming)                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Props
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      ChatContainer                          │
│  Props: { hasMessages, children }                           │
│  Renders: Layout wrapper with conditional classes           │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Children
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     MessageBubble                           │
│  Props: { role, content, streaming, error }                 │
│                                                             │
│  State:                                                     │
│  ├── displayedContent: string                              │
│  └── currentIndex: number                                  │
│                                                             │
│  Effect: Typewriter animation (20ms per char)              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    TypingIndicator                          │
│  Props: none                                                │
│  Renders: 3 animated dots                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       ChatInput                             │
│  Props: { onSend, disabled, hasMessages }                   │
│                                                             │
│  State:                                                     │
│  └── input: string                                          │
│                                                             │
│  Ref:                                                       │
│  └── textareaRef (auto-expand)                             │
│                                                             │
│  Events:                                                    │
│  ├── onChange → setInput                                   │
│  ├── onKeyDown → Enter to send                             │
│  └── onSubmit → onSend(input)                              │
└─────────────────────────────────────────────────────────────┘
```

## Message Flow

```
User Types Message
        │
        ▼
    Press Enter
        │
        ▼
ChatInput.handleSubmit()
        │
        ▼
MentalHealthChatPage.handleSendMessage(userInput)
        │
        ├─► Create userMessage object
        │   └─► Add to messages state (appears instantly)
        │
        ├─► Create botMessage object (empty, streaming: true)
        │   └─► Add to messages state
        │
        ├─► Set isTyping = true
        │   └─► TypingIndicator appears
        │
        ├─► Set inputDisabled = true
        │   └─► ChatInput disabled
        │
        └─► Call chatService.streamReply()
                │
                ├─► onToken(token)
                │   └─► Append token to botMessage.content
                │       └─► MessageBubble typewriter effect
                │           └─► Auto-scroll
                │
                ├─► onDone()
                │   ├─► Set streaming = false
                │   ├─► Set isTyping = false
                │   └─► Set inputDisabled = false
                │
                └─► onError(error)
                    ├─► Show error message
                    ├─► Set isTyping = false
                    └─► Set inputDisabled = false
```

## State Management

### Message Object Structure
```typescript
interface Message {
  id: string              // "msg-1234567890-abc123"
  role: 'user' | 'bot'    // Message sender
  content: string         // Message text
  timestamp: string       // ISO 8601 format
  streaming?: boolean     // True while bot is typing
  error?: boolean         // True if error occurred
}
```

### Component State

**MentalHealthChatPage:**
```javascript
const [messages, setMessages] = useState<Message[]>([])
const [isTyping, setIsTyping] = useState<boolean>(false)
const [inputDisabled, setInputDisabled] = useState<boolean>(false)
const messagesEndRef = useRef<HTMLDivElement>(null)
const abortControllerRef = useRef<AbortController | null>(null)
```

**MessageBubble:**
```javascript
const [displayedContent, setDisplayedContent] = useState<string>('')
const [currentIndex, setCurrentIndex] = useState<number>(0)
```

**ChatInput:**
```javascript
const [input, setInput] = useState<string>('')
const textareaRef = useRef<HTMLTextAreaElement>(null)
```

## API Integration

### Service Layer
```
chatService.streamReply()
        │
        ▼
apiClient.stream()
        │
        ▼
fetch(API_BASE_URL + path, {
  method: 'POST',
  body: FormData,
  headers: { Authorization: Bearer token }
})
        │
        ▼
ReadableStream
        │
        ├─► reader.read()
        ├─► decoder.decode()
        ├─► Parse JSON chunks
        └─► onMessage({ delta: "..." })
                │
                ▼
        onToken(delta)
                │
                ▼
        Update message content
```

### Request Format
```javascript
FormData {
  messages: JSON.stringify([
    { role: "user", content: "Hello" },
    { role: "assistant", content: "Hi!" },
    { role: "user", content: "How are you?" }
  ])
}
```

### Response Format
```
data: {"delta": "I"}
data: {"delta": "'"}
data: {"delta": "m"}
data: {"delta": " "}
data: {"delta": "g"}
data: {"delta": "o"}
data: {"delta": "o"}
data: {"delta": "d"}
data: {"done": true}
```

## Styling Architecture

### CSS Structure
```
MentalHealthChat.css
├── Page Layout
│   ├── .mental-health-chat-page
│   └── .chat-container
│
├── Welcome Screen
│   ├── .welcome-screen
│   └── .welcome-content
│
├── Messages
│   ├── .messages-container
│   ├── .message-bubble
│   │   ├── .user
│   │   └── .bot
│   └── .message-content
│
├── Typing Indicator
│   ├── .typing-indicator
│   └── .typing-dots
│
├── Input
│   ├── .chat-input-wrapper
│   ├── .chat-input-form
│   ├── .input-container
│   ├── .chat-textarea
│   └── .send-button
│
├── Animations
│   ├── @keyframes fadeIn
│   ├── @keyframes typingBounce
│   └── @keyframes blink
│
└── Responsive
    ├── @media (max-width: 768px)
    └── @media (max-width: 480px)
```

### CSS Variables (Implicit)
```css
/* Colors */
--bg-primary: #212121
--bg-secondary: #2f2f2f
--bg-tertiary: #3a3a3a
--text-primary: #ececec
--text-secondary: #b4b4b4
--text-muted: #888
--gradient-start: #667eea
--gradient-end: #764ba2

/* Spacing */
--spacing-xs: 0.5rem
--spacing-sm: 0.75rem
--spacing-md: 1rem
--spacing-lg: 1.5rem
--spacing-xl: 2rem

/* Border Radius */
--radius-sm: 0.25rem
--radius-md: 1.25rem
--radius-lg: 1.5rem
--radius-full: 50%

/* Transitions */
--transition-fast: 0.2s ease
--transition-normal: 0.3s ease
--transition-slow: 0.5s ease
```

## Animation Timeline

### Message Send Animation
```
0ms:    User types and presses Enter
        ├─► Input value captured
        └─► Form submit triggered

10ms:   User message created
        ├─► Added to messages array
        └─► Appears instantly (no animation)

20ms:   Bot message placeholder created
        ├─► Empty content
        ├─► streaming: true
        └─► Added to messages array

30ms:   Typing indicator appears
        └─► 3 dots bouncing animation starts

100ms:  API request sent
        └─► Waiting for first token

500ms:  First token received
        ├─► Typing indicator removed
        ├─► Bot message starts appearing
        └─► Typewriter effect begins

520ms:  Second character appears
540ms:  Third character appears
560ms:  Fourth character appears
...     (20ms per character)

5000ms: Last character appears
        ├─► Cursor stops blinking
        ├─► streaming: false
        └─► Input re-enabled
```

### Typewriter Effect Detail
```
Token received: "Hello"
        │
        ▼
Split into characters: ['H', 'e', 'l', 'l', 'o']
        │
        ▼
For each character:
  ├─► Wait 20ms
  ├─► Append to displayedContent
  ├─► Increment currentIndex
  └─► Re-render with cursor
        │
        ▼
All characters displayed
  └─► Remove cursor
```

## Performance Optimizations

### React Optimizations
```
1. useRef for DOM references
   └─► Avoids re-renders on scroll

2. Conditional rendering
   └─► Only render what's needed

3. Key props on lists
   └─► Efficient list updates

4. Cleanup on unmount
   └─► Prevent memory leaks

5. AbortController
   └─► Cancel pending requests
```

### CSS Optimizations
```
1. Transform/opacity animations
   └─► GPU accelerated

2. will-change hints
   └─► Prepare for animations

3. requestAnimationFrame
   └─► Smooth scrolling

4. CSS containment
   └─► Isolate layout calculations
```

## Error Handling

```
Error Occurs
        │
        ├─► Network Error
        │   ├─► Catch in try/catch
        │   ├─► Show error message in chat
        │   └─► Re-enable input
        │
        ├─► Abort Error
        │   ├─► User clicked stop
        │   ├─► Clean up gracefully
        │   └─► Show "Stopped by user"
        │
        └─► API Error
            ├─► Parse error response
            ├─► Show error message
            └─► Log to console
```

## Security Considerations

```
1. Authentication
   └─► Protected route (ProtectedRoute wrapper)
   └─► Auth token in API requests

2. Input Sanitization
   └─► React auto-escapes JSX
   └─► No dangerouslySetInnerHTML for user input

3. XSS Prevention
   └─► Content rendered as text
   └─► No eval() or innerHTML

4. CORS
   └─► Backend must allow origin
   └─► Credentials included in requests

5. Rate Limiting
   └─► Input disabled during response
   └─► Prevents spam
```

## Deployment Architecture

```
Development:
  Vite Dev Server (localhost:5173)
        │
        ▼
  Backend API (localhost:8000)

Production:
  Static Files (CDN/S3)
        │
        ▼
  Backend API (production URL)
        │
        ▼
  Database / AI Service
```

## File Size Breakdown

```
Components:
  MentalHealthChatPage.jsx    ~4 KB
  ChatContainer.jsx           ~1 KB
  MessageBubble.jsx           ~2 KB
  ChatInput.jsx               ~2 KB
  TypingIndicator.jsx         ~0.5 KB

Styling:
  MentalHealthChat.css        ~8 KB

Total (uncompressed):         ~17.5 KB
Total (gzipped):              ~6 KB
```

## Browser Compatibility

```
✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Mobile Safari (iOS 14+)
✅ Chrome Mobile (Android 10+)

Features Used:
  ├─► ES6+ (const, let, arrow functions)
  ├─► React Hooks
  ├─► Fetch API with streams
  ├─► CSS Grid/Flexbox
  ├─► CSS Animations
  └─► FormData
```

## Testing Strategy

```
Unit Tests:
  ├─► MessageBubble typewriter effect
  ├─► ChatInput validation
  └─► Message state management

Integration Tests:
  ├─► Message send flow
  ├─► Streaming response handling
  └─► Error handling

E2E Tests:
  ├─► Login → Chat → Send message
  ├─► Streaming response display
  └─► Mobile responsive behavior
```

---

This architecture provides a scalable, maintainable foundation for the mental health chatbot UI with clear separation of concerns and efficient data flow.
