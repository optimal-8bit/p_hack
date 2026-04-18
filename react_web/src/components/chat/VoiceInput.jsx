import { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { Mic, MicOff, X } from 'lucide-react'

export default function VoiceInput({ onTranscript, onClose, language = 'en-US' }) {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [interimTranscript, setInterimTranscript] = useState('')
  const [error, setError] = useState(null)
  const recognitionRef = useRef(null)

  useEffect(() => {
    // Check if browser supports Web Speech API
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.')
      return
    }

    // Initialize Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = language
    recognition.maxAlternatives = 1

    recognition.onstart = () => {
      setIsListening(true)
      setError(null)
    }

    recognition.onresult = (event) => {
      let interimText = ''
      let finalText = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptPart = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalText += transcriptPart + ' '
        } else {
          interimText += transcriptPart
        }
      }

      if (finalText) {
        setTranscript((prev) => prev + finalText)
        setInterimTranscript('')
      } else {
        setInterimTranscript(interimText)
      }
    }

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error)
      
      switch (event.error) {
        case 'no-speech':
          setError('No speech detected. Please try again.')
          break
        case 'audio-capture':
          setError('No microphone found. Please check your microphone.')
          break
        case 'not-allowed':
          setError('Microphone permission denied. Please allow microphone access.')
          break
        case 'network':
          setError('Network error. Please check your internet connection.')
          break
        default:
          setError(`Error: ${event.error}`)
      }
      
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition

    // Start recognition automatically
    try {
      recognition.start()
    } catch (err) {
      console.error('Failed to start recognition:', err)
      setError('Failed to start voice input. Please try again.')
    }

    // Cleanup
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [language])

  const toggleListening = () => {
    if (!recognitionRef.current) return

    if (isListening) {
      recognitionRef.current.stop()
    } else {
      setError(null)
      try {
        recognitionRef.current.start()
      } catch (err) {
        console.error('Failed to restart recognition:', err)
        setError('Failed to start voice input. Please try again.')
      }
    }
  }

  const handleSend = () => {
    const finalTranscript = (transcript + interimTranscript).trim()
    if (finalTranscript) {
      onTranscript(finalTranscript)
    }
    handleClose()
  }

  const handleClose = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }
    onClose()
  }

  const displayText = transcript + interimTranscript

  return (
    <div className="voice-input-container">
      <div className="voice-input-header">
        <div className="voice-input-status">
          {isListening ? (
            <>
              <span className="voice-pulse"></span>
              <span className="voice-status-text">Listening...</span>
            </>
          ) : (
            <span className="voice-status-text">Paused</span>
          )}
        </div>
        <button
          onClick={handleClose}
          className="voice-close-button"
          aria-label="Close voice input"
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

      <div className="voice-transcript-area">
        {displayText ? (
          <p className="voice-transcript-text">
            {transcript}
            {interimTranscript && (
              <span className="voice-interim-text">{interimTranscript}</span>
            )}
          </p>
        ) : (
          <p className="voice-placeholder">Start speaking...</p>
        )}
      </div>

      <div className="voice-controls">
        <button
          onClick={toggleListening}
          className={`voice-toggle-button ${isListening ? 'listening' : 'paused'}`}
          aria-label={isListening ? 'Pause listening' : 'Start listening'}
          disabled={!!error}
        >
          {isListening ? <Mic size={24} /> : <MicOff size={24} />}
        </button>

        <button
          onClick={handleSend}
          disabled={!displayText.trim()}
          className="voice-send-button"
          aria-label="Send transcript"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M2.5 10L17.5 10M17.5 10L11.25 3.75M17.5 10L11.25 16.25"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>

      <p className="voice-hint">
        {isListening 
          ? 'Speak clearly into your microphone' 
          : 'Click the microphone to resume'}
      </p>
    </div>
  )
}

VoiceInput.propTypes = {
  onTranscript: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
  language: PropTypes.string,
}
