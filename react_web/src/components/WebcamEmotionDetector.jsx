import React from 'react';
import { useFacialEmotion, getEmotionEmoji } from '../hooks/useFacialEmotion';
import './WebcamEmotionDetector.css';

/**
 * Webcam emotion detector component
 * Shows live webcam feed with emotion detection overlay
 */
const WebcamEmotionDetector = ({ enabled, onEmotionDetected, compact = false }) => {
  const {
    videoRef,
    canvasRef,
    isLoading,
    isReady,
    error,
    currentEmotion,
    loadingProgress,
    stopWebcam
  } = useFacialEmotion(enabled);

  // Debug logging
  React.useEffect(() => {
    console.log('🎭 [WEBCAM-COMPONENT] State changed:', {
      enabled,
      isLoading,
      isReady,
      hasError: !!error,
      hasEmotion: !!currentEmotion,
      emotion: currentEmotion?.dominant_emotion,
      videoRef: !!videoRef.current,
      canvasRef: !!canvasRef.current
    });
  }, [enabled, isLoading, isReady, error, currentEmotion]);

  // Notify parent component when emotion changes
  React.useEffect(() => {
    if (currentEmotion && onEmotionDetected) {
      console.log('📤 [WEBCAM-COMPONENT] Sending emotion to parent:', currentEmotion);
      onEmotionDetected(currentEmotion);
    }
  }, [currentEmotion, onEmotionDetected]);

  if (!enabled) {
    return null;
  }

  if (error) {
    return (
      <div className={`webcam-detector ${compact ? 'compact' : ''}`}>
        <div className="webcam-error">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="retry-btn">
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className={`webcam-detector ${compact ? 'compact' : ''}`}>
        <div className="webcam-loading">
          <div className="loading-spinner"></div>
          <p>Loading emotion detection models...</p>
          <div className="loading-progress">
            <div 
              className="progress-bar"
              style={{ width: `${(loadingProgress.current / loadingProgress.total) * 100}%` }}
            ></div>
          </div>
          <span className="progress-text">
            {loadingProgress.current}/{loadingProgress.total} models loaded
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className={`webcam-detector ${compact ? 'compact' : ''}`}>
      <div className="webcam-container">
        {/* Direct video element - minimal props to avoid conflicts */}
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="webcam-video"
        />
        
        <canvas
          ref={canvasRef}
          className="webcam-canvas"
        />
        
        {currentEmotion && (
          <div className="emotion-overlay">
            <div className="emotion-badge">
              <span className="emotion-emoji">
                {getEmotionEmoji(currentEmotion.dominant_emotion)}
              </span>
              <span className="emotion-text">
                {currentEmotion.dominant_emotion}
              </span>
              <span className="emotion-confidence">
                {(currentEmotion.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        )}

        <button 
          className="webcam-close-btn"
          onClick={stopWebcam}
          title="Disable webcam"
        >
          ✕
        </button>
      </div>

      {!compact && currentEmotion && (
        <div className="emotion-details">
          <div className="detail-item">
            <span className="detail-label">Age:</span>
            <span className="detail-value">{currentEmotion.age || 'N/A'}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Gender:</span>
            <span className="detail-value">{currentEmotion.gender || 'N/A'}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default WebcamEmotionDetector;
