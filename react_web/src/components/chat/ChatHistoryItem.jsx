import PropTypes from 'prop-types'

export default function ChatHistoryItem({ chat, isActive, onClick }) {
  return (
    <button
      className={`chat-history-item ${isActive ? 'active' : ''}`}
      onClick={onClick}
    >
      <div className="chat-history-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path
            d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      <span className="chat-history-title">{chat.title}</span>
    </button>
  )
}

ChatHistoryItem.propTypes = {
  chat: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
  }).isRequired,
  isActive: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
}

ChatHistoryItem.defaultProps = {
  isActive: false,
}
