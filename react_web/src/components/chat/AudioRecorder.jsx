import { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { Square, Send } from 'lucide-react'

export default function AudioRecorder({ onSendAudio, onCancel }) {
  const [audioTime, setAudioTime] = useState(0)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const streamRef = useRef(null)

  useEffect(() => {
    startRecording()

    // Timer
    const interval = setInterval(() => {
      setAudioTime((prev) => prev + 1)
    }, 1000)

    return () => {
      clearInterval(interval)
      stopRecording()
    }
  }, [])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream

      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.start()
    } catch (error) {
      console.error('Error accessing microphone:', error)
      alert('Could not access microphone. Please check permissions.')
      onCancel()
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop()
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
    }
  }

  const handleStop = () => {
    stopRecording()
    onCancel()
  }

  const handleSend = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        onSendAudio(audioBlob, audioTime)
      }
      stopRecording()
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="flex items-center gap-3 bg-[#202123] px-4 py-3 rounded-lg border border-gray-700 w-full">
      {/* Recording indicator */}
      <span className="flex items-center gap-2">
        <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
        <span className="text-sm text-gray-300">Recording</span>
      </span>

      {/* Timer */}
      <span className="text-sm text-gray-400 font-mono">{formatTime(audioTime)}</span>

      {/* Spacer */}
      <div className="flex-1"></div>

      {/* Stop button */}
      <button
        onClick={handleStop}
        className="p-2 text-gray-400 hover:text-gray-200 hover:bg-[#2a2b32] rounded-lg transition-colors"
        aria-label="Stop recording"
      >
        <Square size={20} />
      </button>

      {/* Send button */}
      <button
        onClick={handleSend}
        className="p-2 bg-white text-black hover:bg-gray-200 rounded-lg transition-colors"
        aria-label="Send audio"
      >
        <Send size={20} />
      </button>
    </div>
  )
}

AudioRecorder.propTypes = {
  onSendAudio: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
}
