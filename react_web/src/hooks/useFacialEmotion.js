import { useState, useEffect, useRef, useCallback } from 'react';

const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.12/model';

/**
 * Custom hook for real-time facial emotion detection using face-api.js
 * Runs entirely in the browser for privacy
 */
export const useFacialEmotion = (enabled = true) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState(null);
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const [stream, setStream] = useState(null);
  const [loadingProgress, setLoadingProgress] = useState({ current: 0, total: 4 });
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const detectionIntervalRef = useRef(null);
  const modelsLoadedRef = useRef(false);

  // Load face-api.js models
  const loadModels = useCallback(async () => {
    if (modelsLoadedRef.current || !window.faceapi) {
      console.log('🔄 [FACIAL-EMOTION] Models already loaded or face-api not available');
      return;
    }

    try {
      console.log('🚀 [FACIAL-EMOTION] Starting model loading...');
      setIsLoading(true);
      setLoadingProgress({ current: 0, total: 4 });

      // Load models one by one with progress updates
      console.log('📥 [FACIAL-EMOTION] Loading SSD MobileNet v1 (1/4)...');
      await window.faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL);
      setLoadingProgress({ current: 1, total: 4 });
      console.log('✅ [FACIAL-EMOTION] SSD MobileNet v1 loaded');

      console.log('📥 [FACIAL-EMOTION] Loading Face Landmark 68 (2/4)...');
      await window.faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
      setLoadingProgress({ current: 2, total: 4 });
      console.log('✅ [FACIAL-EMOTION] Face Landmark 68 loaded');

      console.log('📥 [FACIAL-EMOTION] Loading Face Expression Net (3/4)...');
      await window.faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL);
      setLoadingProgress({ current: 3, total: 4 });
      console.log('✅ [FACIAL-EMOTION] Face Expression Net loaded');

      console.log('📥 [FACIAL-EMOTION] Loading Age Gender Net (4/4)...');
      await window.faceapi.nets.ageGenderNet.loadFromUri(MODEL_URL);
      setLoadingProgress({ current: 4, total: 4 });
      console.log('✅ [FACIAL-EMOTION] Age Gender Net loaded');

      modelsLoadedRef.current = true;
      setIsLoading(false);
      setIsReady(true);
      console.log('🎉 [FACIAL-EMOTION] All models loaded successfully! Ready for detection.');
    } catch (err) {
      console.error('❌ [FACIAL-EMOTION] Failed to load models:', err);
      setError('Failed to load emotion detection models');
      setIsLoading(false);
    }
  }, []);

  // Start webcam
  const startWebcam = useCallback(async () => {
    if (!enabled || !isReady || stream) {
      console.log('🔄 [FACIAL-EMOTION] Webcam start skipped:', { enabled, isReady, hasStream: !!stream });
      return;
    }

    try {
      console.log('📹 [FACIAL-EMOTION] Requesting webcam access...');
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        }
      });

      console.log('✅ [FACIAL-EMOTION] Webcam access granted');
      console.log('📊 [FACIAL-EMOTION] Video stream info:', {
        tracks: mediaStream.getTracks().length,
        videoTracks: mediaStream.getVideoTracks().length,
        active: mediaStream.active
      });

      setStream(mediaStream);
      console.log('🎥 [FACIAL-EMOTION] Webcam started successfully');
    } catch (err) {
      console.error('❌ [FACIAL-EMOTION] Failed to access webcam:', err);
      
      let errorMessage = 'Failed to access webcam. ';
      if (err.name === 'NotAllowedError') {
        errorMessage += 'Please grant camera permission.';
      } else if (err.name === 'NotFoundError') {
        errorMessage += 'No camera found.';
      } else if (err.name === 'NotReadableError') {
        errorMessage += 'Camera is already in use.';
      } else {
        errorMessage += 'Please check your camera settings.';
      }
      
      setError(errorMessage);
    }
  }, [enabled, isReady, stream]);

  // Stop webcam
  const stopWebcam = useCallback(() => {
    console.log('🛑 [FACIAL-EMOTION] Stopping webcam...');
    
    if (stream) {
      console.log('📹 [FACIAL-EMOTION] Stopping video tracks...');
      stream.getTracks().forEach(track => {
        console.log(`🔌 [FACIAL-EMOTION] Stopping track: ${track.kind} (${track.label})`);
        track.stop();
      });
      setStream(null);
    }

    if (detectionIntervalRef.current) {
      console.log('⏹️ [FACIAL-EMOTION] Clearing detection interval...');
      clearInterval(detectionIntervalRef.current);
      detectionIntervalRef.current = null;
    }

    if (videoRef.current) {
      console.log('📺 [FACIAL-EMOTION] Clearing video source...');
      videoRef.current.srcObject = null;
    }

    setCurrentEmotion(null);
    console.log('✅ [FACIAL-EMOTION] Webcam stopped successfully');
  }, [stream]);

  // Detect emotions from video frame
  const detectEmotion = useCallback(async () => {
    if (!videoRef.current || !canvasRef.current || !window.faceapi) {
      console.log('⚠️ [FACIAL-EMOTION] Detection skipped - missing refs or face-api');
      return;
    }

    if (videoRef.current.readyState !== 4) {
      console.log('⚠️ [FACIAL-EMOTION] Detection skipped - video not ready (readyState: ' + videoRef.current.readyState + ')');
      return;
    }

    try {
      const detections = await window.faceapi
        .detectAllFaces(
          videoRef.current,
          new window.faceapi.SsdMobilenetv1Options({ minConfidence: 0.3 })
        )
        .withFaceLandmarks()
        .withFaceExpressions()
        .withAgeAndGender();

      // Clear canvas
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (detections && detections.length > 0) {
        // Use first detected face
        const detection = detections[0];
        const expressions = detection.expressions;

        // Find dominant emotion
        let maxEmotion = 'neutral';
        let maxConfidence = 0;
        const allEmotions = {};

        Object.entries(expressions).forEach(([emotion, confidence]) => {
          allEmotions[emotion] = confidence;
          if (confidence > maxConfidence) {
            maxConfidence = confidence;
            maxEmotion = emotion;
          }
        });

        // Log detection results
        console.log('😊 [FACIAL-EMOTION] Face detected:', {
          emotion: maxEmotion,
          confidence: (maxConfidence * 100).toFixed(1) + '%',
          age: Math.round(detection.age),
          gender: detection.gender,
          allEmotions: Object.fromEntries(
            Object.entries(allEmotions).map(([k, v]) => [k, (v * 100).toFixed(1) + '%'])
          )
        });

        // Update current emotion state
        const emotionData = {
          dominant_emotion: maxEmotion,
          confidence: maxConfidence,
          all_emotions: allEmotions,
          age: Math.round(detection.age),
          gender: detection.gender,
          timestamp: Date.now()
        };

        setCurrentEmotion(emotionData);

        // Draw bounding box on canvas
        const box = detection.detection.box;
        ctx.strokeStyle = getEmotionColor(maxEmotion);
        ctx.lineWidth = 3;
        ctx.strokeRect(box.x, box.y, box.width, box.height);

        // Draw emotion label
        ctx.fillStyle = getEmotionColor(maxEmotion);
        ctx.font = '16px Arial';
        ctx.fillText(
          `${maxEmotion} (${(maxConfidence * 100).toFixed(0)}%)`,
          box.x,
          box.y - 10
        );
      } else {
        // No face detected
        if (currentEmotion) {
          console.log('👤 [FACIAL-EMOTION] No face detected (was previously detecting)');
        }
        setCurrentEmotion(null);
      }
    } catch (err) {
      console.error('❌ [FACIAL-EMOTION] Error detecting emotion:', err);
    }
  }, [currentEmotion]);

  // Start detection loop
  const startDetection = useCallback(() => {
    if (detectionIntervalRef.current) {
      console.log('🔄 [FACIAL-EMOTION] Detection already running');
      return;
    }

    console.log('🎯 [FACIAL-EMOTION] Starting emotion detection loop (500ms interval)...');
    detectionIntervalRef.current = setInterval(() => {
      detectEmotion();
    }, 500); // Detect every 500ms

    console.log('✅ [FACIAL-EMOTION] Emotion detection started');
  }, [detectEmotion]);

  // Stop detection loop
  const stopDetection = useCallback(() => {
    if (detectionIntervalRef.current) {
      console.log('⏹️ [FACIAL-EMOTION] Stopping emotion detection loop...');
      clearInterval(detectionIntervalRef.current);
      detectionIntervalRef.current = null;
      console.log('✅ [FACIAL-EMOTION] Emotion detection stopped');
    }
  }, []);

  // Initialize on mount
  useEffect(() => {
    console.log('🚀 [FACIAL-EMOTION] Hook initialized:', { enabled, hasFaceApi: !!window.faceapi });
    
    if (enabled && window.faceapi) {
      loadModels();
    } else if (enabled && !window.faceapi) {
      console.error('❌ [FACIAL-EMOTION] face-api.js not loaded! Check if script is included in index.html');
      setError('face-api.js library not loaded');
    }

    return () => {
      console.log('🧹 [FACIAL-EMOTION] Cleaning up hook...');
      stopWebcam();
      stopDetection();
    };
  }, [enabled, loadModels, stopWebcam, stopDetection]);

  // Start webcam when ready
  useEffect(() => {
    console.log('🔄 [FACIAL-EMOTION] Webcam effect:', { enabled, isReady, hasStream: !!stream });
    
    if (enabled && isReady && !stream) {
      startWebcam();
    }
  }, [enabled, isReady, stream, startWebcam]);

  // Start detection when stream is ready
  useEffect(() => {
    console.log('🔄 [FACIAL-EMOTION] Detection effect:', { 
      hasStream: !!stream, 
      videoReady: videoRef.current?.readyState === 4,
      hasInterval: !!detectionIntervalRef.current
    });
    
    if (stream && videoRef.current) {
      const video = videoRef.current;
      
      // Set up video element with the stream
      if (video.srcObject !== stream) {
        console.log('🎥 [FACIAL-EMOTION] Setting video srcObject...');
        video.srcObject = stream;
        
        // Set up event listeners
        const handleLoadedMetadata = () => {
          console.log('📺 [FACIAL-EMOTION] Video metadata loaded');
        };
        
        const handlePlay = () => {
          console.log('🎬 [FACIAL-EMOTION] Video playback started');
        };
        
        const handleCanPlay = () => {
          console.log('▶️ [FACIAL-EMOTION] Video can play, starting detection...');
          startDetection();
        };
        
        const handleError = (e) => {
          console.error('❌ [FACIAL-EMOTION] Video error:', e);
        };
        
        video.addEventListener('loadedmetadata', handleLoadedMetadata);
        video.addEventListener('play', handlePlay);
        video.addEventListener('canplay', handleCanPlay);
        video.addEventListener('error', handleError);
        
        // Try to play the video
        video.play().catch(playError => {
          // Only log non-AbortError issues
          if (playError.name !== 'AbortError') {
            console.error('❌ [FACIAL-EMOTION] Video play() failed:', playError);
          }
        });
        
        // Cleanup function
        return () => {
          video.removeEventListener('loadedmetadata', handleLoadedMetadata);
          video.removeEventListener('play', handlePlay);
          video.removeEventListener('canplay', handleCanPlay);
          video.removeEventListener('error', handleError);
          stopDetection();
        };
      } else if (video.readyState >= 4) {
        // Video is already set up and ready
        console.log('▶️ [FACIAL-EMOTION] Video already ready, starting detection...');
        startDetection();
      }
    }

    return () => {
      stopDetection();
    };
  }, [stream, startDetection, stopDetection]);

  // Resize canvas to match video
  useEffect(() => {
    const resizeCanvas = () => {
      if (videoRef.current && canvasRef.current) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        
        // Use the video's display size (offsetWidth/Height)
        const displayWidth = video.offsetWidth;
        const displayHeight = video.offsetHeight;
        
        canvas.width = displayWidth;
        canvas.height = displayHeight;
        
        console.log('📐 [FACIAL-EMOTION] Canvas resized:', {
          displaySize: `${displayWidth}x${displayHeight}`,
          videoSize: `${video.videoWidth}x${video.videoHeight}`,
          canvasSize: `${canvas.width}x${canvas.height}`
        });
      }
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Also resize when video metadata loads
    if (videoRef.current) {
      videoRef.current.addEventListener('loadedmetadata', resizeCanvas);
    }

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (videoRef.current) {
        videoRef.current.removeEventListener('loadedmetadata', resizeCanvas);
      }
    };
  }, [stream]);

  return {
    videoRef,
    canvasRef,
    isLoading,
    isReady,
    error,
    currentEmotion,
    loadingProgress,
    startWebcam,
    stopWebcam,
    startDetection,
    stopDetection
  };
};

// Helper function to get color for emotion
function getEmotionColor(emotion) {
  const colors = {
    happy: '#4ade80',
    sad: '#60a5fa',
    angry: '#f87171',
    fearful: '#a78bfa',
    disgusted: '#fb923c',
    surprised: '#fbbf24',
    neutral: '#94a3b8'
  };
  return colors[emotion] || '#94a3b8';
}

// Helper function to get emoji for emotion
export function getEmotionEmoji(emotion) {
  const emojis = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    fearful: '😨',
    disgusted: '🤢',
    surprised: '😲',
    neutral: '😐',
    joy: '😊',
    sadness: '😢',
    anger: '😠',
    fear: '😨',
    disgust: '🤢',
    surprise: '😲'
  };
  return emojis[emotion?.toLowerCase()] || '😐';
}
