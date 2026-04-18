# Mock Backend Guide - Testing Without Backend

## 🎯 Overview

The chatbot now includes a **mock backend system** for testing and demo purposes. This allows you to test the full streaming experience without needing the backend API running.

---

## ✅ What Was Added

### 1. Mock Responses System
- **File:** `src/mock/mockResponses.js`
- **50+ predefined responses** covering:
  - Greetings (hello, hi, good morning, etc.)
  - Emotional states (sad, stressed, anxious, happy, etc.)
  - Coping mechanisms (help me, breathing exercises, etc.)
  - Self-care topics
  - Crisis support
  - Relationship issues
  - Professional help resources

### 2. Intelligent Matching
- **Direct match:** Exact phrase matching
- **Partial match:** Keyword detection in user input
- **Fallback responses:** 6 generic supportive responses for unmatched queries

### 3. Streaming Simulation
- Character-by-character typewriter effect
- 20ms delay per character (adjustable)
- Maintains the same UX as real backend streaming

### 4. Centered Chat Layout
- **Max width:** 800px (readable width)
- **Centered:** Horizontally centered with margins
- **Responsive:** Adapts to screen size

---

## 🚀 How to Use

### Enable Mock Mode

**Option 1: Environment Variable (Recommended)**
```bash
# In .env file
VITE_USE_MOCK=true
```

**Option 2: Code Toggle**
```javascript
// In src/mock/mockResponses.js
export const USE_MOCK = true
```

### Disable Mock Mode (Use Real Backend)
```bash
# In .env file
VITE_USE_MOCK=false
```

---

## 📝 Example Queries

### Greetings
```
User: "hello"
Bot: "Hey, I am great! How can I help you today?"

User: "good morning"
Bot: "Good morning! Hope you have a peaceful day ahead."
```

### Emotional Support
```
User: "i feel sad"
Bot: "I'm sorry you're feeling that way. Do you want to talk about it?"

User: "i am stressed"
Bot: "Try taking a deep breath. What's causing the stress?"

User: "i feel anxious"
Bot: "You're not alone. Let's take it one step at a time. What's making you feel anxious?"
```

### Coping Mechanisms
```
User: "help me"
Bot: "I'm here to help. Can you tell me more about what you're going through?"

User: "breathing exercises"
Bot: "Great choice! Try this: Breathe in slowly for 4 counts, hold for 4, breathe out for 4, hold for 4. Repeat 4 times. How do you feel?"
```

### Crisis Support
```
User: "suicide"
Bot: "I'm really concerned about you. Please reach out to a crisis helpline immediately: National Suicide Prevention Lifeline: 988 or 1-800-273-8255. You matter, and help is available."
```

### Gratitude
```
User: "thank you"
Bot: "You're welcome. I'm always here for you."
```

### About the Bot
```
User: "who are you"
Bot: "I'm your mental wellness assistant, here to support you and listen without judgment."
```

---

## 🎨 Centered Layout

### Before
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  Chat stretches full width (too wide to read)         │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### After
```
┌────────────────────────────────────────────────────────┐
│        ┌──────────────────────────┐                    │
│        │  Centered chat area      │                    │
│        │  Max width: 800px        │                    │
│        │  Easy to read            │                    │
│        └──────────────────────────┘                    │
└────────────────────────────────────────────────────────┘
```

**Benefits:**
- ✅ More readable (optimal line length)
- ✅ Looks professional on large screens
- ✅ Similar to ChatGPT/Gemini layout
- ✅ Equal margins on both sides

---

## 🔧 Technical Details

### Mock Response Matching

```javascript
// 1. Direct match
"hello" → "Hey, I am great! How can I help you today?"

// 2. Partial match (keyword detection)
"i feel very sad today" → Contains "sad" → Sad response

// 3. Fallback (no match)
"random text" → Random supportive response
```

### Streaming Simulation

```javascript
async function simulateStreaming(text, onToken, delay = 20) {
  for (let i = 0; i < text.length; i++) {
    await new Promise(resolve => setTimeout(resolve, delay))
    onToken(text[i])  // Send one character at a time
  }
}
```

