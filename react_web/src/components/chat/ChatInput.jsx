import { useState, useRef, useEffect } from 'react'
import PropTypes from 'prop-types'
import { Plus, Mic, X, FileText, Film, Music, FileSpreadsheet, Presentation, Archive, File } from 'lucide-react'
import UploadMenu from './UploadMenu'
import AudioRecorder from './AudioRecorder'
import VoiceInput from './VoiceInput'
import Toast from '../Toast'
import { getFileInfo } from '../../utils/fileTypeDetector'
import './VoiceInput.css'

// Get appropriate icon for file type
const getFileIcon = (fileType) => {
  if (fileType.includes('Image') || fileType.includes('SVG')) return null // Show image preview
  if (fileType.includes('Video')) return Film
  if (fileType.includes('Audio')) return Music
  if (fileType.includes('Spreadsheet') || fileType.includes('CSV')) return FileSpreadsheet
  if (fileType.includes('Presentation')) return Presentation
  if (fileType.includes('Archive')) return Archive
  if (fileType.includes('PDF') || fileType.includes('Word') || fileType.includes('Text') || fileType.includes('JSON') || fileType.includes('XML')) return FileText
  return File
}

export default function ChatInput({ onSend, disabled, hasMessages }) {
  const [input, setInput] = useState('')
  const [isUploadMenuOpen, setIsUploadMenuOpen] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [isVoiceInput, setIsVoiceInput] = useState(false)
  const [toastFileInfo, setToastFileInfo] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [filePreviewUrl, setFilePreviewUrl] = useState(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current && !isRecording && !isVoiceInput) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [input, isRecording, isVoiceInput])

  // Create preview URL for images
  useEffect(() => {
    if (selectedFile) {
      const fileInfo = getFileInfo(selectedFile)
      
      // Create preview URL for images
      if (fileInfo.type === 'Image' || fileInfo.type === 'SVG Vector') {
        const url = URL.createObjectURL(selectedFile)
        setFilePreviewUrl(url)
        
        // Cleanup
        return () => URL.revokeObjectURL(url)
      } else {
        setFilePreviewUrl(null)
      }
    } else {
      setFilePreviewUrl(null)
    }
  }, [selectedFile])

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Check if there's a file or text to send
    if ((input.trim() || selectedFile) && !disabled) {
      let message = input.trim()
      
      // If there's a selected file, add it to the message
      if (selectedFile) {
        const fileInfo = getFileInfo(selectedFile)
        const fileTag = `📎 [${fileInfo.type}: ${fileInfo.name} - ${fileInfo.size}]`
        
        // Combine file tag with text message
        if (message) {
          message = `${fileTag}\n${message}`
        } else {
          message = fileTag
        }
        
        // TODO: Handle actual file upload to backend here
        console.log('Sending file:', selectedFile, 'with message:', input)
      }
      
      onSend(message)
      setInput('')
      setSelectedFile(null)
      setFilePreviewUrl(null)
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
    
    // Store the selected file (don't send yet)
    setSelectedFile(file)
    
    // Focus on textarea so user can type
    setTimeout(() => {
      textareaRef.current?.focus()
    }, 100)
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    setFilePreviewUrl(null)
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

  const handleStartVoiceInput = () => {
    setIsVoiceInput(true)
    setIsUploadMenuOpen(false)
  }

  const handleVoiceTranscript = (transcript) => {
    setInput(transcript)
    setIsVoiceInput(false)
    // Focus on textarea after voice input
    setTimeout(() => {
      textareaRef.current?.focus()
    }, 100)
  }

  const handleCloseVoiceInput = () => {
    setIsVoiceInput(false)
  }

  const handleCloseToast = () => {
    setToastFileInfo(null)
  }

  // Get file info for display
  const fileInfo = selectedFile ? getFileInfo(selectedFile) : null
  const FileIcon = fileInfo ? getFileIcon(fileInfo.type) : null

  return (
    <>
      {/* Toast Notification */}
      {toastFileInfo && <Toast fileInfo={toastFileInfo} onClose={handleCloseToast} />}

      <div className={`chat-input-wrapper ${hasMessages ? 'with-messages' : 'centered'}`}>
        <form onSubmit={handleSubmit} className="chat-input-form">
          {isVoiceInput ? (
            <VoiceInput onTranscript={handleVoiceTranscript} onClose={handleCloseVoiceInput} />
          ) : isRecording ? (
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

              {/* Input area with file thumbnail */}
              <div className="input-content-wrapper">
                {/* File thumbnail preview */}
                {selectedFile && fileInfo && (
                  <div className="file-thumbnail-container">
                    <div className="file-thumbnail">
                      {/* Image preview or file icon */}
                      {filePreviewUrl ? (
                        <img 
                          src={filePreviewUrl} 
                          alt={fileInfo.name}
                          className="file-thumbnail-image"
                        />
                      ) : FileIcon ? (
                        <div className="file-thumbnail-icon">
                          <FileIcon size={32} />
                        </div>
                      ) : (
                        <div className="file-thumbnail-icon">
                          <File size={32} />
                        </div>
                      )}
                      
                      {/* Remove button overlay */}
                      <button
                        type="button"
                        onClick={handleRemoveFile}
                        className="file-thumbnail-remove"
                        aria-label="Remove file"
                      >
                        <X size={16} />
                      </button>
                    </div>
                    
                    {/* File info below thumbnail */}
                    <div className="file-thumbnail-info">
                      <div className="file-thumbnail-name">{fileInfo.name}</div>
                      <div className="file-thumbnail-size">{fileInfo.size}</div>
                    </div>
                  </div>
                )}

                {/* Text input */}
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={selectedFile ? "Add a message (optional)..." : "Share what's on your mind..."}
                  disabled={disabled}
                  rows={1}
                  className="chat-textarea"
                />
              </div>

              {/* Mic button - Long press for recording, click for voice input */}
              <button
                type="button"
                onClick={handleStartVoiceInput}
                onContextMenu={(e) => {
                  e.preventDefault()
                  handleStartRecording()
                }}
                className="input-icon-button"
                aria-label="Voice input (right-click for audio recording)"
                disabled={disabled}
                title="Click for voice-to-text, right-click for audio recording"
              >
                <Mic size={20} />
              </button>

              {/* Send button */}
              <button
                type="submit"
                disabled={(!input.trim() && !selectedFile) || disabled}
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
        {/* {!hasMessages && !isRecording && !isVoiceInput && (
          <p className="input-hint">Press Enter to send, Shift+Enter for new line</p>
        )} */}
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
