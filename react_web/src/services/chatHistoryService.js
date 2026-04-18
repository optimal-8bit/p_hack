/**
 * Chat History Service
 * Manages saving and loading chat conversations from localStorage
 */

const STORAGE_KEY = 'mental_health_chat_history'
const MAX_CHATS = 50 // Maximum number of chats to store

/**
 * Get all chat sessions
 */
export function getAllChats() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return []
    
    const chats = JSON.parse(stored)
    // Sort by last updated (most recent first)
    return chats.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
  } catch (error) {
    console.error('Error loading chat history:', error)
    return []
  }
}

/**
 * Get a specific chat by session ID
 */
export function getChatBySessionId(sessionId) {
  const chats = getAllChats()
  return chats.find(chat => chat.sessionId === sessionId)
}

/**
 * Save or update a chat session
 */
export function saveChat(sessionId, messages) {
  try {
    const chats = getAllChats()
    
    // Find existing chat or create new one
    const existingIndex = chats.findIndex(chat => chat.sessionId === sessionId)
    
    // Generate title from first user message
    const firstUserMessage = messages.find(msg => msg.role === 'user')
    const title = firstUserMessage 
      ? firstUserMessage.content.slice(0, 50) + (firstUserMessage.content.length > 50 ? '...' : '')
      : 'New Chat'
    
    const chatData = {
      sessionId,
      title,
      messages,
      updatedAt: new Date().toISOString(),
      messageCount: messages.length
    }
    
    if (existingIndex >= 0) {
      // Update existing chat
      chats[existingIndex] = chatData
    } else {
      // Add new chat
      chats.unshift(chatData)
      
      // Limit number of stored chats
      if (chats.length > MAX_CHATS) {
        chats.splice(MAX_CHATS)
      }
    }
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chats))
    return chatData
  } catch (error) {
    console.error('Error saving chat:', error)
    return null
  }
}

/**
 * Delete a chat session
 */
export function deleteChat(sessionId) {
  try {
    const chats = getAllChats()
    const filtered = chats.filter(chat => chat.sessionId !== sessionId)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered))
    return true
  } catch (error) {
    console.error('Error deleting chat:', error)
    return false
  }
}

/**
 * Clear all chat history
 */
export function clearAllChats() {
  try {
    localStorage.removeItem(STORAGE_KEY)
    return true
  } catch (error) {
    console.error('Error clearing chat history:', error)
    return false
  }
}

/**
 * Get chat statistics
 */
export function getChatStats() {
  const chats = getAllChats()
  return {
    totalChats: chats.length,
    totalMessages: chats.reduce((sum, chat) => sum + chat.messageCount, 0),
    oldestChat: chats.length > 0 ? chats[chats.length - 1].updatedAt : null,
    newestChat: chats.length > 0 ? chats[0].updatedAt : null
  }
}
