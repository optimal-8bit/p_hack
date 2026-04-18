import { useRef, useEffect } from 'react'
import PropTypes from 'prop-types'
import { Paperclip } from 'lucide-react'
import './UploadMenu.css'

export default function UploadMenu({ isOpen, onClose, onFileSelect }) {
  const menuRef = useRef(null)
  const fileInputRef = useRef(null)

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      onFileSelect(file)
      onClose()
    }
  }

  return (
    <div ref={menuRef} className="upload-menu">
      <button
        onClick={() => fileInputRef.current?.click()}
        className="upload-menu-item"
      >
        <Paperclip size={20} className="upload-menu-icon" />
        <span className="upload-menu-text">Upload file</span>
      </button>
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.jpg,.jpeg,.png,.gif,.webp,.mp4,.mov,.avi,.mkv,.mp3,.wav,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.csv,.zip,.rar,.json,.xml,.svg"
        onChange={handleFileChange}
        className="upload-menu-input"
      />
    </div>
  )
}

UploadMenu.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onFileSelect: PropTypes.func.isRequired,
}
