# Mental Health Chatbot UI - ChatGPT-like Interface

## Overview
A fully functional, ChatGPT-inspired frontend for an AI-driven mental health chatbot built with React.js.

## Features Implemented

### ✅ Core Requirements

1. **Chat Interface Layout**
   - Full-screen responsive layout
   - Centered input box before first message
   - Switches to chat layout after first message
   - User messages aligned right, bot messages aligned left
   - Clean dark theme UI (similar to ChatGPT)

2. **Message Behavior**
   - Instant message display on send
   - Input field auto-clears after sending
   - Auto-scroll to latest message
   - Smooth animations and transitions

3. **Streaming / Typing Effect** ⭐
   - Character-by-character typewriter animation
   - Real-time streaming from backend API
   - Animated typing indicator (3 bouncing dots)
   - Blinking cursor during streaming

4. **API Integration**
   - Connected to backend endpoint: `POST /api/chat/stream`
   - Handles async streaming responses
   - Proper error handling
   - Abort controller for stopping generation

5. **Component Structure**
   ```
   src/
   ├── pages/
   │   └── MentalHealthChatPage.jsx    # Main chat page
   ├── components/
   │   └── chat/
   │       ├── ChatContainer.jsx        # Layout wrapper
   │       ├── MessageBubble.jsx        # Individual messages
   │       ├── ChatInput.jsx            # Input field + send button
   │       └── TypingIndicator.jsx     # Animated dots
   ├── styles/
   │   └── MentalHealthChat.css        # Complete styling
   └── services/
       └── chatService.js              # API integration (existing)
   ```

6. **UI/UX Details**
   - Rounded message bubbles with gradient backgrounds
   - Different colors for user (purple gradient) vs bot (dark gray)
   - Smooth fade-in animations
   - Scrollable chat window with custom scrollbar
   - Send button with hover effects
   - Enter-to-send support (Shift+Enter for new line)

7. **State Management**
   - React hooks (useState, useEffect, useRef)
   - Message history with structure:
     ```javascript
     {
       id: "unique-id",
       role: "user" | "bot",
       content: "message text",
       timestamp: "ISO string",
       streaming: boolean,
       error: boolean
     }
     ```

8. **Extra Features**
   - Input disabled while bot is responding
   - Loading state with typing indicator
   - Fully responsive for mobile screens
   - Auto-expanding textarea
   - Abort controller for stopping generation
   - Error handling with visual feedback

## Tech Stack
- **React.js** (functional components)
- **CSS** (custom styling with animations)
- **React Router** (routing)
- **Fetch API** (streaming support)

## Usage

### Access the Chat
Navigate to `/chat` route (protected route - requires authentication)

### Environment Variables
Set in `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_CHAT_STREAM_PATH=/chat/stream
```

### Backend API Expected Format

**Request:**
```javascript
POST /api/v1/chat/stream
Content-Type: multipart/form-data

{
  messages: [
    { role: "user", content: "Hello" },
    { role: "assistant", content: "Hi there!" }
  ]
}
```

**Response (Streaming):**
```
data: {"delta": "H"}
data: {"delta": "e"}
data: {"delta": "l"}
data: {"delta": "l"}
data: {"delta": "o"}
data: {"done": true}
```

## Key Components

### MentalHealthChatPage
Main page component that:
- Manages message state
- Handles API calls
- Controls streaming state
- Auto-scrolls to bottom

### MessageBubble
Displays individual messages with:
- Typewriter effect for bot messages (20ms per character)
- Blinking cursor during streaming
- Line break support
- Error state styling

### ChatInput
Input component with:
- Auto-expanding textarea
- Enter to send (Shift+Enter for new line)
- Disabled state during bot response
- Gradient send button with icon

### TypingIndicator
Animated 3-dot indicator shown while waiting for bot response

## Customization

### Adjust Typing Speed
In `MessageBubble.jsx`, line 20:
```javascript
}, 20) // Lower = faster, Higher = slower
```

### Change Theme Colors
In `MentalHealthChat.css`:
- Background: `#212121`
- User bubble: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Bot bubble: `#2f2f2f`
- Text: `#ececec`

### Modify Input Placeholder
In `ChatInput.jsx`, line 37:
```javascript
placeholder="Share what's on your mind..."
```

## Responsive Breakpoints
- Desktop: > 768px
- Tablet: 481px - 768px
- Mobile: < 480px

## Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance
- Smooth 60fps animations
- Efficient re-renders with React hooks
- Optimized scrolling behavior
- Minimal bundle size

## Future Enhancements
- [ ] Markdown rendering in messages
- [ ] Code syntax highlighting
- [ ] Message reactions
- [ ] Conversation history sidebar
- [ ] Export chat functionality
- [ ] Voice input support
- [ ] Multi-language support

## Notes
- The typewriter effect is applied ONLY to bot messages during streaming
- User messages appear instantly
- The welcome screen is shown only when no messages exist
- Input is centered before first message, then moves to bottom
- All animations are CSS-based for performance
