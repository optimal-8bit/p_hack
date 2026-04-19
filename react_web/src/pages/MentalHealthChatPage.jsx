import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/chat/Sidebar'
import ChatContainer from '../components/chat/ChatContainer'
import MessageBubble from '../components/chat/MessageBubble'
import ChatInput from '../components/chat/ChatInput'
import TypingIndicator from '../components/chat/TypingIndicator'
import LightRays from '../components/LightRays'
import VideoBackground from '../components/VideoBackground'
import WebcamEmotionDetector from '../components/WebcamEmotionDetector'
import TTSControl from '../components/chat/TTSControl'
import { CameraIcon } from '../components/CameraIcon'
import { chatService } from '../services/chatService'
import { saveChat, getChatBySessionId } from '../services/chatHistoryService'
import { getRandomVideo } from '../utils/videoHelper'
import { useTextToSpeech } from '../hooks/useTextToSpeech'
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
  const [sessionId, setSessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`)
  const [webcamEnabled, setWebcamEnabled] = useState(false)
  const [currentFacialEmotion, setCurrentFacialEmotion] = useState(null)
  const messagesEndRef = useRef(null)
  const abortControllerRef = useRef(null)
  const navigate = useNavigate()

  // Initialize TTS hook
  const { isSupported, isMuted, isSpeaking, toggleMute, cancelSpeech } = useTextToSpeech()

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      saveChat(sessionId, messages)
    }
  }, [messages, sessionId])

  // Log webcam state changes
  useEffect(() => {
    console.log('📹 [CHAT] Webcam state changed:', { 
      enabled: webcamEnabled,
      hasEmotion: !!currentFacialEmotion,
      emotion: currentFacialEmotion?.dominant_emotion
    });
  }, [webcamEnabled, currentFacialEmotion]);

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
    // Generate new session ID
    setSessionId(`session-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`)
    // Reset video when starting new chat
    setKeepVideoPlaying(false)
    setIsStreaming(false)
    setCurrentVideo(null)
  }

  const handleChatSelect = async (chatId) => {
    setActiveChat(chatId)
    
    // Load chat from localStorage
    const chat = getChatBySessionId(chatId)
    if (chat) {
      setMessages(chat.messages)
      setSessionId(chat.sessionId)
      console.log('Loaded chat:', chatId, 'with', chat.messages.length, 'messages')
    } else {
      console.warn('Chat not found:', chatId)
    }
  }

  const handleSendMessage = async (userInput) => {
    if (!userInput.trim() || inputDisabled) return

    // Cancel any ongoing speech when user sends a new message
    cancelSpeech();

    console.log('💬 [CHAT] Sending message:', {
      message: userInput.trim(),
      hasFacialEmotion: !!currentFacialEmotion,
      facialEmotion: currentFacialEmotion?.dominant_emotion,
      facialConfidence: currentFacialEmotion?.confidence
    });

    const userMessage = {
      id: createMessageId(),
      role: 'user',
      content: userInput.trim(),
      timestamp: new Date().toISOString(),
      facialEmotion: currentFacialEmotion, // Include facial emotion if available
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

    // Simple parallel TTS: Start early indicator, then speak complete response
    let accumulatedResponse = '';
    let shouldSpeak = false;
    let hasReachedTwoLines = false; // Track if we've reached 2 lines for this message

    console.log('🎯 [TTS] Starting new message processing');

    try {
      await chatService.streamReply({
        messages: conversationHistory,
        signal: controller.signal,
        sessionId: sessionId,
        facialEmotion: currentFacialEmotion, // Pass facial emotion to backend
        onToken: (token) => {
          // Update the streaming message
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMessage.id ? { ...msg, content: msg.content + token } : msg
            )
          )
          
          // Accumulate response
          accumulatedResponse += token;
          
          // Mark that we should speak after 2 lines appear (only check once per message)
          if (!hasReachedTwoLines && isSupported && !isMuted) {
            const lineCount = (accumulatedResponse.match(/\n/g) || []).length;
            const hasEnoughContent = accumulatedResponse.length >= 100;
            
            console.log('🎯 [TTS] Checking lines:', lineCount, 'chars:', accumulatedResponse.length);
            
            if (lineCount >= 2 || hasEnoughContent) {
              hasReachedTwoLines = true;
              shouldSpeak = true;
              console.log('🎯 [TTS] ✅ 2 lines detected! Will speak complete response when ready');
              console.log('🎯 [TTS] Current content preview:', accumulatedResponse.substring(0, 100) + '...');
            }
          }
        },
        onDone: (result) => {
          console.log('✅ [CHAT] Message completed:', {
            emotionAnalysis: result?.metadata?.emotionAnalysis,
            isMultimodal: result?.metadata?.isMultimodal,
            congruence: result?.metadata?.emotionCongruence
          });
          
          // FORCE DOCTOR RECOMMENDATION FOR TESTING
          const forcedRecommendation = {
            should_recommend: true,
            specialization: "psychologist",
            reason: "Based on our conversation, I think speaking with a mental health professional could be beneficial. They can provide personalized support and guidance tailored to your specific situation.",
            urgency: "normal"
          };
          
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMessage.id 
                ? { 
                    ...msg, 
                    streaming: false,
                    isCrisis: result?.metadata?.isCrisis || false,
                    emotionAnalysis: result?.metadata?.emotionAnalysis,
                    doctorRecommendation: result?.metadata?.doctorRecommendation || forcedRecommendation
                  } 
                : msg
            )
          );
          
          // Speak the COMPLETE response when streaming finishes
          console.log('🎯 [TTS] Stream finished. shouldSpeak:', shouldSpeak, 'isSupported:', isSupported, 'isMuted:', isMuted);
          console.log('🎯 [TTS] Final response length:', accumulatedResponse.length);
          
          if (shouldSpeak && isSupported && !isMuted && accumulatedResponse.trim()) {
            console.log('🎯 [TTS] ✅ Speaking COMPLETE response:', accumulatedResponse.length, 'chars');
            console.log('🎯 [TTS] Speech synthesis state:', {
              speaking: window.speechSynthesis.speaking,
              pending: window.speechSynthesis.pending,
              paused: window.speechSynthesis.paused
            });
            
            // Cancel any existing speech before starting new one
            if (window.speechSynthesis.speaking) {
              console.log('🎯 [TTS] Canceling existing speech');
              window.speechSynthesis.cancel();
            }
            
            setTimeout(() => {
              const utterance = new SpeechSynthesisUtterance(accumulatedResponse);
              utterance.rate = 0.9; // Calm rate
              utterance.pitch = 1.0;
              utterance.volume = 1.0;
              
              // Get appropriate voice for language
              const voices = window.speechSynthesis.getVoices();
              const targetLang = result?.metadata?.detected_language || 'en';
              const voice = voices.find(v => v.lang.startsWith(targetLang)) || voices[0];
              if (voice) utterance.voice = voice;
              
              utterance.onstart = () => {
                console.log('🗣️ [TTS] ✅ Started speaking complete response');
                console.log('🗣️ [TTS] Text being spoken:', accumulatedResponse.substring(0, 100) + '...');
                console.log('🗣️ [TTS] Full text length:', accumulatedResponse.length);
              };
              
              utterance.onend = () => {
                console.log('✅ [TTS] ✅ Finished speaking complete response');
                console.log('✅ [TTS] Speech completed successfully');
              };
              
              utterance.onerror = (event) => {
                console.error('❌ [TTS] Speech error:', event.error);
                console.error('❌ [TTS] Error details:', event);
              };
              
              utterance.onpause = () => {
                console.log('⏸️ [TTS] Speech paused');
              };
              
              utterance.onresume = () => {
                console.log('▶️ [TTS] Speech resumed');
              };
              
              utterance.onboundary = (event) => {
                console.log('🎯 [TTS] Speech boundary:', event.name, 'at char:', event.charIndex);
              };
              
              window.speechSynthesis.speak(utterance);
            }, 50);
          } else if (!shouldSpeak && isSupported && !isMuted && accumulatedResponse.trim()) {
            // Short response (less than 2 lines) - speak it anyway
            console.log('🎯 [TTS] ✅ Speaking short response:', accumulatedResponse.length, 'chars');
            
            setTimeout(() => {
              const utterance = new SpeechSynthesisUtterance(accumulatedResponse);
              utterance.rate = 0.9;
              utterance.pitch = 1.0;
              utterance.volume = 1.0;
              
              const voices = window.speechSynthesis.getVoices();
              const targetLang = result?.metadata?.detected_language || 'en';
              const voice = voices.find(v => v.lang.startsWith(targetLang)) || voices[0];
              if (voice) utterance.voice = voice;
              
              utterance.onstart = () => {
                console.log('🗣️ [TTS] ✅ Started speaking short response');
              };
              
              utterance.onend = () => {
                console.log('✅ [TTS] ✅ Finished speaking short response');
              };
              
              window.speechSynthesis.speak(utterance);
            }, 50);
          } else {
            console.log('❌ [TTS] Not speaking because:', {
              shouldSpeak,
              isSupported,
              isMuted,
              hasContent: !!accumulatedResponse.trim()
            });
          }
          
          setIsTyping(false)
          setInputDisabled(false)
        },
        onError: (error) => {
          console.error('❌ [CHAT] Chat error:', error)
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
        console.error('❌ [CHAT] Streaming error:', error)
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
    console.log('Is crisis?', voiceData.chat_result?.is_crisis)
    
    // Add user message with voice indicator
    const userMessage = {
      id: createMessageId(),
      role: 'user',
      content: `🎤 ${voiceData.transcript}`,
      timestamp: new Date().toISOString(),
      voiceData: voiceData, // Store voice analysis
    }
    
    // Check if this is a crisis response
    const isCrisis = voiceData.chat_result?.is_crisis || false
    
    // Add bot response from voice pipeline
    const botMessage = {
      id: createMessageId(),
      role: 'bot',
      content: voiceData.chat_result?.response_text || 'Processing your message...',
      timestamp: new Date().toISOString(),
      streaming: false,
      isCrisis: isCrisis,
      // Only show voice analysis if NOT a crisis
      voiceAnalysis: isCrisis ? null : {
        fusedEmotion: voiceData.fused_emotion,
        fusedConfidence: voiceData.fused_confidence,
        textEmotion: voiceData.text_only_emotion,
        audioEmotion: voiceData.audio_focused_emotion,
        isIncongruent: voiceData.is_incongruent,
        incongruenceNote: voiceData.incongruence_note,
        stressedWords: voiceData.stressed_words,
      }
    }
    
    console.log('Bot message:', botMessage)
    
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
          {/* Webcam Emotion Detector - Top Right Corner */}
          {webcamEnabled && (
            <div className="webcam-detector-container">
              <WebcamEmotionDetector
                enabled={webcamEnabled}
                onEmotionDetected={setCurrentFacialEmotion}
                onClose={() => setWebcamEnabled(false)}
                compact={true}
              />
            </div>
          )}

          {/* TTS Control Button */}
          {isSupported && (
            <TTSControl 
              isMuted={isMuted}
              onToggle={toggleMute}
              isSpeaking={isSpeaking}
            />
          )}

          {/* Webcam Toggle Button */}
          <button
            className={`webcam-toggle-btn ${webcamEnabled ? 'active' : ''}`}
            onClick={() => setWebcamEnabled(!webcamEnabled)}
            title={webcamEnabled ? 'Disable facial emotion detection' : 'Enable facial emotion detection'}
          >
            <CameraIcon className="w-6 h-6" />
          </button>

          <ChatContainer hasMessages={hasMessages}>
            {!hasMessages ? (
              <div className="welcome-screen">
                <div className="welcome-content">
                  <h1>Mental Health Support</h1>
                  <p>I'm here to listen and support you. How are you feeling today?</p>
                  <div className="feature-hint">
                    <p className="hint-text">
                      💡 Enable webcam emotion detection for enhanced support
                    </p>
                  </div>
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
                    emotionAnalysis={message.emotionAnalysis}
                    facialEmotion={message.facialEmotion}
                    doctorRecommendation={message.doctorRecommendation}
                    sessionId={sessionId}
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
