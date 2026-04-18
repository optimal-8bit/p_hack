# Video Background Implementation Guide

## Overview

The chatbot UI now features a dynamic video background that activates only while the bot is generating/streaming a response. This creates an engaging, professional visual experience without distracting from the chat content.

## Implementation Summary

### ✅ Completed Components

1. **VideoBackground Component** (`src/components/VideoBackground.jsx`)
   - Handles video playback with smooth fade-in/out transitions
   - Applies blur (12px) and opacity (40%) effects
   - Manages video loading and error states
   - Automatically plays/pauses based on streaming state

2. **Video Helper Utility** (`src/utils/videoHelper.js`)
   - Manages video selection (3 videos: video1.mp4, video2.mp4, video3.mp4)
   - Provides `getRandomVideo()` function for random selection
   - Includes preload and validation utilities

3. **MentalHealthChatPage Integration** (`src/pages/MentalHealthChatPage.jsx`)
   - Added state management: `isStreaming` and `currentVideo`
   - Triggers video on bot response start
   - Clears video on response completion or error
   - Integrated VideoBackground component in render

4. **Styling** (`src/components/VideoBackground.css`)
   - Fixed positioning with z-index: 0 (behind all content)
   - Smooth 500ms fade transitions
   - Responsive blur and opacity adjustments
   - Dark overlay (30%) for text readability

## How It Works

### User Flow

1. **Normal State**: User sees the ChatGPT-style UI with LightRays background
2. **User Sends Message**: Message appears in chat
3. **Bot Starts Streaming**: 
   - Random video is selected
   - Video fades in with blur and low opacity
   - Text streams character-by-character
4. **Response Completes**: Video fades out smoothly
5. **Return to Normal**: LightRays background remains

### Technical Flow

```javascript
// When bot starts responding
setIsStreaming(true)
setCurrentVideo(getRandomVideo())

// VideoBackground component receives props
<VideoBackground videoSrc={currentVideo} isActive={isStreaming} />

// When response completes
setIsStreaming(false)
setCurrentVideo(null)
```

## File Structure

```
p_hack/react_web/
├── public/
│   └── videos/
│       ├── README.md          # Video placement guide
│       ├── video1.mp4         # (User needs to add)
│       ├── video2.mp4         # (User needs to add)
│       └── video3.mp4         # (User needs to add)
├── src/
│   ├── components/
│   │   ├── VideoBackground.jsx      # Video component
│   │   └── VideoBackground.css      # Video styling
│   ├── utils/
│   │   └── videoHelper.js           # Video management
│   └── pages/
│       └── MentalHealthChatPage.jsx # Main integration
```

## Next Steps for User

### 1. Add Video Files

Place 3 video files in `public/videos/`:
- `video1.mp4`
- `video2.mp4`
- `video3.mp4`

**Video Requirements**:
- Format: MP4 (H.264 codec)
- Resolution: 1920x1080 or higher
- Duration: 10-30 seconds (will loop)
- File Size: Under 5MB recommended
- Content: Abstract, calming visuals (particles, waves, gradients)

### 2. Test the Implementation

```bash
# Start the development server
npm run dev

# Open browser and navigate to chat page
# Send a message and observe:
# - Video should fade in when bot starts responding
# - Video should be blurred and subtle
# - Text should remain clear and readable
# - Video should fade out when response completes
```

### 3. Adjust Settings (Optional)

If you want to modify the video effects, edit `VideoBackground.css`:

```css
.video-background {
  filter: blur(12px);    /* Increase/decrease blur */
  opacity: 0.4;          /* Increase/decrease visibility */
}
```

Or adjust the overlay darkness:

```css
.video-background-container::after {
  background: rgba(0, 0, 0, 0.3);  /* Adjust darkness (0-1) */
}
```

## Features

### ✅ Implemented Features

- [x] Random video selection on each bot response
- [x] Smooth fade-in/out transitions (500ms)
- [x] Strong blur effect (12px) for readability
- [x] Low opacity (40%) to avoid distraction
- [x] Dark overlay (30%) for text contrast
- [x] Automatic play/pause based on streaming state
- [x] Error handling (graceful fallback if videos missing)
- [x] Responsive design (reduced blur on mobile)
- [x] Performance optimized (pointer-events: none)
- [x] Proper z-index layering (video behind all content)

### 🎨 Visual Layers (Bottom to Top)

1. **Layer 0**: VideoBackground (z-index: 0) - Only during streaming
2. **Layer 1**: LightRays (z-index: 1) - Always visible
3. **Layer 2**: Dark Overlay (z-index: 2) - For readability
4. **Layer 3**: Chat UI (z-index: 3) - Main content

## Troubleshooting

### Videos Not Playing

1. **Check file paths**: Videos must be in `public/videos/`
2. **Check file names**: Must be exactly `video1.mp4`, `video2.mp4`, `video3.mp4`
3. **Check browser console**: Look for video loading errors
4. **Check video format**: Must be MP4 with H.264 codec

### Videos Too Distracting

1. **Increase blur**: Change `filter: blur(12px)` to `blur(16px)` or higher
2. **Reduce opacity**: Change `opacity: 0.4` to `0.3` or lower
3. **Darken overlay**: Change `rgba(0, 0, 0, 0.3)` to `rgba(0, 0, 0, 0.5)`

### Performance Issues

1. **Compress videos**: Use FFmpeg or HandBrake to reduce file size
2. **Lower resolution**: Use 1280x720 instead of 1920x1080
3. **Reduce video count**: Use only 1-2 videos instead of 3
4. **Disable on mobile**: Add media query to hide on small screens

## Example Video Sources

### Free Stock Video Sites:
- **Pexels Videos**: https://www.pexels.com/videos/
- **Pixabay Videos**: https://pixabay.com/videos/
- **Videvo**: https://www.videvo.net/
- **Coverr**: https://coverr.co/

### Recommended Search Terms:
- "abstract particles"
- "flowing waves"
- "gradient motion"
- "calm nature"
- "soft bokeh"
- "peaceful water"
- "gentle movement"

## Code References

### Key State Variables

```javascript
const [isStreaming, setIsStreaming] = useState(false)
const [currentVideo, setCurrentVideo] = useState(null)
```

### Trigger Points

```javascript
// Start video
setIsStreaming(true)
setCurrentVideo(getRandomVideo())

// Stop video
setIsStreaming(false)
setCurrentVideo(null)
```

### Component Usage

```jsx
<VideoBackground 
  videoSrc={currentVideo}  // Path to video or null
  isActive={isStreaming}   // Boolean: show/hide video
/>
```

## Performance Considerations

- Videos are loaded on-demand (not preloaded)
- Only one video plays at a time
- Videos use `pointer-events: none` to not block interactions
- Smooth transitions prevent jarring visual changes
- Graceful fallback if videos are missing
- Responsive adjustments for mobile devices

## Future Enhancements (Optional)

- [ ] Preload videos for instant playback
- [ ] Add video categories (calm, energetic, nature)
- [ ] User preference for video intensity
- [ ] Video selection based on conversation mood
- [ ] Crossfade between videos for longer responses
- [ ] Custom video upload feature
- [ ] Video playback speed control

## Summary

The video background feature is **fully implemented** and ready to use. The only remaining step is for the user to add the actual video files to the `public/videos/` folder. The implementation is production-ready with proper error handling, performance optimization, and responsive design.

**Status**: ✅ Complete - Ready for testing with video files
