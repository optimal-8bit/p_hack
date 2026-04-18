import { useEffect, useRef, useState } from 'react'
import PropTypes from 'prop-types'
import './VideoBackground.css'

export default function VideoBackground({ videoSrc, isActive }) {
  const videoRef = useRef(null)
  const [isLoaded, setIsLoaded] = useState(false)
  const [hasError, setHasError] = useState(false)

  useEffect(() => {
    if (!videoSrc || !videoRef.current) return

    const video = videoRef.current

    const handleLoadedData = () => {
      setIsLoaded(true)
      setHasError(false)
      if (isActive) {
        video.play().catch(err => {
          console.warn('Video autoplay failed:', err)
        })
      }
    }

    const handleError = () => {
      console.warn('Video failed to load:', videoSrc)
      setHasError(true)
      setIsLoaded(false)
    }

    video.addEventListener('loadeddata', handleLoadedData)
    video.addEventListener('error', handleError)

    return () => {
      video.removeEventListener('loadeddata', handleLoadedData)
      video.removeEventListener('error', handleError)
    }
  }, [videoSrc, isActive])

  useEffect(() => {
    if (!videoRef.current || !isLoaded) return

    const video = videoRef.current

    if (isActive) {
      video.play().catch(err => {
        console.warn('Video play failed:', err)
      })
    } else {
      video.pause()
    }
  }, [isActive, isLoaded])

  if (!videoSrc || hasError) {
    return null
  }

  return (
    <div className={`video-background-container ${isActive ? 'active' : ''}`}>
      <video
        ref={videoRef}
        className="video-background"
        autoPlay
        loop
        muted
        playsInline
        preload="auto"
      >
        <source src={videoSrc} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  )
}

VideoBackground.propTypes = {
  videoSrc: PropTypes.string,
  isActive: PropTypes.bool.isRequired,
}

VideoBackground.defaultProps = {
  videoSrc: null,
}
