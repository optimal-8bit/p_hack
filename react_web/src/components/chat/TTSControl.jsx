import { Volume2, VolumeX } from 'lucide-react';
import PropTypes from 'prop-types';

/**
 * TTS Control Button - Mute/Unmute toggle
 */
export default function TTSControl({ isMuted, onToggle, isSpeaking }) {
  return (
    <button
      onClick={onToggle}
      className="tts-control-btn"
      title={isMuted ? 'Enable voice responses' : 'Disable voice responses'}
      aria-label={isMuted ? 'Enable voice responses' : 'Disable voice responses'}
    >
      {isMuted ? (
        <VolumeX className="tts-icon" />
      ) : (
        <Volume2 className={`tts-icon ${isSpeaking ? 'speaking' : ''}`} />
      )}
    </button>
  );
}

TTSControl.propTypes = {
  isMuted: PropTypes.bool.isRequired,
  onToggle: PropTypes.func.isRequired,
  isSpeaking: PropTypes.bool.isRequired,
};
