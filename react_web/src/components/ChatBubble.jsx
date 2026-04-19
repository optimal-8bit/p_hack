import { motion, AnimatePresence } from 'motion/react'
import PropTypes from 'prop-types'
import { MarkdownView } from './MarkdownView'
import { LoadingIndicator } from './LoadingIndicator'

function formatFileSize(size) {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / (1024 * 1024)).toFixed(1)} MB`
}

export function ChatBubble({ message, isStreaming }) {
  const isUser = message.role === 'user'
  const isAssistant = message.role === 'assistant'

  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} w-full`}
    >
      <div
        className={`
          max-w-[85%] md:max-w-[75%] rounded-2xl px-4 py-3 shadow-sm
          ${
            isUser
              ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white'
              : 'bg-white border border-gray-200 text-gray-900'
          }
        `}
      >
        <div className="flex items-center gap-2 mb-2">
          <span
            className={`
              text-xs font-semibold uppercase tracking-wider
              ${isUser ? 'text-blue-100' : 'text-gray-500'}
            `}
          >
            {isAssistant ? 'Assistant' : 'You'}
          </span>
        </div>

        <AnimatePresence mode="wait">
          {isStreaming && !message.content ? (
            <motion.div
              key="loading"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.3, ease: 'easeInOut' }}
            >
              <LoadingIndicator variant="light" />
            </motion.div>
          ) : (
            <motion.div
              key="content"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
            >
              <MarkdownView content={message.content} isUser={isUser} />
            </motion.div>
          )}
        </AnimatePresence>

        {message.files?.length > 0 && (
          <motion.ul
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="flex flex-wrap gap-2 mt-3"
          >
            {message.files.map((file) => (
              <li
                key={`${message.id}-${file.name}`}
                className={`
                  inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs
                  ${
                    isUser
                      ? 'bg-blue-500/30 text-blue-50'
                      : 'bg-gray-100 text-gray-700 border border-gray-200'
                  }
                `}
              >
                <span className="font-medium truncate max-w-[150px]">{file.name}</span>
                <span className="text-[10px] opacity-75">{formatFileSize(file.size)}</span>
              </li>
            ))}
          </motion.ul>
        )}
      </div>
    </motion.article>
  )
}

ChatBubble.propTypes = {
  message: PropTypes.shape({
    id: PropTypes.string.isRequired,
    role: PropTypes.oneOf(['user', 'assistant']).isRequired,
    content: PropTypes.string,
    files: PropTypes.arrayOf(
      PropTypes.shape({
        name: PropTypes.string.isRequired,
        size: PropTypes.number.isRequired,
        type: PropTypes.string,
      }),
    ),
    createdAt: PropTypes.string.isRequired,
  }).isRequired,
  isStreaming: PropTypes.bool,
}
