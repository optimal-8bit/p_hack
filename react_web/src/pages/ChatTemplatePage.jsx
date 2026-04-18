import { useMemo, useRef, useState } from 'react'

import { chatService } from '../services/chatService'
import './ChatTemplatePage.css'

function createId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

function formatFileSize(size) {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / (1024 * 1024)).toFixed(1)} MB`
}

function escapeHtml(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

function inlineMarkdown(text) {
  let output = escapeHtml(text)
  output = output.replace(/`([^`]+)`/g, '<code>$1</code>')
  output = output.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  output = output.replace(/\*([^*]+)\*/g, '<em>$1</em>')
  output = output.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>')
  return output
}

function markdownToHtml(markdownText) {
  const lines = markdownText.split('\n')
  const blocks = []
  let inCodeBlock = false
  let codeBuffer = []
  let listType = null

  const closeList = () => {
    if (!listType) return
    blocks.push(`</${listType}>`)
    listType = null
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd()

    if (line.startsWith('```')) {
      if (inCodeBlock) {
        blocks.push(`<pre><code>${escapeHtml(codeBuffer.join('\n'))}</code></pre>`)
        codeBuffer = []
        inCodeBlock = false
      } else {
        closeList()
        inCodeBlock = true
      }
      continue
    }

    if (inCodeBlock) {
      codeBuffer.push(rawLine)
      continue
    }

    if (!line) {
      closeList()
      continue
    }

    const headingMatch = line.match(/^(#{1,6})\s+(.*)$/)
    if (headingMatch) {
      closeList()
      const level = headingMatch[1].length
      blocks.push(`<h${level}>${inlineMarkdown(headingMatch[2])}</h${level}>`)
      continue
    }

    const unorderedMatch = line.match(/^[-*]\s+(.*)$/)
    if (unorderedMatch) {
      if (listType !== 'ul') {
        closeList()
        listType = 'ul'
        blocks.push('<ul>')
      }
      blocks.push(`<li>${inlineMarkdown(unorderedMatch[1])}</li>`)
      continue
    }

    const orderedMatch = line.match(/^\d+\.\s+(.*)$/)
    if (orderedMatch) {
      if (listType !== 'ol') {
        closeList()
        listType = 'ol'
        blocks.push('<ol>')
      }
      blocks.push(`<li>${inlineMarkdown(orderedMatch[1])}</li>`)
      continue
    }

    closeList()
    blocks.push(`<p>${inlineMarkdown(line)}</p>`)
  }

  if (inCodeBlock) {
    blocks.push(`<pre><code>${escapeHtml(codeBuffer.join('\n'))}</code></pre>`)
  }
  closeList()

  return blocks.join('')
}

function MarkdownView({ content }) {
  return <div className="markdown-body" dangerouslySetInnerHTML={{ __html: markdownToHtml(content || '...') }} />
}

export default function ChatTemplatePage() {
  const [messages, setMessages] = useState([
    {
      id: createId(),
      role: 'assistant',
      content:
        '## Chat Template Ready\n\nThis interface supports:\n- markdown rendering\n- streaming output\n- file attachment\n\nPlug this page into any route when ready.',
      createdAt: new Date().toISOString(),
    },
  ])
  const [draft, setDraft] = useState('')
  const [files, setFiles] = useState([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState('')

  const messagesEndRef = useRef(null)
  const abortRef = useRef(null)

  const canSend = useMemo(() => {
    return !isStreaming && (draft.trim().length > 0 || files.length > 0)
  }, [draft, files.length, isStreaming])

  const scrollToBottom = () => {
    requestAnimationFrame(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
    })
  }

  const onSelectFiles = (event) => {
    const selected = Array.from(event.target.files || [])
    if (!selected.length) return

    setFiles((prev) => [...prev, ...selected])
    event.target.value = ''
  }

  const removeFile = (targetName) => {
    setFiles((prev) => prev.filter((file) => file.name !== targetName))
  }

  const handleStop = () => {
    abortRef.current?.abort()
    abortRef.current = null
    setIsStreaming(false)
  }

  const appendAssistantToken = (assistantId, token) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === assistantId ? { ...msg, content: `${msg.content}${token}` } : msg)),
    )
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    const userText = draft.trim()
    if (!userText && files.length === 0) {
      return
    }

    setError('')
    setDraft('')

    const attachedFiles = files
    setFiles([])

    const userMessage = {
      id: createId(),
      role: 'user',
      content: userText || 'Uploaded files only',
      files: attachedFiles.map((file) => ({ name: file.name, size: file.size, type: file.type })),
      createdAt: new Date().toISOString(),
    }

    const assistantMessage = {
      id: createId(),
      role: 'assistant',
      content: '',
      createdAt: new Date().toISOString(),
      streaming: true,
    }

    setMessages((prev) => [...prev, userMessage, assistantMessage])
    setIsStreaming(true)
    scrollToBottom()

    const signalController = new AbortController()
    abortRef.current = signalController

    const payloadMessages = [
      ...messages.map((msg) => ({ role: msg.role, content: msg.content })),
      { role: 'user', content: userMessage.content },
    ]

    try {
      await chatService.streamReply({
        messages: payloadMessages,
        files: attachedFiles,
        signal: signalController.signal,
        onToken: (token) => {
          appendAssistantToken(assistantMessage.id, token)
          scrollToBottom()
        },
        onDone: () => {
          setMessages((prev) =>
            prev.map((msg) => (msg.id === assistantMessage.id ? { ...msg, streaming: false } : msg)),
          )
        },
      })
    } catch (streamError) {
      if (signalController.signal.aborted) {
        appendAssistantToken(assistantMessage.id, '\n\n_Stopped by user._')
      } else {
        setError(streamError.message || 'Streaming failed')
        appendAssistantToken(assistantMessage.id, '\n\n_Error while streaming response._')
      }
    } finally {
      abortRef.current = null
      setIsStreaming(false)
      setMessages((prev) => prev.map((msg) => ({ ...msg, streaming: false })))
      scrollToBottom()
    }
  }

  return (
    <div className="chat-template-shell">
      <aside className="chat-sidebar">
        <h2>Conversations</h2>
        <p>This is template-only UI. Connect your own conversation persistence later.</p>
        <button type="button" disabled>
          + New chat
        </button>
      </aside>

      <section className="chat-main">
        <header className="chat-header">
          <div>
            <h1>AI Chat</h1>
            <p>Streaming + files + markdown output template.</p>
          </div>
          {isStreaming ? (
            <button type="button" className="stop-btn" onClick={handleStop}>
              Stop generation
            </button>
          ) : null}
        </header>

        <div className="chat-log" role="log" aria-live="polite">
          {messages.map((message) => (
            <article key={message.id} className={`chat-bubble ${message.role}`}>
              <header>
                <span className="role">{message.role === 'assistant' ? 'Assistant' : 'You'}</span>
              </header>

              <MarkdownView content={message.content} />

              {message.files?.length ? (
                <ul className="message-file-list">
                  {message.files.map((file) => (
                    <li key={`${message.id}-${file.name}`}>
                      <span>{file.name}</span>
                      <small>{formatFileSize(file.size)}</small>
                    </li>
                  ))}
                </ul>
              ) : null}
            </article>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <footer className="chat-compose-area">
          {files.length ? (
            <ul className="pending-files">
              {files.map((file) => (
                <li key={file.name}>
                  <div>
                    <strong>{file.name}</strong>
                    <small>{formatFileSize(file.size)}</small>
                  </div>
                  <button type="button" onClick={() => removeFile(file.name)}>
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          ) : null}

          <form onSubmit={handleSubmit} className="chat-compose-form">
            <label htmlFor="chat-file" className="file-input-btn">
              Attach files
            </label>
            <input
              id="chat-file"
              type="file"
              multiple
              className="file-input"
              onChange={onSelectFiles}
            />

            <textarea
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="Message the assistant..."
              rows={1}
            />

            <button type="submit" disabled={!canSend}>
              {isStreaming ? 'Streaming...' : 'Send'}
            </button>
          </form>

          {error ? <p className="stream-error">{error}</p> : null}
        </footer>
      </section>
    </div>
  )
}
