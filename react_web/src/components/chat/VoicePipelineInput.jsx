import { useState, useRef, useEffect } from 'react'
import PropTypes from 'prop-types'
import { Mic, Square, X, Loader } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function VoicePipelineInput({ onVoiceResult, onClose, sessionId }) {
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [recordingTime, setRecordingTime] = useState(0)
  const [audioLevel, setAudioLevel] = useState(0)
  
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const timerRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const animationFrameRef = useRef(null)

  useEffect(() => {
    startRecording()
    return () => {
      stopRecording()
      if (timerRef.current) clearInterval(timerRef.current)
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current)
      if (audioContextRef.current) audioContextRef.current.close()
    }
  }, [])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      // Setup audio level visualization
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      analyserRef.current = audioContextRef.current.createAnalyser()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      source.connect(analyserRef.current)
      analyserRef.current.fftSize = 256
      
      const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount)
      
      const updateAudioLevel = () => {
        analyserRef.current.getByteFrequencyData(dataArray)
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length
        setAudioLevel(average / 255) // Normalize to 0-1
        animationFrameRef.current = requestAnimationFrame(updateAudioLevel)
      }
      updateAudioLevel()
      
      // Setup media recorder
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }
      
      mediaRecorderRef.current.onstop = async () => {
        // Clear timer immediately when recording stops
        if (timerRef.current) {
          clearInterval(timerRef.current)
          timerRef.current = null
        }
        
        // Stop audio visualization
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current)
          animationFrameRef.current = null
        }
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
        
        // Close audio context
        if (audioContextRef.current) {
          audioContextRef.current.close()
        }
        
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        await sendToVoicePipeline(audioBlob)
      }
      
      mediaRecorderRef.current.start()
      setIsRecording(true)
      setError(null)
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
      
    } catch (err) {
      console.error('Error starting recording:', err)
      setError('Could not access microphone. Please ensure microphone permissions are granted.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      // Clear timer
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
      
      // Stop audio level animation
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
        animationFrameRef.current = null
      }
    }
  }

  const sendToVoicePipeline = async (audioBlob) => {
    setIsProcessing(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('session_id', sessionId)
      formData.append('audio', audioBlob, 'recording.webm')
      
      const response = await fetch(`${API_BASE_URL}/api/voice/chat`, {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Pass the full voice result to parent
      onVoiceResult(data)
      onClose()
      
    } catch (err) {
      console.error('Error sending voice message:', err)
      setError(`Error processing voice: ${err.message}. Please try again.`)
      setIsProcessing(false)
    }
  }

  const handleStop = () => {
    // Clear timer immediately
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
    
    // Stop recording
    stopRecording()
  }

  const handleCancel = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      if (timerRef.current) clearInterval(timerRef.current)
    }
    onClose()
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="voice-pipeline-container">
      <div className="voice-pipeline-header">
        <div className="voice-pipeline-status">
          {isProcessing ? (
            <>
              <Loader className="voice-spinner" size={20} />
              <span className="voice-status-text">Processing audio...</span>
            </>
          ) : isRecording ? (
            <>
              <span className="voice-pulse"></span>
              <span className="voice-status-text">Recording...</span>
            </>
          ) : (
            <span className="voice-status-text">Ready</span>
          )}
        </div>
        <button
          onClick={handleCancel}
          className="voice-close-button"
          aria-label="Cancel"
          disabled={isProcessing}
        >
          <X size={20} />
        </button>
      </div>

      {error && (
        <div className="voice-error">
          <span className="voice-error-icon">⚠️</span>
          <span className="voice-error-text">{error}</span>
        </div>
      )}

      <div className="voice-visualizer">
        {/* Audio level visualization */}
        <div className="voice-waveform">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="voice-bar"
              style={{
                height: `${Math.max(10, audioLevel * 100 * (0.5 + Math.random() * 0.5))}%`,
                animationDelay: `${i * 0.05}s`
              }}
            />
          ))}
        </div>
        
        {/* Recording time */}
        <div className="voice-timer">{formatTime(recordingTime)}</div>
      </div>

      <div className="voice-controls">
        {isRecording ? (
          <button
            onClick={handleStop}
            className="voice-stop-button"
            aria-label="Stop recording"
          >
            <Square size={24} fill="currentColor" />
            <span>Stop</span>
          </button>
        ) : isProcessing ? (
          <div className="voice-processing-text">
            Analyzing your voice...
          </div>
        ) : null}
      </div>

      <p className="voice-hint">
        {isRecording 
          ? 'Speak clearly into your microphone. Click stop when done.' 
          : isProcessing
          ? 'This may take a few seconds...'
          : 'Starting...'}
      </p>
    </div>
  )
}

VoicePipelineInput.propTypes = {
  onVoiceResult: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
  sessionId: PropTypes.string.isRequired,
}
