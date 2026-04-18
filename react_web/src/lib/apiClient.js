import { getAccessToken } from './authToken'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || 'http://localhost:8000/api/v1'

async function request(path, options = {}) {
  const token = getAccessToken()
  const isFormData = options.body instanceof FormData
  const headers = {
    ...(options.headers || {}),
  }

  if (!isFormData && options.body) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  })

  const isJson = response.headers.get('content-type')?.includes('application/json')
  const data = isJson ? await response.json() : await response.text()

  if (!response.ok) {
    const message =
      (typeof data === 'object' && data?.detail) ||
      (typeof data === 'object' && data?.message) ||
      `Request failed with status ${response.status}`

    const error = new Error(message)
    error.status = response.status
    error.payload = data
    throw error
  }

  return data
}

export const apiClient = {
  get: (path) => request(path, { method: 'GET' }),
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
  put: (path, body) => request(path, { method: 'PUT', body: JSON.stringify(body) }),
  del: (path) => request(path, { method: 'DELETE' }),
  async stream(path, { method = 'POST', body, headers = {}, signal, onMessage }) {
    const token = getAccessToken()
    const requestHeaders = { ...headers }

    if (token) {
      requestHeaders.Authorization = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      body,
      headers: requestHeaders,
      signal,
    })

    if (!response.ok) {
      let detail = `Request failed with status ${response.status}`
      try {
        const payload = await response.json()
        detail = payload?.detail || payload?.message || detail
      } catch {
        // Keep default error detail when response body is not JSON.
      }
      throw new Error(detail)
    }

    if (!response.body) {
      throw new Error('Streaming response body is not available')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const rawLine of lines) {
        const line = rawLine.trim()
        if (!line) continue

        const payload = line.startsWith('data:') ? line.slice(5).trim() : line
        if (payload === '[DONE]') return

        try {
          const parsed = JSON.parse(payload)
          onMessage?.(parsed)
        } catch {
          onMessage?.({ delta: payload })
        }
      }
    }

    if (buffer.trim()) {
      const payload = buffer.trim().startsWith('data:') ? buffer.trim().slice(5).trim() : buffer.trim()
      if (payload && payload !== '[DONE]') {
        try {
          onMessage?.(JSON.parse(payload))
        } catch {
          onMessage?.({ delta: payload })
        }
      }
    }
  },
}
