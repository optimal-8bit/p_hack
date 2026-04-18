import { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import ChatHistoryItem from './ChatHistoryItem'
import UserProfileSection from './UserProfileSection'
import HealthStatus from './HealthStatus'
import { getAllChats } from '../../services/chatHistoryService'

export default function Sidebar({ activeChat, onChatSelect, onNewChat }) {
  const [chatHistory, setChatHistory] = useState([])
  const [userProfile] = useState({
    name: 'Vaibhav Kumar',
    plan: 'Free',
  })
  const [loading, setLoading] = useState(true)
  const [isOpen, setIsOpen] = useState(true)

  // Load chat history from localStorage
  const loadChatHistory = () => {
    try {
      const chats = getAllChats()
      setChatHistory(chats.map(chat => ({
        id: chat.sessionId,
        title: chat.title,
        updatedAt: chat.updatedAt,
        messageCount: chat.messageCount
      })))
    } catch (error) {
      console.error('Error loading chat history:', error)
      setChatHistory([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadChatHistory()
    
    // Refresh chat history every 2 seconds to catch new messages
    const interval = setInterval(loadChatHistory, 2000)
    return () => clearInterval(interval)
  }, [])

  return (
    <>
      {/* Mobile toggle button */}
      <button
        className="sidebar-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle sidebar"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path
            d="M3 12h18M3 6h18M3 18h18"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      </button>

      <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-content">
          {/* Header */}
          <div className="sidebar-header">
            <button className="new-chat-btn" onClick={onNewChat}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 5v14M5 12h14"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
              <span>New Chat</span>
            </button>
          </div>

          {/* Backend Health Status */}
          <div className="health-section">
            <div className="section-header">
              <h3>Backend Status</h3>
            </div>
            <HealthStatus />
          </div>

          {/* Recents Section */}
          <div className="recents-section">
            <div className="recents-header">
              <h3>Recents</h3>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path
                  d="M6 9l6 6 6-6"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>

            {/* Chat History List */}
            <div className="chat-history-list">
              {loading ? (
                <div className="loading-state">Loading...</div>
              ) : chatHistory.length === 0 ? (
                <div className="empty-state">No chat history yet</div>
              ) : (
                chatHistory.map((chat) => (
                  <ChatHistoryItem
                    key={chat.id}
                    chat={chat}
                    isActive={activeChat === chat.id}
                    onClick={() => onChatSelect(chat.id)}
                  />
                ))
              )}
            </div>
          </div>

          {/* User Profile Section */}
          {userProfile && <UserProfileSection user={userProfile} />}
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isOpen && (
        <div className="sidebar-overlay" onClick={() => setIsOpen(false)} />
      )}
    </>
  )
}

Sidebar.propTypes = {
  activeChat: PropTypes.number,
  onChatSelect: PropTypes.func.isRequired,
  onNewChat: PropTypes.func.isRequired,
}

Sidebar.defaultProps = {
  activeChat: null,
}