**Delay Options:**
- `10ms` - Very fast
- `20ms` - Default (natural reading speed)
- `30ms` - Slower, more dramatic
- `50ms` - Very slow

### Chat Service Integration

```javascript
// In chatService.js
if (USE_MOCK) {
  // Use mock responses with streaming
  const mockResponse = getMockResponse(userInput)
  await simulateStreaming(mockResponse, onToken, 20)
} else {
  // Use real backend API
  await apiClient.stream(...)
}
```

---

## 📁 File Structure

```
src/
├── mock/
│   └── mockResponses.js          # Mock responses + streaming
├── services/
│   └── chatService.js            # Updated with mock support
└── styles/
    └── MentalHealthChat.css      # Updated with centered layout
```

---

## 🎯 Configuration

### Environment Variables

```bash
# .env file

# Use mock responses (true/false)
VITE_USE_MOCK=true

# Backend API URL (used when mock is disabled)
VITE_API_BASE_URL=http://localhost:8000/api/v1

# Chat streaming endpoint
VITE_CHAT_STREAM_PATH=/chat/stream
```

### Adjust Streaming Speed

In `src/mock/mockResponses.js`:
```javascript
export async function simulateStreaming(text, onToken, delay = 20) {
  // Change delay value (in milliseconds)
  // Lower = faster, Higher = slower
}
```

Or in `chatService.js`:
```javascript
await simulateStreaming(mockResponse, onToken, 30)  // 30ms delay
```

### Adjust Chat Width

In `src/styles/MentalHealthChat.css`:
```css
.chat-container {
  max-width: 800px;  /* Change this value */
  /* Options: 700px, 800px, 900px, 1000px */
}
```

---

## 🧪 Testing

### Test Mock Responses

1. **Start the app:**
   ```bash
   npm run dev
   ```

2. **Ensure mock is enabled:**
   ```bash
   # Check .env file
   VITE_USE_MOCK=true
   ```

3. **Test queries:**
   - Type: "hello"
   - Type: "i feel sad"
   - Type: "help me"
   - Type: "thank you"

4. **Observe:**
   - ✅ Responses appear character-by-character
   - ✅ Typing indicator shows before response
   - ✅ Chat is centered with margins
   - ✅ No backend errors

### Test Real Backend

1. **Disable mock:**
   ```bash
   # In .env
   VITE_USE_MOCK=false
   ```

2. **Start backend:**
   ```bash
   # Start your Python backend
   python -m uvicorn main:app --reload
   ```

3. **Test:**
   - Send messages
   - Should connect to real API

---

## 📊 Mock Response Categories

### Emotional States (25 responses)
- Sadness: 5 responses
- Stress: 4 responses
- Anxiety: 5 responses
- Anger: 3 responses
- Positive: 4 responses
- Loneliness: 1 response
- Depression: 1 response
- Sleep issues: 1 response
- Panic: 1 response

### Support & Coping (10 responses)
- Help requests: 3 responses
- Coping strategies: 2 responses
- Breathing exercises: 1 response
- Self-care: 2 responses
- Meditation: 1 response
- Breaks: 1 response

### Relationships (3 responses)
- Relationship problems
- Family issues
- Friend problems

### Professional Help (4 responses)
- Therapy
- Therapist
- Counseling
- Medication

### Crisis (4 responses)
- Suicide
- Self-harm
- Crisis support
- Emergency resources

### Greetings & Goodbyes (11 responses)
- Hello variations: 3
- Good morning/afternoon/evening: 3
- How are you: 3
- Goodbye: 4

### About Bot (4 responses)
- Who are you
- What are you
- Can you help
- Are you real

### Gratitude (3 responses)
- Thank you
- Thanks
- Appreciate it

---

## 🎨 Layout Specifications

### Chat Container
```css
max-width: 800px;
margin: 0 auto;
padding: 0 1rem;
```

### Responsive Breakpoints
```css
Desktop (>1024px):  max-width: 800px
Tablet (768-1024):  max-width: 700px
Mobile (<768px):    max-width: 100%
```

