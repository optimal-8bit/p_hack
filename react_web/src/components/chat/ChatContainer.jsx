import PropTypes from 'prop-types'

export default function ChatContainer({ children, hasMessages }) {
  return (
    <div className={`chat-container ${hasMessages ? 'has-messages' : 'empty'}`}>
      {children}
    </div>
  )
}

ChatContainer.propTypes = {
  children: PropTypes.node.isRequired,
  hasMessages: PropTypes.bool.isRequired,
}
