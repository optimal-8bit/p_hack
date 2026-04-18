import { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import ChatHistoryItem from './ChatHistoryItem'
import UserProfileSection from './UserProfileSection'
import { apiClient } from '../../lib/apiClient'

export default function Sidebar({ activeChat, onChatSelect, onNewChat }) {
  const [chatHistory, setChatHistory] = useState([])
  const [userProfile, setUserProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isOpen, setIsOpen] = useState(true)

  useEffect(() => {
    fetchChatHistory()
    fetchUserProfile()
  }, [])

  const fetchChatHistory = async () => {
    try {
      const data = await apiClient.get('/chat/history')
      setChatHistory(data || [])
    } catch (error) {
      console.error('Failed to fetch chat history:', error)
      // Use mock data if API fails
      setChatHistory([
        { id: 1, title: 'Test Message' },
        { id: 2, title: 'Offline AI Healthcare Hackathon' },
        { id: 3, title: 'Crank Pin vs Gudgeon Pin' },
        { id: 4, title: 'Diminishing Returns Analysis' },
        { id: 5, title: 'Competing in Hackathons' },
        { id: 6, title: 'NASA Space Apps Hybrid' },
        { id: 7, title: 'Log out Gmail all devices' },
        { id: 8, title: 'Resume PDF Creation' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const fetchUserProfile = async () => {
    try {
      const data = await apiClient.get('/user/profile')
      setUserProfile(data)
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
      // Use mock data if API fails
      setUserProfile({
        name: 'Vaibhav Kumar',
        plan: 'Free',
      })
    }
  }

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
                <div className="empty-state">No chat history</div>
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
