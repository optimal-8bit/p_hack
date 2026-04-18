import { useState, useRef, useEffect } from 'react'
import Sidebar from '../components/chat/Sidebar'
import ChatContainer from '../components/chat/ChatContainer'
import MessageBubble from '../components/chat/MessageBubble'
import ChatInput from '../components/chat/ChatInput'
import TypingIndicator from '../components/chat/TypingIndicator'
import { chatService } from '../services/chatService'
import '../styles/MentalHealthChat.css'

function createMessageId() {
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

export default function MentalHealthChatPage() {
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [inputDisabled, setInputDisabled] = useState(false)
  const [activeChat, setActiveChat] = useState(null)
  const messagesEndRef = useRef(null)
  const abortControllerRef = useRef(null)

  const hasMessages = messages.length > 0

  const scrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
    }, 100)
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  const handleNewChat = () => {
    setMessages([])
    setActiveChat(null)
  }

  const handleChatSelect = async (chatId) => {
    setActiveChat(chatId)
    // TODO: Load chat messages from backend
    // const chatMessages = await apiClient.get(`/chat/${chatId}/messages`)
    // setMessages(chatMessages)
    console.log('Selected chat:', chatId)
  }

  const handleSendMessage = async (userInput) => {
    if (!userInput.trim() || inputDisabled) return

    const userMessage = {
      id: createMessageId(),
      role: 'user',
      content: userInput.trim(),
      timestamp: new Date().toISOString(),
    }

    const botMessage = {
      id: createMessageId(),
      role: 'bot',
      content: '',
      timestamp: new Date().toISOString(),
      streaming: true,
    }

    setMessages((prev) => [...prev, userMessage, botMessage])
    setInputDisabled(true)
    setIsTyping(true)

    const controller = new AbortController()
    abortControllerRef.current = controller

    const conversationHistory = [
      ...messages.map((msg) => ({ role: msg.role === 'bot' ? 'assistant' : 'user', content: msg.content })),
      { role: 'user', content: userInput.trim() },
    ]

    try {
      await chatService.streamReply({
        messages: conversationHistory,
        signal: controller.signal,
        onToken: (token) => {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMessage.id ? { ...msg, content: msg.content + token } : msg
            )
          )
        },
        onDone: () => {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMessage.id ? { ...msg, streaming: false } : msg
            )
          )
          setIsTyping(false)
          setInputDisabled(false)
        },
        onError: (error) => {
          console.error('Chat error:', error)
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMessage.id
                ? { ...msg, content: 'Sorry, I encountered an error. Please try again.', streaming: false, error: true }
                : msg
            )
          )
          setIsTyping(false)
          setInputDisabled(false)
        },
      })
    } catch (error) {
      if (!controller.signal.aborted) {
        console.error('Streaming error:', error)
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === botMessage.id
              ? { ...msg, content: 'Sorry, something went wrong. Please try again.', streaming: false, error: true }
              : msg
          )
        )
      }
      setIsTyping(false)
      setInputDisabled(false)
    } finally {
      abortControllerRef.current = null
    }
  }

  return (
    <div className="mental-health-chat-page with-sidebar">
      <Sidebar
        activeChat={activeChat}
        onChatSelect={handleChatSelect}
        onNewChat={handleNewChat}
      />

      <div className="chat-main-area">
        <ChatContainer hasMessages={hasMessages}>
          {!hasMessages ? (
            <div className="welcome-screen">
              <div className="welcome-content">
                <h1>Mental Health Support</h1>
                <p>I'm here to listen and support you. How are you feeling today?</p>
              </div>
            </div>
          ) : (
            <div className="messages-container">
              {messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  role={message.role}
                  content={message.content}
                  streaming={message.streaming}
                  error={message.error}
                />
              ))}
              {isTyping && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </div>
          )}

          <ChatInput
            onSend={handleSendMessage}
            disabled={inputDisabled}
            hasMessages={hasMessages}
          />
        </ChatContainer>
      </div>
    </div>
  )
}
