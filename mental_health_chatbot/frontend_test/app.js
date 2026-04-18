// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State
let sessionId = generateUUID();
let isProcessing = false;
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('sessionId').textContent = sessionId;
    
    // Event listeners
    document.getElementById('sendButton').addEventListener('click', sendMessage);
    document.getElementById('micButton').addEventListener('click', toggleRecording);
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


// Voice recording functions
async function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        await startRecording();
    }
}

async function startRecording() {
    try {
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Create media recorder
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
            
            // Create audio blob
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            
            // Send to voice API
            await sendVoiceMessage(audioBlob);
        };
        
        // Start recording
        mediaRecorder.start();
        isRecording = true;
        
        // Update UI
        const micButton = document.getElementById('micButton');
        micButton.classList.add('recording');
        micButton.textContent = '⏹️';
        micButton.title = 'Stop recording';
        
        const voiceIndicator = document.getElementById('voiceIndicator');
        const voiceStatus = document.getElementById('voiceStatus');
        voiceIndicator.classList.add('active');
        voiceStatus.textContent = 'Recording... Click stop when done';
        
    } catch (error) {
        console.error('Error starting recording:', error);
        alert('Could not access microphone. Please ensure microphone permissions are granted.');
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        // Update UI
        const micButton = document.getElementById('micButton');
        micButton.classList.remove('recording');
        micButton.textContent = '🎤';
        micButton.title = 'Record voice message';
        
        const voiceIndicator = document.getElementById('voiceIndicator');
        const voiceStatus = document.getElementById('voiceStatus');
        voiceStatus.textContent = 'Processing audio...';
    }
}

async function sendVoiceMessage(audioBlob) {
    isProcessing = true;
    updateSendButton(true);
    
    // Show loading indicator
    const loadingId = addMessage('bot', '<div class="loading"></div> Processing your voice message...', false);
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('session_id', sessionId);
        formData.append('audio', audioBlob, 'recording.webm');
        
        // Send to voice API
        const response = await fetch(`${API_BASE_URL}/api/voice/chat`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading indicator
        removeMessage(loadingId);
        
        // Hide voice indicator
        const voiceIndicator = document.getElementById('voiceIndicator');
        voiceIndicator.classList.remove('active');
        
        // Add transcript as user message
        if (data.transcript) {
            addMessage('user', `🎤 ${data.transcript}`);
        }
        
        // Add bot response with voice metadata
        addVoiceResponse(data);
        
    } catch (error) {
        console.error('Error sending voice message:', error);
        removeMessage(loadingId);
        
        // Hide voice indicator
        const voiceIndicator = document.getElementById('voiceIndicator');
        voiceIndicator.classList.remove('active');
        
        addMessage('bot', `Error processing voice: ${error.message}. Please try again or type your message.`, false);
    } finally {
        isProcessing = false;
        updateSendButton(false);
    }
}

function addVoiceResponse(data) {
    const chatWindow = document.getElementById('chatWindow');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Add response text from chat_result
    const textDiv = document.createElement('div');
    if (data.chat_result && data.chat_result.response_text) {
        textDiv.textContent = data.chat_result.response_text;
    } else {
        textDiv.textContent = 'I heard you. Let me process that...';
    }
    contentDiv.appendChild(textDiv);
    
    // Add voice metadata
    const metadataDiv = document.createElement('div');
    metadataDiv.className = 'metadata';
    
    const emotion = `${data.fused_emotion} ${(data.fused_confidence * 100).toFixed(0)}%`;
    const textEmotion = `text: ${data.text_only_emotion} ${(data.text_only_confidence * 100).toFixed(0)}%`;
    const audioEmotion = `audio: ${data.audio_focused_emotion} ${(data.audio_focused_confidence * 100).toFixed(0)}%`;
    const duration = `${data.audio_duration_seconds.toFixed(1)}s`;
    const time = `${(data.transcription_time_ms + data.fusion_time_ms).toFixed(0)}ms`;
    
    metadataDiv.innerHTML = `
        [🎤 voice] [emotion: ${emotion}] [${textEmotion}] [${audioEmotion}]<br>
        [duration: ${duration}] [processing: ${time}]
    `;
    
    // Add incongruence note if present
    if (data.is_incongruent && data.incongruence_note) {
        const incongruenceDiv = document.createElement('div');
        incongruenceDiv.style.cssText = 'margin-top: 10px; padding: 8px; background: rgba(231, 76, 60, 0.2); border-radius: 4px; font-size: 12px;';
        incongruenceDiv.innerHTML = `<strong>⚠️ Note:</strong> ${data.incongruence_note}`;
        contentDiv.appendChild(incongruenceDiv);
    }
    
    // Add stressed words if present
    if (data.stressed_words && data.stressed_words.length > 0) {
        const stressedDiv = document.createElement('div');
        stressedDiv.style.cssText = 'margin-top: 8px; font-size: 11px; color: #aaa;';
        stressedDiv.textContent = `Emphasized words: ${data.stressed_words.join(', ')}`;
        metadataDiv.appendChild(stressedDiv);
    }
    
    contentDiv.appendChild(metadataDiv);
    messageDiv.appendChild(contentDiv);
    chatWindow.appendChild(messageDiv);
    
    // Scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