### Message Bubbles
```css
User:  max-width: 65%, right-aligned
Bot:   max-width: 65%, left-aligned
```

---

## 🔄 Switching Between Mock and Real Backend

### Development Workflow

**Phase 1: Frontend Development (Mock)**
```bash
VITE_USE_MOCK=true
# Develop UI, test interactions, no backend needed
```

**Phase 2: Integration Testing (Real)**
```bash
VITE_USE_MOCK=false
# Test with real backend, verify API integration
```

**Phase 3: Demo/Presentation (Mock)**
```bash
VITE_USE_MOCK=true
# Show features without backend dependency
```

**Phase 4: Production (Real)**
```bash
VITE_USE_MOCK=false
# Use real backend in production
```

---

## 🐛 Troubleshooting

### Mock Not Working

**Issue:** Responses not appearing
**Solution:**
1. Check `.env` file: `VITE_USE_MOCK=true`
2. Restart dev server: `npm run dev`
3. Clear browser cache
4. Check console for errors

### Chat Not Centered

**Issue:** Chat stretches full width
**Solution:**
1. Check CSS is loaded
2. Verify `.chat-container` has `max-width: 800px`
3. Check browser DevTools for overriding styles

### Streaming Too Fast/Slow

**Issue:** Text appears too quickly or slowly
**Solution:**
```javascript
// In mockResponses.js or chatService.js
await simulateStreaming(text, onToken, 20)  // Adjust this value
```

### Backend Errors When Mock Disabled

**Issue:** API errors when `VITE_USE_MOCK=false`
**Solution:**
1. Ensure backend is running
2. Check `VITE_API_BASE_URL` in `.env`
3. Verify CORS settings on backend
4. Check Network tab in DevTools

---

## 📝 Adding Custom Responses

### Add New Response

In `src/mock/mockResponses.js`:
```javascript
export const mockResponses = {
  // ... existing responses
  
  // Add your custom response
  "custom query": "Your custom response here",
  "another query": "Another response",
}
```

### Add Response Category

```javascript
// Mental health topics
"meditation": "Meditation can be very calming...",
"yoga": "Yoga combines physical and mental wellness...",
"exercise": "Exercise is great for mental health...",

// Daily activities
"work": "Work-life balance is important...",
"sleep": "Good sleep is essential for mental health...",
```

### Modify Default Responses

```javascript
const defaultResponses = [
  "I'm here to listen. Tell me more.",
  "Your custom default response",
  "Another fallback message",
]
```

---

## ✨ Benefits

### For Development
- ✅ No backend dependency
- ✅ Fast iteration
- ✅ Consistent responses
- ✅ Easy testing

### For Demo/Presentation
- ✅ Works offline
- ✅ Predictable responses
- ✅ No API failures
- ✅ Professional appearance

### For Testing
- ✅ Test UI without backend
- ✅ Test streaming effect
- ✅ Test error handling
- ✅ Test responsive design

### For Users
- ✅ Centered, readable layout
- ✅ Professional appearance
- ✅ Smooth streaming experience
- ✅ Helpful responses

---

## 🎯 Summary

**Mock Backend:**
- ✅ 50+ predefined responses
- ✅ Intelligent keyword matching
- ✅ Streaming simulation (20ms/char)
- ✅ Fallback responses
- ✅ Easy toggle (env variable)

**Centered Layout:**
- ✅ Max width: 800px
- ✅ Horizontally centered
- ✅ Equal margins
- ✅ Responsive design

**Configuration:**
- ✅ Environment variable toggle
- ✅ Adjustable streaming speed
- ✅ Customizable responses
- ✅ Easy to extend

---

## 🚀 Quick Start

```bash
# 1. Enable mock mode
# Edit .env: VITE_USE_MOCK=true

# 2. Start app
npm run dev

# 3. Test queries
# Try: "hello", "i feel sad", "help me"

# 4. Observe
# - Centered chat layout
# - Streaming responses
# - No backend needed!
```

---

**Status: COMPLETE AND READY TO USE** 🎉

You can now test the chatbot without any backend dependency!
