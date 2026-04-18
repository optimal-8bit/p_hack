# Integration Checklist

Use this checklist to verify the integration is working correctly.

## Pre-Flight Checks

### Backend Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created (optional but recommended)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Models downloaded (optional, `python scripts/download_models.py`)
- [ ] Backend directory exists: `mental_health_chatbot/backend/`

### Frontend Setup
- [ ] Node.js 16+ installed
- [ ] Dependencies installed (`npm install`)
- [ ] `.env` file exists in `react_web/`
- [ ] `.env` contains correct `VITE_API_BASE_URL=http://localhost:8000`
- [ ] Frontend directory exists: `react_web/`

## Startup Checks

### Backend Startup
- [ ] Backend starts without errors
- [ ] Console shows "Backend startup complete!"
- [ ] Can access http://localhost:8000
- [ ] Can access http://localhost:8000/docs
- [ ] Health endpoint works: http://localhost:8000/api/health

### Frontend Startup
- [ ] Frontend starts without errors
- [ ] Console shows "Local: http://localhost:5173"
- [ ] Can access http://localhost:5173
- [ ] No console errors in browser
- [ ] Page loads correctly

## Integration Checks

### Health Status
- [ ] Sidebar shows "Backend Status" section
- [ ] Status indicator is green (healthy)
- [ ] Status shows "HEALTHY"
- [ ] All models show checkmarks (✓)
- [ ] Models listed:
  - [ ] emotion_classifier
  - [ ] intent_classifier
  - [ ] translator_hi
  - [ ] translator_fr
  - [ ] translator_es
- [ ] Refresh button works
- [ ] Auto-refresh works (wait 30 seconds)

### Basic Chat
- [ ] Can type in message input
- [ ] Send button is enabled
- [ ] Can send message by clicking send button
- [ ] Can send message by pressing Enter
- [ ] Message appears in chat window
- [ ] Bot response appears with typewriter effect
- [ ] Response completes without errors
- [ ] Can send multiple messages in sequence

### Session Management
- [ ] Session ID is displayed (check browser DevTools > Application > Session Storage)
- [ ] Session ID persists after page reload
- [ ] Can clear session (if UI available)
- [ ] New session ID generated after clear

### Emotion Detection
Test these messages and verify emotion is detected:

- [ ] "I'm so happy today!" → Should detect: joy
- [ ] "I feel sad and lonely" → Should detect: sadness
- [ ] "I'm really angry about this" → Should detect: anger
- [ ] "I'm scared and anxious" → Should detect: fear
- [ ] "This is disgusting" → Should detect: disgust
- [ ] "Wow, that's surprising!" → Should detect: surprise
- [ ] "I'm feeling okay" → Should detect: neutral

### Intent Classification
Test these messages and verify intent is detected:

- [ ] "I'm feeling anxious and worried" → Intent: anxiety and panic
- [ ] "I feel so sad and depressed" → Intent: sadness and depression
- [ ] "I'm so stressed out" → Intent: stress and overwhelm
- [ ] "I feel so alone" → Intent: loneliness and isolation
- [ ] "I'm really frustrated and angry" → Intent: anger and frustration
- [ ] "I just need someone to talk to" → Intent: general emotional support

### Crisis Detection
⚠️ **Important**: Test carefully

- [ ] Type: "I want to hurt myself"
- [ ] Response indicates crisis detected
- [ ] Response provides helpline resources
- [ ] Response is empathetic and supportive
- [ ] Backend logs show crisis flag

### Multilingual Support
Test with non-English messages:

**Hindi:**
- [ ] Type: "मैं चिंतित महसूस कर रहा हूं"
- [ ] Response is in Hindi
- [ ] Emotion/intent detected correctly

**French:**
- [ ] Type: "Je me sens anxieux"
- [ ] Response is in French
- [ ] Emotion/intent detected correctly

**Spanish:**
- [ ] Type: "Me siento ansioso"
- [ ] Response is in Spanish
- [ ] Emotion/intent detected correctly

### UI/UX Checks
- [ ] Welcome screen displays before first message
- [ ] Messages scroll automatically
- [ ] User messages align right
- [ ] Bot messages align left
- [ ] Typewriter effect is smooth
- [ ] Loading indicator shows while processing
- [ ] Error messages display correctly (test by stopping backend)
- [ ] Sidebar is visible
- [ ] Sidebar can be toggled (on mobile)
- [ ] New chat button works
- [ ] Responsive on mobile (resize browser)

### Performance Checks
- [ ] First message response time < 5 seconds
- [ ] Subsequent messages response time < 3 seconds
- [ ] No lag in typing
- [ ] No lag in scrolling
- [ ] Health status updates smoothly
- [ ] No memory leaks (check DevTools > Memory)

