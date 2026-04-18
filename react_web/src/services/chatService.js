import { apiClient } from '../lib/apiClient'

const CHAT_STREAM_PATH = import.meta.env.VITE_CHAT_STREAM_PATH || '/chat/stream'

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
