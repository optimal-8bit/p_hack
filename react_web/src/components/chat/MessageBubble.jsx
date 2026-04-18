import { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import EmergencyBubble from './EmergencyBubble'

export default function MessageBubble({ role, content, streaming, error, isCrisis, voiceAnalysis }) {
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

  return (
    <div className={`message-bubble-wrapper ${role}`}>
      <div className={`message-bubble ${role} ${error ? 'error' : ''}`}>
        <div className="message-content">
          {formattedContent}
          {streaming && role === 'bot' && displayedContent.length > 0 && (
            <span className="cursor">|</span>
          )}
        </div>
        
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
}

MessageBubble.defaultProps = {
  streaming: false,
  error: false,
  isCrisis: false,
  voiceAnalysis: null,
}
