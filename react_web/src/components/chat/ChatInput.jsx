import { useState, useRef, useEffect } from 'react'
import PropTypes from 'prop-types'

export default function ChatInput({ onSend, disabled, hasMessages }) {
  const [input, setInput] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [input])

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

  return (
    <div className={`chat-input-wrapper ${hasMessages ? 'with-messages' : 'centered'}`}>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-container">
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
      </form>
      {!hasMessages && (
        <p className="input-hint">Press Enter to send, Shift+Enter for new line</p>
      )}
    </div>
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
