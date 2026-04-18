import React, { useRef, useEffect, useImperativeHandle, forwardRef } from 'react';

/**
 * Stable video element that doesn't get recreated by React
 * This prevents the AbortError when React re-renders
 */
const StableVideoElement = forwardRef(({ onMetadataLoaded, onPlay, onError }, ref) => {
  const videoRef = useRef(null);
  const containerRef = useRef(null);

  // Expose video ref to parent
  useImperativeHandle(ref, () => videoRef.current);

  useEffect(() => {
    // Create video element only once
    if (!videoRef.current && containerRef.current) {
      console.log('🎬 [STABLE-VIDEO] Creating video element...');
      
      const video = document.createElement('video');
      video.autoplay = true;
      video.muted = true;
      video.playsInline = true;
      video.style.width = '100%';
      video.style.height = '100%';
      video.style.objectFit = 'cover';
      video.style.transform = 'scaleX(-1)';
      video.style.display = 'block';
      video.style.borderRadius = '8px';

      // Add event listeners
      video.onloadedmetadata = () => {
        console.log('📺 [STABLE-VIDEO] Metadata loaded:', {
          videoSize: `${video.videoWidth}x${video.videoHeight}`,
          displaySize: `${video.offsetWidth}x${video.offsetHeight}`
        });
        onMetadataLoaded?.(video);
      };

      video.onplay = () => {
        console.log('▶️ [STABLE-VIDEO] Video playing');
        onPlay?.(video);
      };

      video.onerror = (e) => {
        console.error('❌ [STABLE-VIDEO] Video error:', e);
        onError?.(e);
      };

      containerRef.current.appendChild(video);
      videoRef.current = video;
      
      console.log('✅ [STABLE-VIDEO] Video element created and attached');
    }

    // Cleanup function
    return () => {
      if (videoRef.current && containerRef.current) {
        console.log('🧹 [STABLE-VIDEO] Cleaning up video element');
        try {
          if (videoRef.current.srcObject) {
            const stream = videoRef.current.srcObject;
            stream.getTracks().forEach(track => track.stop());
          }
          videoRef.current.srcObject = null;
          containerRef.current.removeChild(videoRef.current);
        } catch (e) {
          console.warn('⚠️ [STABLE-VIDEO] Cleanup warning:', e);
        }
        videoRef.current = null;
      }
    };
  }, [onMetadataLoaded, onPlay, onError]);

  return (
    <div 
      ref={containerRef}
      style={{
        width: '100%',
        height: '100%',
        background: '#000',
        borderRadius: '8px',
        overflow: 'hidden'
      }}
    />
  );
});

StableVideoElement.displayName = 'StableVideoElement';

export default StableVideoElement;