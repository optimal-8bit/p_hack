import { useState, useRef, useEffect } from 'react'
import Sidebar from '../components/chat/Sidebar'
import ChatContainer from '../components/chat/ChatContainer'
import MessageBubble from '../components/chat/MessageBubble'
import ChatInput from '../components/chat/ChatInput'
import TypingIndicator from '../components/chat/TypingIndicator'
import LightRays from '../components/LightRays'
import VideoBackground from '../components/VideoBackground'
import { chatService } from '../services/chatService'
import { getRandomVideo } from '../utils/videoHelper'
import '../styles/MentalHealthChat.css'

function createMessageId() {
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

export default function MentalHealthChatPage() {
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [inputDisabled, setInputDisabled] = useState(false)
  const [activeChat, setActiveChat] = useState(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [currentVideo, setCurrentVideo] = useState(null)
  const [keepVideoPlaying, setKeepVideoPlaying] = useState(false)
  const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`)
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
    // Reset video when starting new chat
    setKeepVideoPlaying(false)
    setIsStreaming(false)
    setCurrentVideo(null)
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
      isCrisis: false,
    }

    setMessages((prev) => [...prev, userMessage, botMessage])
    setInputDisabled(true)
    setIsTyping(true)
    
    setKeepVideoPlaying(true)
    
    if (!currentVideo) {
      setCurrentVideo(getRandomVideo())
    }
    setIsStreaming(true)

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
        onDone: (result) => {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMessage.id 
                ? { 
                    ...msg, 
                    streaming: false,
                    isCrisis: result?.metadata?.isCrisis || false 
                  } 
                : msg
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
          
          if (!keepVideoPlaying) {
            setIsStreaming(false)
            setCurrentVideo(null)
          }
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

  const handleVoiceResult = (voiceData) => {
    // Voice pipeline returns full analysis
    console.log('Voice analysis:', voiceData)
    
    // Add user message with voice indicator
    const userMessage = {
      id: createMessageId(),
      role: 'user',
      content: `🎤 ${voiceData.transcript}`,
      timestamp: new Date().toISOString(),
      voiceData: voiceData, // Store voice analysis
    }
    
    // Add bot response from voice pipeline
    const botMessage = {
      id: createMessageId(),
      role: 'bot',
      content: voiceData.chat_result?.response_text || 'Processing your message...',
      timestamp: new Date().toISOString(),
      streaming: false,
      isCrisis: voiceData.chat_result?.is_crisis || false,
      voiceAnalysis: {
        fusedEmotion: voiceData.fused_emotion,
        fusedConfidence: voiceData.fused_confidence,
        textEmotion: voiceData.text_only_emotion,
        audioEmotion: voiceData.audio_focused_emotion,
        isIncongruent: voiceData.is_incongruent,
        incongruenceNote: voiceData.incongruence_note,
        stressedWords: voiceData.stressed_words,
      }
    }
    
    setMessages((prev) => [...prev, userMessage, botMessage])
    
    // Start video if not already playing
    setKeepVideoPlaying(true)
    if (!currentVideo) {
      setCurrentVideo(getRandomVideo())
    }
    setIsStreaming(true)
  }

  return (
    <div className="mental-health-chat-page with-sidebar">
      {/* Video Background Layer (only during streaming) */}
      <VideoBackground videoSrc={currentVideo} isActive={isStreaming} />

      {/* Animated Background Layer - Only show when video is NOT playing */}
      {!keepVideoPlaying && (
        <div className="background-layer">
          <LightRays
            raysOrigin="top-center"
            raysColor="#ffffff"
            raysSpeed={0.5}
            lightSpread={1.2}
            rayLength={3}
            followMouse={true}
            mouseInfluence={0.15}
            noiseAmount={0}
            distortion={0}
            pulsating={false}
            fadeDistance={1.5}
            saturation={1.0}
          />
        </div>
      )}

      {/* Overlay for readability */}
      <div className="background-overlay" />

      {/* Main Content */}
      <div className="content-layer">
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
                    isCrisis={message.isCrisis}
                    voiceAnalysis={message.voiceAnalysis}
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
              sessionId={sessionId}
              onVoiceResult={handleVoiceResult}
            />
          </ChatContainer>
        </div>
      </div>
    </div>
  )
}
