# Mental Health Chatbot UI - Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd p_hack/react_web
npm install
```

### 2. Configure Environment
Create `.env` file in `react_web/` directory:

```env
# Backend API URL
VITE_API_BASE_URL=http://localhost:8000/api/v1

# Chat streaming endpoint (optional, defaults to /chat/stream)
VITE_CHAT_STREAM_PATH=/chat/stream
```

### 3. Start Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Structure

```
react_web/
├── src/
│   ├── pages/
│   │   ├── MentalHealthChatPage.jsx    # 🆕 Main chat interface
│   │   ├── DashboardPage.jsx           # Dashboard with chat link
│   │   ├── LoginPage.jsx
│   │   └── RegisterPage.jsx
│   ├── components/
│   │   ├── chat/                       # 🆕 Chat components
│   │   │   ├── ChatContainer.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   └── TypingIndicator.jsx
│   │   └── ProtectedRoute.jsx
│   ├── styles/
│   │   └── MentalHealthChat.css        # 🆕 Chat styling
│   ├── services/
│   │   ├── chatService.js              # API integration
│   │   └── authService.js
│   ├── routes/
│   │   └── AppRouter.jsx               # Updated with /chat route
│   └── lib/
│       └── apiClient.js                # HTTP client with streaming
├── .env                                 # Environment variables
├── package.json
├── CHAT_README.md                       # 🆕 Feature documentation
└── SETUP_GUIDE.md                       # 🆕 This file
```

## Routes

| Route | Description | Protected |
|-------|-------------|-----------|
| `/` | Intro/Landing page | No |
| `/login` | Login page | No |
| `/register` | Registration page | No |
| `/dashboard` | User dashboard | Yes |
| `/chat` | Mental Health Chat | Yes ✅ |

## Usage Flow

1. **Register/Login** → Navigate to `/login` or `/register`
2. **Access Dashboard** → After login, you'll be at `/dashboard`
3. **Open Chat** → Click "Open Mental Health Chat" button
4. **Start Chatting** → Type your message and press Enter

## Features

### 🎨 UI/UX
- ChatGPT-like dark theme
- Centered input before first message
- Smooth transitions and animations
- Responsive design (mobile-friendly)
- Auto-scrolling to latest message

### ⚡ Streaming
- Real-time character-by-character display
- Typewriter effect (20ms per character)
- Blinking cursor during streaming
- Animated typing indicator

### 🔧 Functionality
- Enter to send, Shift+Enter for new line
- Auto-expanding textarea
- Input disabled during bot response
- Error handling with visual feedback
- Abort controller to stop generation

## Backend API Requirements

Your backend should provide a streaming endpoint:

### Endpoint
```
POST /api/v1/chat/stream
```

### Request Format
```javascript
Content-Type: multipart/form-data

FormData:
  messages: JSON.stringify([
    { role: "user", content: "Hello" },
    { role: "assistant", content: "Hi!" },
    { role: "user", content: "How are you?" }
  ])
```

### Response Format (Server-Sent Events)
```
data: {"delta": "I"}
data: {"delta": "'"}
data: {"delta": "m"}
data: {"delta": " "}
data: {"delta": "d"}
data: {"delta": "o"}
data: {"delta": "i"}
data: {"delta": "n"}
data: {"delta": "g"}
data: {"delta": " "}
data: {"delta": "w"}
data: {"delta": "e"}
data: {"delta": "l"}
data: {"delta": "l"}
data: {"done": true}
```

Alternative response formats supported:
- `{"token": "text"}`
- `{"content": "text"}`
- `{"text": "text"}`

## Customization

### Change Typing Speed
Edit `src/components/chat/MessageBubble.jsx`:
```javascript
setTimeout(() => {
  // ...
}, 20) // Change this value (milliseconds per character)
```

### Modify Theme Colors
Edit `src/styles/MentalHealthChat.css`:
```css
/* Background */
.mental-health-chat-page {
  background: #212121; /* Change this */
}

/* User message bubble */
.message-bubble.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Bot message bubble */
.message-bubble.bot .message-content {
  background: #2f2f2f;
}
```

### Update Welcome Message
Edit `src/pages/MentalHealthChatPage.jsx`:
```javascript
<h1>Mental Health Support</h1>
<p>I'm here to listen and support you. How are you feeling today?</p>
```

## Testing Without Backend

If your backend isn't ready, you can test with a mock:

1. Create `src/services/mockChatService.js`:
```javascript
export const mockChatService = {
  async streamReply({ messages, signal, onToken, onDone }) {
    const response = "I'm a mock response. Your backend will provide real responses."
    
    for (let i = 0; i < response.length; i++) {
      if (signal?.aborted) break
      
      await new Promise(resolve => setTimeout(resolve, 50))
      onToken(response[i])
    }
    
    onDone({ done: true })
  }
}
```

2. In `MentalHealthChatPage.jsx`, temporarily import mock:
```javascript
import { mockChatService as chatService } from '../services/mockChatService'
```

## Troubleshooting

### Issue: "Network Error" or "Failed to fetch"
**Solution:** Check that:
- Backend is running
- `VITE_API_BASE_URL` is correct in `.env`
- CORS is enabled on backend
- Endpoint path matches `VITE_CHAT_STREAM_PATH`

### Issue: Messages not streaming
**Solution:** Verify backend response format:
- Should be Server-Sent Events (SSE)
- Each chunk should have `delta`, `token`, `content`, or `text` field
- Content-Type should allow streaming

### Issue: "401 Unauthorized"
**Solution:** 
- Make sure you're logged in
- Check that auth token is being sent (see Network tab)
- Verify token hasn't expired

### Issue: Typing effect too fast/slow
**Solution:** Adjust timeout in `MessageBubble.jsx` (line 20)

### Issue: Input not clearing after send
**Solution:** Check that `setInput('')` is being called in `handleSendMessage`

## Development Commands

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Browser DevTools Tips

### Check Streaming
1. Open DevTools → Network tab
2. Send a message
3. Look for `/chat/stream` request
4. Click on it → Response tab
5. You should see chunks arriving in real-time

### Debug State
Add React DevTools extension and inspect:
- `messages` state in `MentalHealthChatPage`
- `isTyping` and `inputDisabled` states

## Performance Tips

1. **Large conversations:** Consider implementing pagination or limiting message history
2. **Slow streaming:** Adjust typewriter speed or disable it for very long responses
3. **Mobile performance:** Test on actual devices, not just browser emulation

## Security Notes

- All routes under `/chat` are protected (require authentication)
- Auth token is automatically included in API requests
- Input is sanitized before display
- XSS protection via React's built-in escaping

## Next Steps

1. ✅ Basic chat interface working
2. ✅ Streaming with typewriter effect
3. ✅ Responsive design
4. 🔲 Add markdown rendering (optional)
5. 🔲 Add conversation history sidebar (optional)
6. 🔲 Add message reactions (optional)
7. 🔲 Add voice input (optional)

## Support

For issues or questions:
1. Check `CHAT_README.md` for feature documentation
2. Review backend API logs
3. Check browser console for errors
4. Verify environment variables

## License

Part of the Mental Health Chatbot project.
