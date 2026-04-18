import { getMockResponse, simulateStreaming } from '../mock/mockResponses'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || false

// Generate a session ID (stored in sessionStorage for persistence across page reloads)
function getSessionId() {
  let sessionId = sessionStorage.getItem('mental_health_session_id')
  if (!sessionId) {
    sessionId = `session-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
    sessionStorage.setItem('mental_health_session_id', sessionId)
  }
  return sessionId
}

// Simulate streaming by yielding characters from the full response
async function simulateStreamingFromResponse(text, signal, onToken, delay = 20) {
  for (let i = 0; i < text.length; i++) {
    if (signal?.aborted) throw new Error('Aborted')
    await new Promise(resolve => setTimeout(resolve, delay))
    onToken(text[i])
  }
}

export const chatService = {
  async streamReply({ messages, signal, onToken, onDone, onError }) {
    // Check if we should use mock responses
    if (USE_MOCK) {
      try {
        // Get the last user message
        const lastUserMessage = messages[messages.length - 1]?.content || ''
        
        // Get mock response
        const mockResponse = getMockResponse(lastUserMessage)
        
        // Simulate streaming with typewriter effect
        // 300ms initial delay (thinking time), then 20ms per character
        await simulateStreaming(
          mockResponse,
          (char) => {
            if (signal?.aborted) throw new Error('Aborted')
            onToken?.(char)
          },
          20,   // 20ms delay between characters
          300   // 300ms initial delay before starting
        )
        
        onDone?.({ done: true })
        return
      } catch (error) {
        if (error.message === 'Aborted') {
          return
        }
        onError?.(error)
        throw error
      }
    }

    // Use real Mental Health Chatbot backend API
    try {
      // Get the last user message
      const lastUserMessage = messages[messages.length - 1]?.content || ''
      
      if (!lastUserMessage.trim()) {
        throw new Error('Message cannot be empty')
      }

      // Call the backend API
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: getSessionId(),
          message: lastUserMessage
        }),
        signal
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      // Simulate streaming the response text character by character
      // This provides a nice typewriter effect even though the backend returns the full response
      await simulateStreamingFromResponse(
        data.response_text,
        signal,
        onToken,
        20 // 20ms per character
      )

      // Call onDone with metadata from the backend
      onDone?.({
        done: true,
        metadata: {
          emotion: data.emotion?.emotion,
          emotionConfidence: data.emotion?.confidence,
          intent: data.intent?.intent,
          intentConfidence: data.intent?.confidence,
          language: data.detected_language,
          isCrisis: data.is_crisis,
          processingTime: data.processing_time_ms,
          turnNumber: data.turn_number
        }
      })

    } catch (error) {
      if (error.name === 'AbortError' || error.message === 'Aborted') {
        return
      }
      console.error('Chat service error:', error)
      onError?.(error)
      throw error
    }
  },

  // Get session history
  async getHistory() {
    try {
      const sessionId = getSessionId()
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/history`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error fetching history:', error)
      throw error
    }
  },

  // Clear session
  async clearSession() {
    try {
      const sessionId = getSessionId()
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      // Generate new session ID
      sessionStorage.removeItem('mental_health_session_id')
      
      return await response.json()
    } catch (error) {
      console.error('Error clearing session:', error)
      throw error
    }
  },

  // Get health status
  async getHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error fetching health:', error)
      throw error
    }
  },

  // Get supported languages
  async getSupportedLanguages() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/supported-languages`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error fetching languages:', error)
      throw error
    }
  }
}
