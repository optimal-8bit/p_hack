import { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { Phone, MessageCircle, Heart } from 'lucide-react'
import './EmergencyBubble.css'

export default function EmergencyBubble({ content, streaming }) {
  const [displayedContent, setDisplayedContent] = useState('')

  useEffect(() => {
    setDisplayedContent(content)
  }, [content])

  // Parse the crisis response to extract helpline numbers and message
  const parseEmergencyContent = (text) => {
    const lines = text.split('\n').filter(line => line.trim())
    const helplines = []
    const messageParts = []
    
    lines.forEach(line => {
      // Check if line contains a helpline number
      if (line.includes('🆘') || line.includes('iCall') || line.includes('Emergency')) {
        helplines.push(line.trim())
      } else if (line.trim()) {
        messageParts.push(line.trim())
      }
    })

    return { helplines, message: messageParts.join(' ') }
  }

  const { helplines, message } = parseEmergencyContent(displayedContent)

  // Extract phone numbers from helplines
  const extractPhoneNumber = (text) => {
    const match = text.match(/\d{3,}/g)
    return match ? match[0] : null
  }

  return (
    <div className="message-bubble-wrapper bot">
      <div className="message-bubble bot crisis-bubble">
        {/* Gentle header with heart */}
        <div className="crisis-header">
          <Heart className="crisis-heart" size={20} />
          <span className="crisis-header-text">I'm here for you</span>
        </div>

        {/* Main compassionate message */}
        <div className="crisis-message">
          <p>{message}</p>
        </div>

        {/* Compact helpline section */}
        {helplines.length > 0 && (
          <div className="crisis-helplines">
            <div className="crisis-helplines-label">Someone to talk to:</div>
            {helplines.map((helpline, idx) => {
              const phoneNumber = extractPhoneNumber(helpline)
              const isChat = helpline.includes('Chat') || helpline.includes('icall')
              
              // Clean up the helpline text
              let cleanText = helpline.replace('🆘', '').trim()
              
              return (
                <div key={idx} className="crisis-helpline-item">
                  <div className="crisis-helpline-icon">
                    {isChat ? <MessageCircle size={14} /> : <Phone size={14} />}
                  </div>
                  <div className="crisis-helpline-info">
                    <span className="crisis-helpline-text">{cleanText}</span>
                    {phoneNumber && !isChat && (
                      <a 
                        href={`tel:${phoneNumber}`} 
                        className="crisis-helpline-link"
                        onClick={(e) => {
                          // On desktop, copy to clipboard instead
                          if (window.innerWidth > 768) {
                            e.preventDefault()
                            navigator.clipboard.writeText(phoneNumber)
                            const btn = e.target
                            const originalText = btn.textContent
                            btn.textContent = 'Copied!'
                            setTimeout(() => {
                              btn.textContent = originalText
                            }, 2000)
                          }
                        }}
                      >
                        Call
                      </a>
                    )}
                    {isChat && helpline.includes('icallhelpline.org') && (
                      <a 
                        href="https://icallhelpline.org" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="crisis-helpline-link"
                      >
                        Chat
                      </a>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}

        {/* Gentle closing */}
        <div className="crisis-footer">
          <p>💙 Let's talk through this together. What's on your mind?</p>
        </div>

        {/* Streaming Cursor */}
        {streaming && displayedContent.length > 0 && (
          <span className="cursor">|</span>
        )}
      </div>
    </div>
  )
}

EmergencyBubble.propTypes = {
  content: PropTypes.string.isRequired,
  streaming: PropTypes.bool,
}

EmergencyBubble.defaultProps = {
  streaming: false,
}
