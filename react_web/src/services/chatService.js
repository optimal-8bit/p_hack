import { apiClient } from '../lib/apiClient'
import { getMockResponse, simulateStreaming } from '../mock/mockResponses'

const CHAT_STREAM_PATH = import.meta.env.VITE_CHAT_STREAM_PATH || '/chat/stream'
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || false

function buildFormData({ messages, files, metadata }) {
  const formData = new FormData()
  formData.append('messages', JSON.stringify(messages))

  if (metadata) {
    formData.append('metadata', JSON.stringify(metadata))
  }

  if (files?.length) {
    for (const file of files) {
      formData.append('files', file)
    }
  }

  return formData
}

export const chatService = {
  async streamReply({ messages, files = [], metadata, signal, onToken, onDone, onError }) {
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

    // Use real backend API
    const body = buildFormData({ messages, files, metadata })

    try {
      await apiClient.stream(CHAT_STREAM_PATH, {
        method: 'POST',
        body,
        signal,
        onMessage: (chunk) => {
          if (chunk?.error) {
            throw new Error(chunk.error)
          }

          const token = chunk?.delta || chunk?.token || chunk?.content || chunk?.text || ''
          if (token) {
            onToken?.(token)
          }

          if (chunk?.done === true) {
            onDone?.(chunk)
          }
        },
      })

      onDone?.({ done: true })
    } catch (error) {
      onError?.(error)
      throw error
    }
  },
}
