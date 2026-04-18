// Debug script for webcam issues
// Copy and paste this into browser console when webcam is enabled

console.log('🔍 [DEBUG] Starting webcam diagnosis...');

// Check if video element exists
const video = document.querySelector('.webcam-video');
console.log('📺 [DEBUG] Video element:', video);

if (video) {
  console.log('📊 [DEBUG] Video properties:', {
    srcObject: video.srcObject,
    readyState: video.readyState,
    videoWidth: video.videoWidth,
    videoHeight: video.videoHeight,
    offsetWidth: video.offsetWidth,
    offsetHeight: video.offsetHeight,
    paused: video.paused,
    muted: video.muted,
    autoplay: video.autoplay,
    playsInline: video.playsInline
  });

  console.log('🎨 [DEBUG] Video styles:', {
    display: getComputedStyle(video).display,
    visibility: getComputedStyle(video).visibility,
    opacity: getComputedStyle(video).opacity,
    width: getComputedStyle(video).width,
    height: getComputedStyle(video).height,
    transform: getComputedStyle(video).transform,
    objectFit: getComputedStyle(video).objectFit
  });

  if (video.srcObject) {
    const stream = video.srcObject;
    console.log('📡 [DEBUG] Stream info:', {
      active: stream.active,
      tracks: stream.getTracks().map(track => ({
        kind: track.kind,
        label: track.label,
        enabled: track.enabled,
        readyState: track.readyState,
        settings: track.getSettings()
      }))
    });

    // Try to play the video manually
    console.log('▶️ [DEBUG] Attempting manual play...');
    video.play().then(() => {
      console.log('✅ [DEBUG] Manual play successful');
    }).catch(err => {
      console.error('❌ [DEBUG] Manual play failed:', err);
    });
  } else {
    console.warn('⚠️ [DEBUG] No stream attached to video element');
  }
} else {
  console.error('❌ [DEBUG] Video element not found');
}

// Check canvas
const canvas = document.querySelector('.webcam-canvas');
console.log('🎨 [DEBUG] Canvas element:', canvas);

if (canvas) {
  console.log('📊 [DEBUG] Canvas properties:', {
    width: canvas.width,
    height: canvas.height,
    offsetWidth: canvas.offsetWidth,
    offsetHeight: canvas.offsetHeight
  });
}

// Check container
const container = document.querySelector('.webcam-container');
console.log('📦 [DEBUG] Container element:', container);

if (container) {
  console.log('📊 [DEBUG] Container properties:', {
    offsetWidth: container.offsetWidth,
    offsetHeight: container.offsetHeight,
    children: container.children.length
  });
}

// Check face-api
console.log('🤖 [DEBUG] Face-api status:', {
  loaded: !!window.faceapi,
  nets: window.faceapi ? Object.keys(window.faceapi.nets) : 'N/A'
});

console.log('🔍 [DEBUG] Diagnosis complete. Check the logs above for issues.');