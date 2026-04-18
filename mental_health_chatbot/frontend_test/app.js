// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State
let sessionId = generateUUID();
let isProcessing = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('sessionId').textContent = sessionId;
    
    // Event listeners
    document.getElementById('sendButton').addEventListener('click', sendMessage);
    document.getElementById('messageInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isProcessing) {
            sendMessage();
        }
    });
    document.getElementById('clearButton').addEventListener('click', clearSession);
    document.getElementById('refreshHealthButton').addEventListener('click', loadHealthStatus);
    
    // Load initial health status
    loadHealthStatus();
    
    // Auto-refresh health every 10 seconds
    setInterval(loadHealthStatus, 10000);
});

// Generate UUID for session
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Send message
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isProcessing) return;
    
    // Clear input
    input.value = '';
    isProcessing = true;
    updateSendButton(true);
    
    // Add user message to chat
    addMessage('user', message);
    
    // Show loading indicator
    const loadingId = addMessage('bot', '<div class="loading"></div>', false);
    
    try {
        // Send to API
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading indicator
        removeMessage(loadingId);
        
        // Add bot response
        addBotResponse(data);
        
    } catch (error) {
        console.error('Error sending message:', error);
        removeMessage(loadingId);
        addMessage('bot', `Error: ${error.message}. Please check if the backend server is running.`, false);
    } finally {
        isProcessing = false;
        updateSendButton(false);
        input.focus();
    }
}

// Add message to chat
function addMessage(type, content, includeMetadata = true) {
    const chatWindow = document.getElementById('chatWindow');
    const messageId = `msg-${Date.now()}-${Math.random()}`;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.id = messageId;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = content;
    
    messageDiv.appendChild(contentDiv);
    chatWindow.appendChild(messageDiv);
    
    // Scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
    
    return messageId;
}

// Add bot response with metadata
function addBotResponse(data) {
    const chatWindow = document.getElementById('chatWindow');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message bot ${data.is_crisis ? 'crisis' : ''}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Add crisis badge if applicable
    if (data.is_crisis) {
        const badge = document.createElement('div');
        badge.className = 'crisis-badge';
        badge.textContent = '🆘 Crisis Response';
        contentDiv.appendChild(badge);
    }
    
    // Add response text
    const textDiv = document.createElement('div');
    textDiv.textContent = data.response_text;
    contentDiv.appendChild(textDiv);
    
    // Add metadata
    const metadataDiv = document.createElement('div');
    metadataDiv.className = 'metadata';
    
    const emotion = `${data.emotion.emotion} ${(data.emotion.confidence * 100).toFixed(0)}%`;
    const intent = data.intent.intent;
    const lang = data.detected_language;
    const time = `${data.processing_time_ms.toFixed(0)}ms`;
    
    metadataDiv.textContent = `[emotion: ${emotion}] [intent: ${intent}] [lang: ${lang}] [${time}]`;
    contentDiv.appendChild(metadataDiv);
    
    messageDiv.appendChild(contentDiv);
    chatWindow.appendChild(messageDiv);
    
    // Scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Remove message
function removeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.remove();
    }
}

// Update send button state
function updateSendButton(disabled) {
    const button = document.getElementById('sendButton');
    button.disabled = disabled;
    button.textContent = disabled ? 'Sending...' : 'Send';
}

// Load health status
async function loadHealthStatus() {
    const healthDiv = document.getElementById('healthStatus');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        
        if (!response.ok) {
            throw new Error('Health check failed');
        }
        
        const data = await response.json();
        
        // Build health display
        let html = `
            <div class="health-item">
                <span>Status:</span>
                <span>
                    <span class="status-indicator ${data.status === 'healthy' ? 'healthy' : 'unhealthy'}"></span>
                    ${data.status.toUpperCase()}
                </span>
            </div>
            <div class="health-item">
                <span>Version:</span>
                <span>${data.version}</span>
            </div>
            <hr style="margin: 10px 0; border-color: #333;">
        `;
        
        // Add model statuses
        for (const [model, loaded] of Object.entries(data.models_loaded)) {
            html += `
                <div class="health-item">
                    <span>${model}:</span>
                    <span>
                        <span class="status-indicator ${loaded ? 'healthy' : 'unhealthy'}"></span>
                        ${loaded ? 'Loaded' : 'Not loaded'}
                    </span>
                </div>
            `;
        }
        
        healthDiv.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading health status:', error);
        healthDiv.innerHTML = `
            <div class="health-item">
                <span>Status:</span>
                <span>
                    <span class="status-indicator unhealthy"></span>
                    ERROR
                </span>
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #e74c3c;">
                Cannot connect to backend server. Please ensure it's running at ${API_BASE_URL}
            </div>
        `;
    }
}

// Clear session
async function clearSession() {
    if (!confirm('Clear this session? This will reset the conversation context.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to clear session');
        }
        
        // Clear chat window
        const chatWindow = document.getElementById('chatWindow');
        chatWindow.innerHTML = `
            <div class="message bot">
                <div class="message-content">
                    Session cleared. How can I support you today?
                </div>
            </div>
        `;
        
        // Generate new session ID
        sessionId = generateUUID();
        document.getElementById('sessionId').textContent = sessionId;
        
    } catch (error) {
        console.error('Error clearing session:', error);
        alert('Failed to clear session: ' + error.message);
    }
}
