import { useState, useRef, useEffect } from 'react'
import PropTypes from 'prop-types'
import { Plus, Mic } from 'lucide-react'
import UploadMenu from './UploadMenu'
import AudioRecorder from './AudioRecorder'
import Toast from '../Toast'
import { getFileInfo } from '../../utils/fileTypeDetector'

export default function ChatInput({ onSend, disabled, hasMessages }) {
  const [input, setInput] = useState('')
  const [isUploadMenuOpen, setIsUploadMenuOpen] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [toastFileInfo, setToastFileInfo] = useState(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current && !isRecording) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [input, isRecording])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input)
      setInput('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleFileSelect = (file) => {
    console.log('File selected:', file)
    
    // Get file information with type detection
    const fileInfo = getFileInfo(file)
    
    // Show toast notification
    setToastFileInfo(fileInfo)
    
    // TODO: Handle file upload to backend
    // For now, just show a message with detected type
    const fileMessage = `📎 [${fileInfo.type}: ${fileInfo.name} - ${fileInfo.size}]`
    onSend(fileMessage)
  }

  const handleSendAudio = (audioBlob, duration) => {
    console.log('Audio recorded:', audioBlob, 'Duration:', duration)
    // TODO: Handle audio upload to backend
    // For now, just show a message
    const audioMessage = `🎤 [Audio message: ${duration}s]`
    onSend(audioMessage)
    setIsRecording(false)
  }

  const handleCancelRecording = () => {
    setIsRecording(false)
  }

  const handleStartRecording = () => {
    setIsRecording(true)
    setIsUploadMenuOpen(false)
  }

  const handleCloseToast = () => {
    setToastFileInfo(null)
  }

  return (
    <>
      {/* Toast Notification */}
      {toastFileInfo && <Toast fileInfo={toastFileInfo} onClose={handleCloseToast} />}

      <div className={`chat-input-wrapper ${hasMessages ? 'with-messages' : 'centered'}`}>
        <form onSubmit={handleSubmit} className="chat-input-form">
          {isRecording ? (
            <AudioRecorder onSendAudio={handleSendAudio} onCancel={handleCancelRecording} />
          ) : (
            <div className="input-container">
              {/* Plus button for upload menu */}
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setIsUploadMenuOpen(!isUploadMenuOpen)}
                  className="input-icon-button"
                  aria-label="Attach file"
                  disabled={disabled}
                >
                  <Plus size={20} />
                </button>
                <UploadMenu
                  isOpen={isUploadMenuOpen}
                  onClose={() => setIsUploadMenuOpen(false)}
                  onFileSelect={handleFileSelect}
                />
              </div>

              {/* Text input */}
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Share what's on your mind..."
                disabled={disabled}
                rows={1}
                className="chat-textarea"
              />

              {/* Mic button */}
              <button
                type="button"
                onClick={handleStartRecording}
                className="input-icon-button"
                aria-label="Voice input"
                disabled={disabled}
              >
                <Mic size={20} />
              </button>

              {/* Send button */}
              <button
                type="submit"
                disabled={!input.trim() || disabled}
                className="send-button"
                aria-label="Send message"
              >
                <svg
                  width="20"
                  height="20"
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
          )}
        </form>
        {!hasMessages && !isRecording && (
          <p className="input-hint">Press Enter to send, Shift+Enter for new line</p>
        )}
      </div>
    </>
  )
}

ChatInput.propTypes = {
  onSend: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  hasMessages: PropTypes.bool.isRequired,
}

ChatInput.defaultProps = {
  disabled: false,
}
