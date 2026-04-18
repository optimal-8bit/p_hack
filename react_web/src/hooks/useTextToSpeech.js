import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Custom hook for Text-to-Speech using Web Speech API
 * Provides calm, empathetic voice output for mental health chatbot
 */
export function useTextToSpeech() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [voices, setVoices] = useState([]);
  const [isSupported, setIsSupported] = useState(false);
  const utteranceRef = useRef(null);

  // Check if speech synthesis is supported
  useEffect(() => {
    if ('speechSynthesis' in window) {
      setIsSupported(true);
      
      // Load available voices
      const loadVoices = () => {
        const availableVoices = window.speechSynthesis.getVoices();
        console.log('📢 [TTS] Available voices:', availableVoices.length);
        if (availableVoices.length > 0) {
          setVoices(availableVoices);
          console.log('🎤 [TTS] First few voices:', availableVoices.slice(0, 3).map(v => `${v.name} (${v.lang})`));
        }
      };

      // Load voices immediately
      loadVoices();

      // Some browsers load voices asynchronously - wait for them
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = () => {
          console.log('🔄 [TTS] Voices changed event fired');
          loadVoices();
        };
      }

      // Fallback: Try loading voices after a delay
      setTimeout(() => {
        if (voices.length === 0) {
          console.log('⏰ [TTS] Trying to load voices after delay...');
          loadVoices();
        }
      }, 1000);

    } else {
      console.warn('⚠️ [TTS] Speech synthesis not supported in this browser');
      setIsSupported(false);
    }

    // Cleanup
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  /**
   * Get the best voice for a given language
   * Prefers local, natural-sounding voices
   */
  const getVoiceForLanguage = useCallback((language = 'en') => {
    if (voices.length === 0) return null;

    // Language code mapping
    const langMap = {
      'en': 'en-US',
      'hi': 'hi-IN',
      'fr': 'fr-FR',
      'es': 'es-ES'
    };

    const targetLang = langMap[language] || language;

    // Priority 1: Local service voices for the target language
    let voice = voices.find(v => 
      v.lang.startsWith(targetLang.split('-')[0]) && 
      v.localService
    );

    // Priority 2: Any voice for the target language
    if (!voice) {
      voice = voices.find(v => 
        v.lang.startsWith(targetLang.split('-')[0])
      );
    }

    // Priority 3: Default English voice
    if (!voice) {
      voice = voices.find(v => v.lang.startsWith('en'));
    }

    // Fallback: First available voice
    if (!voice) {
      voice = voices[0];
    }

    console.log('🎤 [TTS] Selected voice:', voice?.name, voice?.lang);
    return voice;
  }, [voices]);

  /**
   * Cancel any ongoing speech
   */
  const cancelSpeech = useCallback(() => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      utteranceRef.current = null;
    }
  }, []);

  /**
   * Speak the given text
   * @param {string} text - Text to speak
   * @param {string} language - Language code (en, hi, fr, es)
   */
  const speak = useCallback((text, language = 'en') => {
    if (!isSupported || isMuted || !text) {
      console.log('🔇 [TTS] Speech skipped:', { isSupported, isMuted, hasText: !!text });
      return;
    }

    // Cancel any ongoing speech
    cancelSpeech();

    // Create new utterance
    const utterance = new SpeechSynthesisUtterance(text);
    utteranceRef.current = utterance;

    // Get appropriate voice (if available)
    const voice = getVoiceForLanguage(language);
    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang;
      console.log('🎤 [TTS] Using voice:', voice.name, voice.lang);
    } else {
      // Fallback to language code even without specific voice
      const langCode = language === 'hi' ? 'hi-IN' : 
                       language === 'fr' ? 'fr-FR' : 
                       language === 'es' ? 'es-ES' : 'en-US';
      utterance.lang = langCode;
      console.log('🎤 [TTS] Using fallback language:', langCode);
    }

    // Speech settings for calm, empathetic delivery
    utterance.rate = 0.9;  // Slightly slower for calmness
    utterance.pitch = 1.0; // Normal pitch
    utterance.volume = 1.0; // Full volume

    // Event handlers
    utterance.onstart = () => {
      console.log('🗣️ [TTS] Started speaking');
      setIsSpeaking(true);
    };

    utterance.onend = () => {
      console.log('✅ [TTS] Finished speaking');
      setIsSpeaking(false);
      utteranceRef.current = null;
    };

    utterance.onerror = (event) => {
      console.error('❌ [TTS] Speech error:', event.error);
      setIsSpeaking(false);
      utteranceRef.current = null;
    };

    // Speak
    try {
      window.speechSynthesis.speak(utterance);
      console.log('📢 [TTS] Speaking:', text.substring(0, 50) + '...');
    } catch (error) {
      console.error('❌ [TTS] Failed to speak:', error);
      setIsSpeaking(false);
    }
  }, [isSupported, isMuted, cancelSpeech, getVoiceForLanguage]);

  /**
   * Toggle mute/unmute
   */
  const toggleMute = useCallback(() => {
    setIsMuted(prev => {
      const newMuted = !prev;
      console.log('🔊 [TTS] Mute toggled:', newMuted);
      
      // Cancel speech if muting
      if (newMuted) {
        cancelSpeech();
      }
      
      return newMuted;
    });
  }, [cancelSpeech]);

  /**
   * Pause current speech
   */
  const pause = useCallback(() => {
    if (window.speechSynthesis && isSpeaking) {
      window.speechSynthesis.pause();
      console.log('⏸️ [TTS] Paused');
    }
  }, [isSpeaking]);

  /**
   * Resume paused speech
   */
  const resume = useCallback(() => {
    if (window.speechSynthesis && isSpeaking) {
      window.speechSynthesis.resume();
      console.log('▶️ [TTS] Resumed');
    }
  }, [isSpeaking]);

  return {
    speak,
    cancelSpeech,
    toggleMute,
    pause,
    resume,
    isSpeaking,
    isMuted,
    isSupported,
    voices
  };
}
