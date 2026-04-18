# 🚀 Quick Start - Mental Health Chatbot UI

## Get Running in 3 Steps

### Step 1: Install
```bash
cd p_hack/react_web
npm install
```

### Step 2: Configure
Create `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Step 3: Run
```bash
npm run dev
```

Open `http://localhost:5173` → Click "START CHAT" (no login required!)

---

## ✅ What You Get

- **ChatGPT-like UI** with dark theme
- **Streaming responses** with typewriter effect (20ms per character)
- **Typing indicator** (animated dots)
- **Responsive design** (mobile, tablet, desktop)
- **Protected route** (requires authentication)

---

## 🎯 Key Features

### Before First Message
```
┌─────────────────────────────┐
│   Mental Health Support     │
│   I'm here to listen...     │
│                             │
│  ┌─────────────────────┐   │
│  │ Type here...        │ ➤ │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

### During Conversation
```
┌─────────────────────────────┐
│          ┌──────────────┐   │
│          │ User message │   │ Right
│          └──────────────┘   │
│                             │
│  ┌──────────────────────┐  │
│  │ Bot response here... │  │ Left
│  └──────────────────────┘  │
│                             │
│  ┌─────┐                    │
│  │ ● ● ● │  Typing...       │
│  └─────┘                    │
├─────────────────────────────┤
│  ┌─────────────────────┐   │
│  │ Type here...        │ ➤ │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

---

## 📁 What Was Created

### Components
- `src/pages/MentalHealthChatPage.jsx` - Main page
- `src/components/chat/ChatContainer.jsx` - Layout
- `src/components/chat/MessageBubble.jsx` - Messages with typewriter
- `src/components/chat/ChatInput.jsx` - Input field
- `src/components/chat/TypingIndicator.jsx` - Loading dots

### Styling
- `src/styles/MentalHealthChat.css` - Complete dark theme

### Routes
- `/chat` - Mental health chat (protected)

---

## 🔌 Backend Requirements

Your backend should provide:

**Endpoint:** `POST /api/v1/chat/stream`

**Request:**
```javascript
FormData {
  messages: JSON.stringify([
    { role: "user", content: "Hello" }
  ])
}
```

**Response (streaming):**
```
data: {"delta": "H"}
data: {"delta": "i"}
data: {"done": true}
```

---

## 🎨 Customization

### Change Typing Speed
`src/components/chat/MessageBubble.jsx` line 20:
```javascript
}, 20) // Change this number (ms per character)
```

### Change Colors
`src/styles/MentalHealthChat.css`:
```css
/* User bubble */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Bot bubble */
background: #2f2f2f;
```

### Change Welcome Text
`src/pages/MentalHealthChatPage.jsx`:
```javascript
<h1>Mental Health Support</h1>
<p>Your custom message here</p>
```

---

## 🐛 Troubleshooting

**"Network Error"**
- Check backend is running
- Verify `VITE_API_BASE_URL` in `.env`
- Check CORS settings

**"401 Unauthorized"**
- Make sure you're logged in
- Check auth token in Network tab

**Messages not streaming**
- Verify backend response format
- Check for `delta`, `token`, or `content` field

**Typing too fast/slow**
- Adjust timeout in `MessageBubble.jsx`

---

## 📚 Documentation

- **`IMPLEMENTATION_SUMMARY.md`** - What was built
- **`SETUP_GUIDE.md`** - Detailed setup instructions
- **`CHAT_README.md`** - Feature documentation
- **`FEATURES.md`** - Design specifications

---

## ✨ Features Checklist

✅ ChatGPT-like layout  
✅ Centered input before first message  
✅ Streaming typewriter effect  
✅ Typing indicator  
✅ Dark theme  
✅ Responsive design  
✅ Auto-scroll  
✅ Enter to send  
✅ Input disabled during response  
✅ Error handling  
✅ Mobile friendly  

---

## 🎯 Next Steps

1. ✅ **Setup complete** - Follow steps above
2. 🔲 **Test with backend** - Send real messages
3. 🔲 **Customize** - Adjust colors, text, speed
4. 🔲 **Deploy** - Build and deploy to production

---

## 💡 Tips

- Press **Enter** to send, **Shift+Enter** for new line
- Input auto-expands as you type
- Scroll is automatic
- Works on mobile, tablet, desktop
- Dark theme reduces eye strain

---

**Ready to go!** 🚀

For detailed information, see `SETUP_GUIDE.md` or `CHAT_README.md`.