### Error Handling
- [ ] Stop backend → Frontend shows "Backend Offline"
- [ ] Restart backend → Frontend reconnects automatically
- [ ] Send empty message → Nothing happens (validation works)
- [ ] Send very long message → Handled gracefully
- [ ] Network error → Error message displayed
- [ ] Retry after error → Works correctly

### Browser Compatibility
Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if on Mac)
- [ ] Mobile browser (Chrome/Safari)

### Console Checks
**Frontend Console (Browser DevTools):**
- [ ] No errors in console
- [ ] No warnings (or only expected warnings)
- [ ] Network requests show 200 status
- [ ] API responses are correct format

**Backend Console (Terminal):**
- [ ] No errors in logs
- [ ] Requests logged correctly
- [ ] Processing times reasonable
- [ ] No warnings (or only expected warnings)

## Advanced Checks

### API Endpoints
Test directly using browser or curl:

**Health Check:**
```bash
curl http://localhost:8000/api/health
```
- [ ] Returns JSON with status "healthy"
- [ ] Shows all models loaded

**Chat:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-123","message":"Hello"}'
```
- [ ] Returns JSON with response_text
- [ ] Includes emotion and intent
- [ ] Processing time is reasonable

**Supported Languages:**
```bash
curl http://localhost:8000/api/supported-languages
```
- [ ] Returns list of 4 languages
- [ ] Includes en, hi, fr, es

### Database Checks
- [ ] Database file created: `mental_health_chatbot/backend/chat_history.db`
- [ ] Chat turns are saved (check with SQLite browser)
- [ ] Crisis events are logged (if crisis detected)

### Mock Mode
- [ ] Set `VITE_USE_MOCK=true` in `.env`
- [ ] Restart frontend
- [ ] Chat works with mock responses
- [ ] No backend calls made
- [ ] Set back to `VITE_USE_MOCK=false`

## Production Readiness

### Security
- [ ] CORS configured correctly
- [ ] Input validation working
- [ ] No sensitive data in logs
- [ ] No API keys in frontend code
- [ ] Session IDs are random and unique

### Performance
- [ ] Response times acceptable
- [ ] No memory leaks
- [ ] Database queries optimized
- [ ] Models load efficiently

### Monitoring
- [ ] Health endpoint accessible
- [ ] Logs are informative
- [ ] Errors are caught and logged
- [ ] Can monitor backend status from frontend

### Documentation
- [ ] README_INTEGRATION.md exists
- [ ] INTEGRATION_GUIDE.md exists
- [ ] INTEGRATION_COMPLETE.md exists
- [ ] ARCHITECTURE_DIAGRAM.md exists
- [ ] Code comments are clear
- [ ] API documentation accessible

## Deployment Checks

### Backend Deployment
- [ ] Environment variables configured
- [ ] Production ASGI server configured
- [ ] Database path configured
- [ ] CORS updated for production domain
- [ ] Health check endpoint works
- [ ] Logs configured for production

### Frontend Deployment
- [ ] Build succeeds (`npm run build`)
- [ ] `dist/` folder created
- [ ] `.env` updated for production API URL
- [ ] Static files served correctly
- [ ] API calls work from production domain
- [ ] HTTPS configured (if applicable)

## Final Verification

### End-to-End Test
Complete this full workflow:

1. [ ] Start backend
2. [ ] Start frontend
3. [ ] Open http://localhost:5173
4. [ ] Check health status is healthy
5. [ ] Send message: "Hello"
6. [ ] Receive response
7. [ ] Send message: "I'm feeling anxious"
8. [ ] Verify emotion and intent detected
9. [ ] Refresh page
10. [ ] Verify session persists
11. [ ] Send another message
12. [ ] Verify context is maintained
13. [ ] Check backend logs
14. [ ] Check database has entries
15. [ ] Stop and restart backend
16. [ ] Verify frontend reconnects
17. [ ] All features still work

### Sign-Off
- [ ] All critical checks passed
- [ ] All features working
- [ ] No blocking issues
- [ ] Documentation complete
- [ ] Ready for use/demo

## Issue Tracking

If any checks fail, document here:

| Check | Status | Issue | Solution |
|-------|--------|-------|----------|
| Example | ❌ | Backend won't start | Install dependencies |
|  |  |  |  |
|  |  |  |  |

## Notes

Add any additional notes or observations:

```
[Your notes here]
```

---

## Quick Reference

### Start Servers
```bash
# Windows
start-dev.bat

# Linux/Mac
./start-dev.sh
```

### Access Points
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Stop Servers
- Close terminal windows
- Or press Ctrl+C in each terminal

---

**Checklist Version**: 1.0.0
**Last Updated**: 2024
