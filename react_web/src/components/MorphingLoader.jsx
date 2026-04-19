import { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import './MorphingLoader.css'

/**
 * MorphingLoader - Modern morphing shapes loader with smooth transitions
 * 
 * Features:
 * - Continuously transforms between shapes (circle → rounded square → blob → circle)
 * - Smooth easing with gradient color transitions
 * - Optimized with CSS transforms and opacity
 * - Respects prefers-reduced-motion
 * - Prevents flicker for fast loads (minimum visible time)
 * - Accessible with aria-busy support
 * 
 * @param {string} size - Size of the loader: 'sm' (32px), 'md' (48px), 'lg' (64px), 'xl' (80px)
 * @param {string} color - Color theme: 'blue', 'purple', 'yellow', 'gradient' (default)
 * @param {boolean} fullScreen - Whether to show as full-screen overlay
 * @param {string} message - Optional loading message to display
 */
export default function MorphingLoader({ 
  size = 'md', 
  color = 'yellow',
  fullScreen = false,
  message = ''
}) {
  const [isVisible, setIsVisible] = useState(false)
  const [shouldRender, setShouldRender] = useState(true)

  // Minimum visible time to prevent flicker (500ms)
  useEffect(() => {
    const showTimer = setTimeout(() => setIsVisible(true), 10)
    
    return () => clearTimeout(showTimer)
  }, [])

  // Size mapping
  const sizeMap = {
    sm: 32,
    md: 48,
    lg: 64,
    xl: 80
  }

  const loaderSize = sizeMap[size] || sizeMap.md

  // Color theme mapping
  const colorThemes = {
    blue: {
      from: '#3b82f6',
      via: '#60a5fa',
      to: '#93c5fd'
    },
    purple: {
      from: '#8b5cf6',
      via: '#a78bfa',
      to: '#c4b5fd'
    },
    gradient: {
      from: '#3b82f6',
      via: '#8b5cf6',
      to: '#ec4899'
    },
    yellow: {
      from: '#fbbf24',
      via: '#fcd34d',
      to: '#fde68a'
    }
  }

  const theme = colorThemes[color] || colorThemes.yellow

  const containerClass = fullScreen 
    ? 'morphing-loader-fullscreen' 
    : 'morphing-loader-container'

  if (!shouldRender) return null

  return (
    <div 
      className={`${containerClass} ${isVisible ? 'visible' : ''}`}
      role="status"
      aria-busy="true"
      aria-live="polite"
    >
      <div className="morphing-loader-content">
        <div 
          className="morphing-shape"
          style={{
            width: loaderSize,
            height: loaderSize,
            background: `linear-gradient(135deg, ${theme.from}, ${theme.via}, ${theme.to})`,
          }}
        />
        
        {message && (
          <p className="morphing-loader-message">
            {message}
          </p>
        )}
      </div>
    </div>
  )
}

MorphingLoader.propTypes = {
  size: PropTypes.oneOf(['sm', 'md', 'lg', 'xl']),
  color: PropTypes.oneOf(['blue', 'purple', 'yellow', 'gradient']),
  fullScreen: PropTypes.bool,
  message: PropTypes.string,
}

/**
 * LoadingWrapper - Wrapper component to handle loading states with minimum visible time
 * 
 * @param {boolean} loading - Whether data is loading
 * @param {ReactNode} children - Content to show when not loading
 * @param {object} loaderProps - Props to pass to MorphingLoader
 */
export function LoadingWrapper({ loading, children, loaderProps = {} }) {
  const [showLoader, setShowLoader] = useState(loading)
  const [minTimeElapsed, setMinTimeElapsed] = useState(false)

  useEffect(() => {
    if (loading) {
      setShowLoader(true)
      setMinTimeElapsed(false)
      
      // Minimum visible time of 500ms
      const timer = setTimeout(() => {
        setMinTimeElapsed(true)
      }, 500)

      return () => clearTimeout(timer)
    } else {
      // Only hide if minimum time has elapsed
      if (minTimeElapsed) {
        // Add fade-out delay
        const fadeTimer = setTimeout(() => {
          setShowLoader(false)
        }, 300)
        return () => clearTimeout(fadeTimer)
      }
    }
  }, [loading, minTimeElapsed])

  if (showLoader) {
    return <MorphingLoader {...loaderProps} />
  }

  return <>{children}</>
}

LoadingWrapper.propTypes = {
  loading: PropTypes.bool.isRequired,
  children: PropTypes.node.isRequired,
  loaderProps: PropTypes.object,
}
