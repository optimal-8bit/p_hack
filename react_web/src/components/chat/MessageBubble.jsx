import { useEffect, useState } from 'react'
import PropTypes from 'prop-types'

export default function MessageBubble({ role, content, streaming, error }) {
  const [displayedContent, setDisplayedContent] = useState('')

  useEffect(() => {
    // For bot messages that are streaming, show content as it arrives
    if (role === 'bot' && streaming) {
      setDisplayedContent(content)
    } else {
      // For completed messages or user messages, show full content
      setDisplayedContent(content)
    }
  }, [content, streaming, role])

  const formattedContent = displayedContent.split('\n').map((line, idx) => (
    <span key={idx}>
      {line}
      {idx < displayedContent.split('\n').length - 1 && <br />}
    </span>
  ))

  return (
    <div className={`message-bubble-wrapper ${role}`}>
      <div className={`message-bubble ${role} ${error ? 'error' : ''}`}>
        <div className="message-content">
          {formattedContent}
          {streaming && role === 'bot' && displayedContent.length > 0 && (
            <span className="cursor">|</span>
          )}
        </div>
      </div>
    </div>
  )
}

MessageBubble.propTypes = {
  role: PropTypes.oneOf(['user', 'bot']).isRequired,
  content: PropTypes.string.isRequired,
  streaming: PropTypes.bool,
  error: PropTypes.bool,
}

MessageBubble.defaultProps = {
  streaming: false,
  error: false,
}
