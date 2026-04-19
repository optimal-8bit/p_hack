const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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
  async streamReply({ messages, signal, sessionId, facialEmotion, onToken, onDone, onError }) {
    // Use real Mental Health Chatbot backend API
    try {
      // Get the last user message
      const lastUserMessage = messages[messages.length - 1]?.content || ''
      
      if (!lastUserMessage.trim()) {
        throw new Error('Message cannot be empty')
      }

      // Prepare request body
      const requestBody = {
        session_id: sessionId || getSessionId(),
        message: lastUserMessage
      }

      // Add facial emotion data if available
      if (facialEmotion) {
        requestBody.facial_emotion = {
          dominant_emotion: facialEmotion.dominant_emotion,
          confidence: facialEmotion.confidence,
          all_emotions: facialEmotion.all_emotions,
          age: facialEmotion.age,
          gender: facialEmotion.gender,
          timestamp: facialEmotion.timestamp
        }
        console.log('Sending facial emotion data:', requestBody.facial_emotion)
      }

      // Call the backend API
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      // Log emotion analysis if multimodal
      if (data.emotion?.is_multimodal) {
        console.log('Multimodal emotion analysis:', {
          textEmotion: data.emotion.emotion,
          facialEmotion: data.emotion.facial_emotion,
          congruence: data.emotion.emotion_congruence
        })
      }

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
          facialEmotion: data.emotion?.facial_emotion,
          facialConfidence: data.emotion?.facial_confidence,
          isMultimodal: data.emotion?.is_multimodal,
          emotionCongruence: data.emotion?.emotion_congruence,
          intent: data.intent?.intent,
          intentConfidence: data.intent?.confidence,
          language: data.detected_language,
          isCrisis: data.is_crisis,
          processingTime: data.processing_time_ms,
          turnNumber: data.turn_number,
          emotionAnalysis: data.emotion?.is_multimodal ? {
            textEmotion: data.emotion.emotion,
            facialEmotion: data.emotion.facial_emotion,
            congruence: data.emotion.emotion_congruence
          } : null,
          doctorRecommendation: data.doctor_recommendation || null
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
      // Silently fail - health check is optional
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
