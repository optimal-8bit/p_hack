# Upload Menu & Audio Input Feature ✅

## Overview

Enhanced the chat input with ChatGPT-like controls:
- **"+" Button** (left side) → Opens upload options dropdown
- **Mic Button** (right side) → Enables voice recording
- **Send Button** (rightmost) → Sends text messages

## Features Implemented

### 1. Upload Menu (+ Button)

**Location**: Left side of input bar

**Functionality**:
- Click to open dropdown menu
- Menu appears above input bar
- Closes when clicking outside
- Four upload options available

**Upload Options**:
1. **Upload Image** - Accepts: `image/*` (jpg, png, gif, etc.)
2. **Upload Video** - Accepts: `video/*` (mp4, webm, etc.)
3. **Upload File** - Accepts: `.txt, .doc, .docx`
4. **Upload PDF** - Accepts: `.pdf`

**UI Design**:
- Dark theme (`#202123` background)
- Gray border (`#707070`)
- Hover effect on items
- Icons from lucide-react
- Smooth fade-in animation

### 2. Audio Recording (Mic Button)

**Location**: Right side of input bar (before send button)

**Functionality**:
- Click to start recording
- Replaces input UI with recording interface
- Real-time timer display
- Stop and Send options

**Recording UI**:
- Red pulsing dot indicator
- Timer (MM:SS format)
- Stop button (square icon)
- Send button (arrow icon)
- Clean, minimal design

**Technical Implementation**:
- Uses `MediaRecorder API`
- Requests microphone permission
- Records in `audio/webm` format
- Tracks recording duration
- Properly cleans up resources

### 3. Updated Input Layout

**New Layout**:
```
[ + ]  [ Text Input Field................ ]  [ Mic ]  [ Send ]
```

**Spacing**:
- Proper gap between buttons (0.5rem)
- Buttons have hover effects
- Icons are 20px (18px on mobile)
- Consistent padding and alignment

## Components Created

### 1. UploadMenu.jsx

**Location**: `src/components/chat/UploadMenu.jsx`

**Props**:
- `isOpen` (boolean) - Controls menu visibility
- `onClose` (function) - Called when menu should close
- `onFileSelect` (function) - Called when file is selected

**Features**:
- Click-outside detection
- Hidden file inputs
- File type validation
- Smooth animations

**Usage**:
```jsx
<UploadMenu
  isOpen={isUploadMenuOpen}
  onClose={() => setIsUploadMenuOpen(false)}
  onFileSelect={handleFileSelect}
/>
```

### 2. AudioRecorder.jsx

**Location**: `src/components/chat/AudioRecorder.jsx`

**Props**:
- `onSendAudio` (function) - Called with audio blob and duration
- `onCancel` (function) - Called when recording is cancelled

**Features**:
- Auto-starts recording on mount
- Real-time timer
- Stop and send controls
- Proper cleanup on unmount
- Error handling for permissions

**Usage**:
```jsx
<AudioRecorder
  onSendAudio={handleSendAudio}
  onCancel={handleCancelRecording}
/>
```

### 3. Updated ChatInput.jsx

**Location**: `src/components/chat/ChatInput.jsx`

**New State**:
```javascript
const [isUploadMenuOpen, setIsUploadMenuOpen] = useState(false)
const [isRecording, setIsRecording] = useState(false)
```

**New Handlers**:
- `handleFileSelect(file, type)` - Processes uploaded files
- `handleSendAudio(audioBlob, duration)` - Processes recorded audio
- `handleStartRecording()` - Starts audio recording
- `handleCancelRecording()` - Cancels recording

## File Structure

```
src/
├── components/
│   └── chat/
│       ├── ChatInput.jsx          (updated)
│       ├── UploadMenu.jsx         (new)
│       └── AudioRecorder.jsx      (new)
└── styles/
    └── MentalHealthChat.css       (updated)
```

## Dependencies Added

```bash
npm install lucide-react
```

**Icons Used**:
- `Plus` - Upload menu button
- `Mic` - Audio recording button
- `Square` - Stop recording
- `Send` - Send audio
- `Image` - Upload image option
- `Video` - Upload video option
- `FileText` - Upload file option
- `FileType` - Upload PDF option

## CSS Updates

**New Styles Added**:
- `.input-icon-button` - Styling for + and Mic buttons
- `.animate-fadeIn` - Fade-in animation for upload menu
- `.animate-pulse` - Pulse animation for recording indicator
- Updated `.input-container` with gap
- Mobile responsive adjustments

## User Flow

### Upload File Flow:

1. User clicks **"+"** button
2. Dropdown menu appears with 4 options
3. User selects option (e.g., "Upload Image")
4. File picker opens
5. User selects file
6. File is processed (currently shows placeholder message)
7. Menu closes automatically

