import { useState, useRef, useEffect } from 'react'
import PropTypes from 'prop-types'
import { Plus, Mic, X, FileText, Film, Music, FileSpreadsheet, Presentation, Archive, File, Waves } from 'lucide-react'
import UploadMenu from './UploadMenu'
import AudioRecorder from './AudioRecorder'
import VoiceInput from './VoiceInput'
import VoicePipelineInput from './VoicePipelineInput'
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

export default function ChatInput({ onSend, disabled, hasMessages, sessionId, onVoiceResult }) {
  const [input, setInput] = useState('')
  const [isUploadMenuOpen, setIsUploadMenuOpen] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [isVoiceInput, setIsVoiceInput] = useState(false)
  const [isVoicePipeline, setIsVoicePipeline] = useState(false)
  const [toastFileInfo, setToastFileInfo] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [filePreviewUrl, setFilePreviewUrl] = useState(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current && !isRecording && !isVoiceInput && !isVoicePipeline) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [input, isRecording, isVoiceInput, isVoicePipeline])

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

  const handleStartVoicePipeline = () => {
    setIsVoicePipeline(true)
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

  const handleVoicePipelineResult = (voiceData) => {
    // Pass the full voice result to parent component
    if (onVoiceResult) {
      onVoiceResult(voiceData)
    }
    setIsVoicePipeline(false)
  }

  const handleCloseVoiceInput = () => {
    setIsVoiceInput(false)
  }

  const handleCloseVoicePipeline = () => {
    setIsVoicePipeline(false)
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
          {isVoicePipeline ? (
            <VoicePipelineInput 
              onVoiceResult={handleVoicePipelineResult} 
              onClose={handleCloseVoicePipeline}
              sessionId={sessionId}
            />
          ) : isVoiceInput ? (
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

              {/* Mic button - Click for voice-to-text */}
              <button
                type="button"
                onClick={handleStartVoiceInput}
                className="input-icon-button"
                aria-label="Voice-to-text"
                disabled={disabled}
                title="Voice-to-text (browser speech recognition)"
              >
                <Mic size={20} />
              </button>

              {/* Voice Pipeline button - Click for audio analysis */}
              <button
                type="button"
                onClick={handleStartVoicePipeline}
                className="input-icon-button voice-pipeline-button"
                aria-label="Voice with emotion analysis"
                disabled={disabled}
                title="Voice with emotion analysis (audio + text fusion)"
              >
                <Waves size={20} />
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
        {!hasMessages && !isRecording && !isVoiceInput && !isVoicePipeline && (
          <p className="input-hint">
            <Mic size={14} style={{display: 'inline', verticalAlign: 'middle'}} /> Voice-to-text | 
            <Waves size={14} style={{display: 'inline', verticalAlign: 'middle', marginLeft: '8px'}} /> Voice with emotion analysis
          </p>
        )}
      </div>
    </>
  )
}

ChatInput.propTypes = {
  onSend: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  hasMessages: PropTypes.bool.isRequired,
  sessionId: PropTypes.string.isRequired,
  onVoiceResult: PropTypes.func,
}

ChatInput.defaultProps = {
  disabled: false,
  onVoiceResult: null,
}
