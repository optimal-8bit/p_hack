import { motion } from 'motion/react'
import PropTypes from 'prop-types'

/**
 * LoadingIndicator - Wave dots animation with gradient colors
 * 
 * Features:
 * - Multiple dots forming a wave motion (sine wave)
 * - Smooth easing with ease-in-out
 * - Gradient color transition across dots
 * - Dynamic and premium feel
 * - Seamless infinite loop
 * 
 * @param {string} variant - 'light' or 'dark' theme
 */
export function LoadingIndicator({ variant = 'light' }) {
  const dots = 7 // Number of dots for wave effect
  
  // Gradient colors for dots (blue to purple gradient)
  const gradientColors = [
    '#3B82F6', // blue-500
    '#60A5FA', // blue-400
    '#818CF8', // indigo-400
    '#A78BFA', // violet-400
    '#C084FC', // purple-400
    '#E879F9', // fuchsia-400
    '#F472B6', // pink-400
  ]

  return (
    <div className="flex items-center gap-1.5 py-3" role="status" aria-label="Loading">
      {Array.from({ length: dots }).map((_, i) => (
        <motion.div
          key={i}
          className="w-2.5 h-2.5 rounded-full"
          style={{
            backgroundColor: gradientColors[i % gradientColors.length],
          }}
          animate={{
            y: [0, -12, 0],
            scale: [1, 1.2, 1],
            opacity: [0.6, 1, 0.6],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: i * 0.1, // Stagger for wave effect
          }}
        />
      ))}
    </div>
  )
}

LoadingIndicator.propTypes = {
  variant: PropTypes.oneOf(['light', 'dark']),
}

/**
 * Alternative: Pulsing Wave with Glow
 * Enhanced version with glow effects
 */
export function PulsingWaveLoader() {
  const dots = 7
  const colors = ['#3B82F6', '#60A5FA', '#818CF8', '#A78BFA', '#C084FC', '#E879F9', '#F472B6']

  return (
    <div className="flex items-center gap-2 py-3">
      {Array.from({ length: dots }).map((_, i) => (
        <motion.div
          key={i}
          className="w-3 h-3 rounded-full"
          style={{
            backgroundColor: colors[i],
            boxShadow: `0 0 12px ${colors[i]}80`,
          }}
          animate={{
            scale: [1, 1.5, 1],
            opacity: [0.5, 1, 0.5],
          }}
          transition={{
            duration: 1.8,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: i * 0.12,
          }}
        />
      ))}
    </div>
  )
}

/**
 * Alternative: Smooth Sine Wave
 * Dots follow a smooth sine wave pattern
 */
export function SineWaveLoader() {
  const dots = 9
  const baseColor = '#3B82F6'

  return (
    <div className="flex items-center gap-1 py-4">
      {Array.from({ length: dots }).map((_, i) => {
        const phase = (i / dots) * Math.PI * 2
        return (
          <motion.div
            key={i}
            className="w-2 h-2 rounded-full"
            style={{
              background: `linear-gradient(135deg, #3B82F6, #8B5CF6)`,
            }}
            animate={{
              y: [
                Math.sin(phase) * 10,
                Math.sin(phase + Math.PI) * 10,
                Math.sin(phase) * 10,
              ],
              opacity: [0.4, 1, 0.4],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'easeInOut',
              delay: i * 0.08,
            }}
          />
        )
      })}
    </div>
  )
}

/**
 * Alternative: Gradient Shimmer Effect
 * Uncomment to use this instead of bouncing dots
 */
export function ShimmerLoader() {
  return (
    <div className="relative h-4 w-32 overflow-hidden rounded-lg bg-gray-200">
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent"
        animate={{
          x: ['-100%', '200%'],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'linear',
        }}
      />
    </div>
  )
}

/**
 * Alternative: Pulsing Dots with Glow
 * Uncomment to use this instead of bouncing dots
 */
export function PulsingLoader() {
  return (
    <div className="flex items-center gap-2 py-2">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="w-2.5 h-2.5 bg-blue-500 rounded-full"
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.6, 1, 0.6],
          }}
          transition={{
            duration: 1.2,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: i * 0.2,
          }}
          style={{
            boxShadow: '0 0 8px rgba(59, 130, 246, 0.5)',
          }}
        />
      ))}
    </div>
  )
}