### Audio Recording Flow:

1. User clicks **Mic** button
2. Browser requests microphone permission
3. Recording UI replaces input
4. Timer starts counting
5. User can:
   - Click **Stop** → Cancel recording
   - Click **Send** → Send audio message
6. Recording stops and cleans up
7. Input returns to normal state

## Current Behavior (Placeholder)

### File Upload:
```javascript
// Currently sends placeholder message
const fileMessage = `[Uploaded ${type}: ${file.name}]`
onSend(fileMessage)
```

**TODO**: Implement actual file upload to backend

### Audio Recording:
```javascript
// Currently sends placeholder message
const audioMessage = `[Audio message: ${duration}s]`
onSend(audioMessage)
```

**TODO**: Implement actual audio upload to backend

## Backend Integration (TODO)

### File Upload Endpoint:
```javascript
// Example implementation
const handleFileSelect = async (file, type) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', type)
  
  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData,
  })
  
  const data = await response.json()
  onSend(`[File uploaded: ${data.url}]`)
}
```

### Audio Upload Endpoint:
```javascript
// Example implementation
const handleSendAudio = async (audioBlob, duration) => {
  const formData = new FormData()
  formData.append('audio', audioBlob, 'recording.webm')
  formData.append('duration', duration)
  
  const response = await fetch('/api/upload-audio', {
    method: 'POST',
    body: formData,
  })
  
  const data = await response.json()
  onSend(`[Audio: ${data.url}]`)
}
```

## Browser Compatibility

### MediaRecorder API:
- ✅ Chrome 47+
- ✅ Firefox 25+
- ✅ Safari 14.1+
- ✅ Edge 79+

### File Input:
- ✅ All modern browsers

## Error Handling

### Microphone Permission Denied:
```javascript
try {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  // ... recording logic
} catch (error) {
  console.error('Error accessing microphone:', error)
  alert('Could not access microphone. Please check permissions.')
  onCancel()
}
```

### File Selection Cancelled:
- Menu simply closes
- No error shown
- User can try again

## Testing

```bash
npm run dev
```

### Test Upload Menu:
1. Click "+" button
2. Verify dropdown appears
3. Click each option
4. Verify file picker opens with correct filters
5. Select a file
6. Verify placeholder message appears in chat
7. Click outside menu to close

### Test Audio Recording:
1. Click Mic button
2. Allow microphone permission
3. Verify recording UI appears
4. Verify timer counts up
5. Click Stop → Verify returns to input
6. Click Mic again
7. Click Send → Verify audio message appears

### Test Responsive Design:
1. Resize browser to mobile width
2. Verify buttons are properly sized
3. Verify upload menu is readable
4. Verify recording UI fits properly

## Keyboard Shortcuts

**Existing**:
- `Enter` → Send message
- `Shift + Enter` → New line

**Note**: Upload and audio features require mouse/touch interaction

## Accessibility

- All buttons have `aria-label` attributes
- Keyboard navigation supported
- Focus states visible
- Color contrast meets WCAG standards

## Performance Considerations

- Upload menu only renders when open
- Audio recording cleans up resources properly
- File inputs are hidden (not rendered multiple times)
- Smooth animations (CSS-based)

## Mobile Responsiveness

**Adjustments**:
- Smaller button padding on mobile
- Icon size reduced to 18px
- Upload menu width adjusted
- Recording UI fits in smaller screens

## Known Limitations

1. **File Upload**: Currently placeholder only (needs backend)
2. **Audio Upload**: Currently placeholder only (needs backend)
3. **Audio Format**: Records in `audio/webm` (may need conversion)
4. **File Size**: No size limit validation yet
5. **Multiple Files**: Only single file upload supported

## Future Enhancements

- [ ] Implement actual file upload to backend
- [ ] Implement actual audio upload to backend
- [ ] Add file size validation
- [ ] Add upload progress indicator
- [ ] Support multiple file selection
- [ ] Add audio playback preview before sending
- [ ] Add file type icons in chat messages
- [ ] Add drag-and-drop file upload
- [ ] Add paste image from clipboard
- [ ] Convert audio to MP3 format

## Summary

✅ **"+" Upload Menu** - Fully functional UI (backend integration pending)
✅ **Mic Audio Recording** - Fully functional UI (backend integration pending)
✅ **ChatGPT-like Design** - Clean, minimal, dark theme
✅ **Smooth Animations** - Fade-in, pulse effects
✅ **Responsive Design** - Works on all screen sizes
✅ **Error Handling** - Graceful permission handling
✅ **Accessibility** - ARIA labels, keyboard support

The UI is complete and ready for backend integration! 🎉
