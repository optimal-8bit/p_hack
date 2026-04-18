# Video Background Files

This folder contains the background videos that play during bot streaming responses.

## Required Files

Place the following video files in this directory:

1. `video1.mp4`
2. `video2.mp4`
3. `video3.mp4`

## Video Specifications

### Recommended Settings:
- **Format**: MP4 (H.264 codec)
- **Resolution**: 1920x1080 (Full HD) or higher
- **Duration**: 10-30 seconds (will loop)
- **File Size**: Keep under 5MB for optimal performance
- **Frame Rate**: 30fps or 60fps
- **Aspect Ratio**: 16:9

### Content Guidelines:
- Use abstract, calming visuals (particles, waves, gradients, nature)
- Avoid text or distracting elements
- Choose soothing colors (blues, purples, soft pastels)
- Ensure videos work well with blur effect (12px blur applied)
- Videos should complement the mental health theme

## How It Works

1. When the bot starts streaming a response, a random video is selected
2. The video plays with:
   - **Blur**: 12px (strong blur for readability)
   - **Opacity**: 40% (subtle background effect)
   - **Dark overlay**: 30% black overlay for text contrast
3. When the response completes, the video fades out smoothly
4. Videos loop continuously while streaming

## Testing

If videos are not available, the app will gracefully handle the missing files:
- No errors will be shown
- The LightRays background will remain visible
- Chat functionality continues normally

## Adding More Videos

To add more videos:

1. Add video files to this folder (e.g., `video4.mp4`, `video5.mp4`)
2. Update `/src/utils/videoHelper.js`:
   ```javascript
   const videos = [
     '/videos/video1.mp4',
     '/videos/video2.mp4',
     '/videos/video3.mp4',
     '/videos/video4.mp4', // Add new videos here
     '/videos/video5.mp4',
   ];
   ```

## Performance Tips

- Compress videos using tools like HandBrake or FFmpeg
- Use web-optimized encoding (fast start enabled)
- Test on slower connections to ensure smooth loading
- Consider using CDN for production deployment

## Example FFmpeg Command

To optimize a video for web use:

```bash
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k -movflags +faststart -vf scale=1920:1080 output.mp4
```

This command:
- Compresses the video with good quality (CRF 22)
- Scales to 1080p
- Enables fast start for web streaming
- Adds audio compression
