import { useMemo, useRef, useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import { StopCircle } from 'lucide-react'
import { chatService } from '../services/chatService'
import { ChatBubble } from '../components/ChatBubble'
import { InputBar } from '../components/InputBar'

function createId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
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

  useEffect(() => {
    scrollToBottom()
  }, [messages])

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
    }
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
      {/* Sidebar */}
      <aside className="hidden lg:flex lg:w-80 flex-col border-r border-gray-200 bg-white/80 backdrop-blur-sm">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Conversations</h2>
          <p className="text-sm text-gray-600 leading-relaxed">
            This is template-only UI. Connect your own conversation persistence later.
          </p>
        </div>
        <div className="p-4">
          <motion.button
            type="button"
            disabled
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full py-3 px-4 bg-gray-100 text-gray-400 rounded-xl font-medium cursor-not-allowed"
          >
            + New chat
          </motion.button>
        </div>
      </aside>

      {/* Main Chat Area */}
      <section className="flex-1 flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-white/80 backdrop-blur-sm">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">AI Chat</h1>
            <p className="text-sm text-gray-600 mt-1">Streaming + files + markdown output template.</p>
          </div>
          <AnimatePresence>
            {isStreaming && (
              <motion.button
                type="button"
                onClick={handleStop}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-full font-medium shadow-lg transition-colors"
              >
                <StopCircle className="w-4 h-4" />
                Stop
              </motion.button>
            )}
          </AnimatePresence>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4" role="log" aria-live="polite">
          <AnimatePresence mode="popLayout">
            {messages.map((message) => (
              <ChatBubble
                key={message.id}
                message={message}
                isStreaming={message.streaming && !message.content}
              />
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Error Display */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="mx-4 mb-2 px-4 py-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Input Bar */}
        <InputBar
          draft={draft}
          setDraft={setDraft}
          files={files}
          onSelectFiles={onSelectFiles}
          removeFile={removeFile}
          onSubmit={handleSubmit}
          canSend={canSend}
          isStreaming={isStreaming}
        />
      </section>
    </div>
  )
}
