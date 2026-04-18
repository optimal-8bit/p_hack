# Voice Input Feature - Web Speech API Integration

## Overview
The chat interface now supports voice-to-text input using the Web Speech API, allowing users to speak their messages instead of typing them.

## Features

### 1. **Voice-to-Text Input**
- Click the microphone button to activate voice input
- Speak naturally and see your words transcribed in real-time
- Interim results show as you speak (in gray italic text)
- Final results are confirmed and added to the transcript
- Click send to insert the transcript into the chat input

### 2. **Audio Recording (Existing)**
- Right-click the microphone button to record audio messages
- Records audio as a file to be sent to the backend

## How to Use

### Voice-to-Text (New Feature)
1. Click the microphone icon in the chat input
2. Allow microphone permissions when prompted
3. Start speaking - you'll see "Listening..." indicator
4. Your speech will be transcribed in real-time
5. Click the microphone icon to pause/resume listening
6. Click the send button to insert the transcript into the chat input
7. Click X to cancel and close voice input

### Audio Recording (Existing Feature)
1. Right-click the microphone icon
2. Speak your message
3. Click send to submit the audio recording
4. Click stop to cancel

## Browser Support

The Web Speech API is supported in:
- ✅ Chrome (Desktop & Mobile)
- ✅ Edge (Desktop)
- ✅ Safari (Desktop & iOS)
- ❌ Firefox (Limited support)

## Technical Details

### Components
- **VoiceInput.jsx** - Main voice input component with Web Speech API integration
- **VoiceInput.css** - Styling for the voice input interface
- **ChatInput.jsx** - Updated to support both voice input and audio recording

### Web Speech API Features Used
- `SpeechRecognition` / `webkitSpeechRecognition`
- Continuous recognition mode
- Interim results for real-time feedback
- Multiple language support (default: en-US)

### Error Handling
The component handles various error scenarios:
- Browser not supported
- Microphone permission denied
- No microphone detected
- Network errors
- No speech detected

## Customization

### Change Language
You can modify the language by passing a `language` prop to the VoiceInput component:

```jsx
<VoiceInput 
  onTranscript={handleVoiceTranscript} 
  onClose={handleCloseVoiceInput}
  language="es-ES"  // Spanish
/>
```

Supported languages include:
- `en-US` - English (US)
- `en-GB` - English (UK)
- `es-ES` - Spanish
- `fr-FR` - French
- `de-DE` - German
- `it-IT` - Italian
- `pt-BR` - Portuguese (Brazil)
- `ja-JP` - Japanese
- `zh-CN` - Chinese (Simplified)
- And many more...

## User Experience

### Visual Feedback
- 🔴 Red pulsing dot when listening
- Gray text for interim (in-progress) transcription
- White text for confirmed transcription
- Error messages with warning icon
- Smooth animations and transitions

### Accessibility
- ARIA labels for all buttons
- Keyboard accessible
- Clear visual states
- Error messages are descriptive

## Future Enhancements

Possible improvements:
- Language selection dropdown
- Voice commands (e.g., "send message", "new line")
- Punctuation commands
- Voice activity detection
- Offline support with local models
- Custom wake words

## Troubleshooting

### "Speech recognition is not supported"
- Use Chrome, Edge, or Safari browser
- Update your browser to the latest version

### "Microphone permission denied"
- Check browser settings and allow microphone access
- On mobile, check system settings for browser permissions

### "No speech detected"
- Speak louder or closer to the microphone
- Check if microphone is working in other apps
- Ensure microphone is not muted

### Poor transcription accuracy
- Speak clearly and at a moderate pace
- Reduce background noise
- Use a better quality microphone
- Check if the correct language is selected
