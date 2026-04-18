import { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import EmergencyBubble from './EmergencyBubble'

export default function MessageBubble({ role, content, streaming, error, isCrisis, voiceAnalysis, emotionAnalysis, facialEmotion }) {
  const [displayedContent, setDisplayedContent] = useState('')

  useEffect(() => {
    // For bot messages that are streaming, show content as it arrives
    if (role === 'bot' && streaming) {
      setDisplayedContent(content)
    } else {
      // For completed messages or user messages, show full content
      setDisplayedContent(content)
    }
  }, [content, streaming, role])

  // If this is a crisis message from the bot, use EmergencyBubble
  if (role === 'bot' && isCrisis) {
    return <EmergencyBubble content={displayedContent} streaming={streaming} />
  }

  const formattedContent = displayedContent.split('\n').map((line, idx) => (
    <span key={idx}>
      {line}
      {idx < displayedContent.split('\n').length - 1 && <br />}
    </span>
  ))

  // Helper to get emotion emoji
  const getEmotionEmoji = (emotion) => {
    const emojis = {
      happy: '😊', sad: '😢', angry: '😠', fearful: '😨', 
      disgusted: '🤢', surprised: '😲', neutral: '😐',
      joy: '😊', sadness: '😢', anger: '😠', fear: '😨',
      disgust: '🤢', surprise: '😲'
    }
    return emojis[emotion?.toLowerCase()] || '😐'
  }

  return (
    <div className={`message-bubble-wrapper ${role}`}>
      <div className={`message-bubble ${role} ${error ? 'error' : ''}`}>
        {/* Show facial emotion badge for user messages */}
        {role === 'user' && facialEmotion && (
          <div className="facial-emotion-badge">
            <span className="facial-emoji">{getEmotionEmoji(facialEmotion.dominant_emotion)}</span>
            <span className="facial-text">{facialEmotion.dominant_emotion}</span>
            <span className="facial-confidence">{(facialEmotion.confidence * 100).toFixed(0)}%</span>
          </div>
        )}

        <div className="message-content">
          {formattedContent}
          {streaming && role === 'bot' && displayedContent.length > 0 && (
            <span className="cursor">|</span>
          )}
        </div>
        
        {/* Multimodal Emotion Analysis */}
        {emotionAnalysis && role === 'bot' && !streaming && (
          <div className="emotion-analysis-metadata">
            <div className="emotion-analysis-header">🧠 Emotion Analysis</div>
            <div className="emotion-analysis-grid">
              <div className="emotion-analysis-item">
                <span className="emotion-label">Text Emotion:</span>
                <span className="emotion-value">
                  {getEmotionEmoji(emotionAnalysis.textEmotion)} {emotionAnalysis.textEmotion}
                </span>
              </div>
              <div className="emotion-analysis-item">
                <span className="emotion-label">Facial Emotion:</span>
                <span className="emotion-value">
                  {getEmotionEmoji(emotionAnalysis.facialEmotion)} {emotionAnalysis.facialEmotion}
                </span>
              </div>
              <div className="emotion-analysis-item full-width">
                <span className="emotion-label">Congruence:</span>
                <span className={`emotion-value congruence-${emotionAnalysis.congruence}`}>
                  {emotionAnalysis.congruence === 'congruent' && '✓ Emotions align'}
                  {emotionAnalysis.congruence === 'incongruent' && '⚠️ Emotional incongruence detected'}
                  {emotionAnalysis.congruence === 'uncertain' && '? Uncertain'}
                </span>
              </div>
            </div>
          </div>
        )}
        
        {/* Voice Analysis Metadata */}
        {voiceAnalysis && role === 'bot' && !streaming && (
          <div className="voice-analysis-metadata">
            <div className="voice-analysis-header">🎤 Voice Analysis</div>
            <div className="voice-analysis-grid">
              <div className="voice-analysis-item">
                <span className="voice-label">Fused Emotion:</span>
                <span className="voice-value">{voiceAnalysis.fusedEmotion} ({(voiceAnalysis.fusedConfidence * 100).toFixed(0)}%)</span>
              </div>
              <div className="voice-analysis-item">
                <span className="voice-label">Text:</span>
                <span className="voice-value">{voiceAnalysis.textEmotion}</span>
              </div>
              <div className="voice-analysis-item">
                <span className="voice-label">Audio:</span>
                <span className="voice-value">{voiceAnalysis.audioEmotion}</span>
              </div>
              {voiceAnalysis.stressedWords && voiceAnalysis.stressedWords.length > 0 && (
                <div className="voice-analysis-item full-width">
                  <span className="voice-label">Emphasized:</span>
                  <span className="voice-value">{voiceAnalysis.stressedWords.join(', ')}</span>
                </div>
              )}
            </div>
            {voiceAnalysis.isIncongruent && voiceAnalysis.incongruenceNote && (
              <div className="voice-incongruence-note">
                ⚠️ {voiceAnalysis.incongruenceNote}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

MessageBubble.propTypes = {
  role: PropTypes.oneOf(['user', 'bot']).isRequired,
  content: PropTypes.string.isRequired,
  streaming: PropTypes.bool,
  error: PropTypes.bool,
  isCrisis: PropTypes.bool,
  voiceAnalysis: PropTypes.shape({
    fusedEmotion: PropTypes.string,
    fusedConfidence: PropTypes.number,
    textEmotion: PropTypes.string,
    audioEmotion: PropTypes.string,
    isIncongruent: PropTypes.bool,
    incongruenceNote: PropTypes.string,
    stressedWords: PropTypes.arrayOf(PropTypes.string),
  }),
  emotionAnalysis: PropTypes.shape({
    textEmotion: PropTypes.string,
    facialEmotion: PropTypes.string,
    congruence: PropTypes.string,
  }),
  facialEmotion: PropTypes.shape({
    dominant_emotion: PropTypes.string,
    confidence: PropTypes.number,
    all_emotions: PropTypes.object,
  }),
}

MessageBubble.defaultProps = {
  streaming: false,
  error: false,
  isCrisis: false,
  voiceAnalysis: null,
  emotionAnalysis: null,
  facialEmotion: null,
}
