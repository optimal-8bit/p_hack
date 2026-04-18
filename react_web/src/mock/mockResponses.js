/**
 * Mock Responses for Mental Health Chatbot
 * Used for testing and demo purposes when backend is unavailable
 */

export const mockResponses = {
  // Greetings
  "hello": "Hey, I am great! How can I help you today?",
  "hi": "Hello! I'm here to support you. How are you feeling?",
  "hey": "Hey there! What's on your mind today?",
  "good morning": "Good morning! Hope you have a peaceful day ahead.",
  "good afternoon": "Good afternoon! How has your day been so far?",
  "good evening": "Good evening! How are you feeling right now?",
  "good night": "Good night. Take care and rest well.",
  
  // How are you
  "how are you": "I'm doing well, thanks for asking. How are you feeling?",
  "how are you doing": "I'm here and ready to listen. More importantly, how are you doing?",
  "what's up": "I'm here for you. What's going on with you today?",
  
  // Emotional states - Sadness
  "i feel sad": "I'm sorry you're feeling that way. Do you want to talk about it?",
  "i am sad": "It's okay to feel sad. Would you like to share what's making you feel this way?",
  "i'm feeling down": "I hear you. Feeling down is tough. What's been happening?",
  "i'm depressed": "I'm really sorry you're going through this. Have you considered talking to a professional? I'm here to listen in the meantime.",
  "i feel lonely": "Loneliness can be really hard. You're not alone in feeling this way. Want to talk about it?",
  
  // Emotional states - Stress
  "i am stressed": "Try taking a deep breath. What's causing the stress?",
  "i'm stressed": "Stress can be overwhelming. Let's break it down - what's the main thing stressing you out?",
  "i'm overwhelmed": "When we're overwhelmed, it helps to take things one step at a time. What's the most pressing thing right now?",
  "too much work": "Work stress is real. Have you been able to take any breaks today?",
  
  // Emotional states - Anxiety
  "i feel anxious": "You're not alone. Let's take it one step at a time. What's making you feel anxious?",
  "i'm anxious": "Anxiety can be really challenging. Try taking a few deep breaths. What's on your mind?",
  "i'm worried": "It's natural to worry sometimes. What are you worried about?",
  "i can't sleep": "Sleep troubles often come with stress or anxiety. What's been keeping you up?",
  "panic attack": "I'm sorry you're experiencing this. Try to focus on your breathing - in for 4, hold for 4, out for 4. Are you in a safe place?",
  
  // Emotional states - Anger
  "i'm angry": "It's okay to feel angry. What happened that made you feel this way?",
  "i'm frustrated": "Frustration is a valid feeling. What's frustrating you right now?",
  "i'm mad": "I hear you. What's making you mad?",
  
  // Emotional states - Positive
  "i'm happy": "That's wonderful! I'm so glad to hear that. What's making you happy?",
  "i feel good": "That's great! It's nice to hear you're feeling good. What's going well?",
  "i'm excited": "How exciting! What are you excited about?",
  "i'm grateful": "Gratitude is powerful. What are you grateful for today?",
  
  // Coping mechanisms
  "help me": "I'm here to help. Can you tell me more about what you're going through?",
  "what should i do": "Let's think through this together. Can you tell me more about the situation?",
  "i need advice": "I'm here to listen and support you. What's going on?",
  "how do i cope": "Coping strategies vary for everyone. Some find deep breathing helpful, others prefer journaling or talking. What usually helps you feel better?",
  "breathing exercises": "Great choice! Try this: Breathe in slowly for 4 counts, hold for 4, breathe out for 4, hold for 4. Repeat 4 times. How do you feel?",
  
  // Self-care
  "self care": "Self-care is so important! It can be as simple as taking a walk, listening to music, or doing something you enjoy. What makes you feel good?",
  "i need a break": "Taking breaks is essential. Even 5 minutes can help. What would help you relax right now?",
  "meditation": "Meditation can be very calming. Have you tried guided meditation apps? Even 5 minutes can make a difference.",
  
  // Relationships
  "relationship problems": "Relationship issues can be really stressful. Do you want to talk about what's happening?",
  "family issues": "Family dynamics can be complex. What's been going on with your family?",
  "friend problems": "Friendships matter. What's happening with your friend?",
  
  // Professional help
  "therapy": "Therapy can be incredibly helpful. Have you considered reaching out to a mental health professional?",
  "therapist": "A therapist can provide professional support. Would you like some resources for finding one?",
  "counseling": "Counseling is a great step. Many people find it very beneficial. Are you thinking about starting?",
  "medication": "Medication can be helpful for some people. Have you talked to a doctor about this?",
  
  // Crisis
  "suicide": "I'm really concerned about you. Please reach out to a crisis helpline immediately: National Suicide Prevention Lifeline: 988 or 1-800-273-8255. You matter, and help is available.",
  "kill myself": "Please don't hurt yourself. You matter. Call 988 or 1-800-273-8255 right now. I'm worried about you.",
  "end it all": "I'm very concerned. Please call 988 or text 'HELLO' to 741741 immediately. You deserve support and help is available.",
  "self harm": "I'm worried about you. Please reach out to a crisis counselor: Text 'HELLO' to 741741. You don't have to go through this alone.",
  
  // Gratitude
  "thank you": "You're welcome. I'm always here for you.",
  "thanks": "You're very welcome. Take care of yourself.",
  "appreciate it": "I'm glad I could help. Remember, I'm here whenever you need to talk.",
  
  // About the bot
  "who are you": "I'm your mental wellness assistant, here to support you and listen without judgment.",
  "what are you": "I'm an AI assistant designed to provide mental health support and a listening ear.",
  "can you help me": "Yes, I'm here to listen and support you. While I'm not a replacement for professional help, I can be here for you. What's going on?",
  "are you real": "I'm an AI assistant, but my support for you is real. I'm here to listen and help however I can.",
  
  // Goodbye
  "goodbye": "Take care of yourself. Remember, I'm here whenever you need to talk.",
  "bye": "Goodbye! Be kind to yourself today.",
  "see you": "See you later. Take care!",
  "talk later": "Sounds good. I'll be here whenever you need me.",
}

