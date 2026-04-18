import React, { useRef, useState } from 'react';

const SimpleVideoTest = () => {
  const videoRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [status, setStatus] = useState('Ready to test');

  const startVideo = async () => {
    try {
      setStatus('Requesting camera...');
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' }
      });
      
      setStatus('Camera granted, setting up video...');
      setStream(mediaStream);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        
        videoRef.current.onloadedmetadata = () => {
          setStatus(`Video loaded: ${videoRef.current.videoWidth}x${videoRef.current.videoHeight}`);
        };
        
        videoRef.current.onplay = () => {
          setStatus('Video playing successfully!');
        };
        
        await videoRef.current.play();
      }
    } catch (error) {
      setStatus(`Error: ${error.message}`);
      console.error('Video test error:', error);
    }
  };

  const stopVideo = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }
      setStatus('Video stopped');
    }
  };

  return (
    <div style={{ 
      position: 'fixed', 
      top: '20px', 
      right: '20px', 
      width: '300px', 
      background: 'white', 
      border: '2px solid #333', 
      borderRadius: '10px', 
      padding: '15px',
      zIndex: 1000,
      boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
    }}>
      <h3>🎥 Video Test</h3>
      <div style={{ 
        width: '100%', 
        height: '200px', 
        background: '#000', 
        borderRadius: '5px', 
        overflow: 'hidden',
        marginBottom: '10px'
      }}>
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: 'scaleX(-1)'
          }}
        />
      </div>
      <div style={{ fontSize: '12px', marginBottom: '10px' }}>
        Status: {status}
      </div>
      <button 
        onClick={startVideo} 
        style={{ 
          marginRight: '10px', 
          padding: '5px 10px',
          background: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '3px',
          cursor: 'pointer'
        }}
      >
        Start
      </button>
      <button 
        onClick={stopVideo}
        style={{ 
          padding: '5px 10px',
          background: '#f44336',
          color: 'white',
          border: 'none',
          borderRadius: '3px',
          cursor: 'pointer'
        }}
      >
        Stop
      </button>
    </div>
  );
};

export default SimpleVideoTest;