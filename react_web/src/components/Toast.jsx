import { useEffect } from 'react'
import PropTypes from 'prop-types'
import { X, FileText, Image, Video, Music, FileSpreadsheet, Presentation, Archive, File } from 'lucide-react'
import './Toast.css'

const getFileIcon = (fileType) => {
  if (fileType.includes('Image') || fileType.includes('SVG')) return Image
  if (fileType.includes('Video')) return Video
  if (fileType.includes('Audio')) return Music
  if (fileType.includes('Spreadsheet') || fileType.includes('CSV')) return FileSpreadsheet
  if (fileType.includes('Presentation')) return Presentation
  if (fileType.includes('Archive')) return Archive
  if (fileType.includes('PDF') || fileType.includes('Word') || fileType.includes('Text') || fileType.includes('JSON') || fileType.includes('XML')) return FileText
  return File
}

export default function Toast({ fileInfo, onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose()
    }, 5000) // Auto-close after 5 seconds

    return () => clearTimeout(timer)
  }, [onClose])

  if (!fileInfo) return null

  const Icon = getFileIcon(fileInfo.type)

  return (
    <div className="toast-container">
      <div className="toast">
        <div className="toast-icon">
          <Icon size={24} />
        </div>
        <div className="toast-content">
          <div className="toast-title">File Selected</div>
          <div className="toast-filename">{fileInfo.name}</div>
          <div className="toast-details">
            <span className="toast-type">{fileInfo.type}</span>
            <span className="toast-separator">•</span>
            <span className="toast-size">{fileInfo.size}</span>
          </div>
        </div>
        <button className="toast-close" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>
      </div>
    </div>
  )
}

Toast.propTypes = {
  fileInfo: PropTypes.shape({
    name: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    size: PropTypes.string.isRequired,
  }),
  onClose: PropTypes.func.isRequired,
}