/**
 * Get a mock response for a given user input
 * @param {string} userInput - The user's message
 * @returns {string} - The mock response
 */
export function getMockResponse(userInput) {
  const normalizedInput = userInput.toLowerCase().trim()
  
  // Direct match
  if (mockResponses[normalizedInput]) {
    return mockResponses[normalizedInput]
  }
  
  // Partial match - check if any key is contained in the input
  for (const [key, response] of Object.entries(mockResponses)) {
    if (normalizedInput.includes(key)) {
      return response
    }
  }
  
  // Default responses for unmatched queries
  const defaultResponses = [
    "I'm here to listen. Tell me more about what you're feeling.",
    "I hear you. Can you tell me more about that?",
    "That sounds important. Would you like to talk more about it?",
    "I'm listening. What else is on your mind?",
    "Thank you for sharing that with me. How does that make you feel?",
    "I understand. What would help you feel better right now?",
  ]
  
  // Return a random default response
  return defaultResponses[Math.floor(Math.random() * defaultResponses.length)]
}

/**
 * Simulate streaming by yielding characters one at a time
 * @param {string} text - The full text to stream
 * @param {function} onToken - Callback for each character
 * @param {number} delay - Delay between characters in ms
 * @param {number} initialDelay - Delay before starting streaming in ms
 * @returns {Promise} - Resolves when streaming is complete
 */
export async function simulateStreaming(text, onToken, delay = 20, initialDelay = 300) {
  // Initial delay before starting to type (simulates "thinking")
  if (initialDelay > 0) {
    await new Promise(resolve => setTimeout(resolve, initialDelay))
  }

  // Stream character by character
  for (let i = 0; i < text.length; i++) {
    await new Promise(resolve => setTimeout(resolve, delay))
    onToken(text[i])
  }
}

// Configuration flag
export const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || false
