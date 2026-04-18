import { motion } from 'motion/react'
import { Send, Plus, X } from 'lucide-react'
import PropTypes from 'prop-types'
import { useRef } from 'react'
import { CameraIcon } from './CameraIcon'

function formatFileSize(size) {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / (1024 * 1024)).toFixed(1)} MB`
}

export function InputBar({
  draft,
  setDraft,
  files,
  onSelectFiles,
  removeFile,
  onSubmit,
  canSend,
  isStreaming,
}) {
  const fileInputRef = useRef(null)

  const handleFileClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="border-t border-gray-200 bg-white px-4 py-4">
      {/* Pending Files */}
      {files.length > 0 && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="mb-3 flex flex-wrap gap-2"
        >
          {files.map((file) => (
            <motion.div
              key={file.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex items-center gap-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-xl text-sm"
            >
              <div className="flex flex-col">
                <span className="font-medium text-gray-900">{file.name}</span>
                <span className="text-xs text-gray-500">{formatFileSize(file.size)}</span>
              </div>
              <motion.button
                type="button"
                onClick={() => removeFile(file.name)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="p-1 hover:bg-red-50 rounded-full transition-colors"
              >
                <X className="w-4 h-4 text-red-500" />
              </motion.button>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Input Form */}
      <form onSubmit={onSubmit} className="relative">
        <div
          className="
            flex items-end gap-2 px-4 py-2 
            bg-gray-50 border-2 border-gray-200 
            rounded-full shadow-sm
            transition-all duration-200 ease-in-out
            focus-within:border-blue-500 focus-within:shadow-md focus-within:bg-white
          "
        >
          {/* Plus Button */}
          <motion.button
            type="button"
            onClick={handleFileClick}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-all duration-200"
            aria-label="Add attachment"
          >
            <Plus className="w-5 h-5" strokeWidth={2} />
          </motion.button>

          {/* Camera Icon */}
          <motion.button
            type="button"
            onClick={handleFileClick}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="p-2 hover:bg-blue-50 rounded-full transition-all duration-200 flex items-center justify-center"
            aria-label="Attach image"
          >
            <CameraIcon className="w-6 h-6" />
          </motion.button>

          {/* Hidden File Input */}
          <input
            ref={fileInputRef}
            type="file"
            multiple
            className="hidden"
            onChange={onSelectFiles}
            aria-label="File input"
          />

          {/* Text Input */}
          <textarea
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                if (canSend) {
                  onSubmit(e)
                }
              }
            }}
            placeholder="Message the assistant..."
            rows={1}
            className="
              flex-1 bg-transparent border-none outline-none resize-none
              text-gray-900 placeholder-gray-400
              text-sm leading-6
              max-h-32 overflow-y-auto
              scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent
            "
            style={{
              minHeight: '24px',
              maxHeight: '128px',
            }}
          />

          {/* Send Button */}
          <motion.button
            type="submit"
            disabled={!canSend}
            whileHover={canSend ? { scale: 1.1 } : {}}
            whileTap={canSend ? { scale: 0.95 } : {}}
            className={`
              p-2 rounded-full transition-all duration-200
              ${
                canSend
                  ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-md hover:shadow-lg'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }
            `}
            aria-label="Send message"
          >
            <Send className="w-5 h-5" strokeWidth={2} />
          </motion.button>
        </div>
      </form>

      {/* Streaming Indicator */}
      {isStreaming && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-xs text-gray-500 mt-2 text-center"
        >
          Assistant is typing...
        </motion.p>
      )}
    </div>
  )
}

InputBar.propTypes = {
  draft: PropTypes.string.isRequired,
  setDraft: PropTypes.func.isRequired,
  files: PropTypes.array.isRequired,
  onSelectFiles: PropTypes.func.isRequired,
  removeFile: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  canSend: PropTypes.bool.isRequired,
  isStreaming: PropTypes.bool.isRequired,
}
