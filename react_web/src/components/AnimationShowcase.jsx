import { motion } from 'motion/react'
import { Send, Plus, StopCircle } from 'lucide-react'
import { LoadingIndicator, ShimmerLoader, PulsingLoader, PulsingWaveLoader, SineWaveLoader } from './LoadingIndicator'
import { CameraIcon } from './CameraIcon'

/**
 * AnimationShowcase - Demo component showing all animations and interactions
 * 
 * This component is for demonstration purposes only.
 * Use it to preview all the UI improvements in isolation.
 */
export function AnimationShowcase() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50 p-8">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Chat UI Showcase</h1>
          <p className="text-gray-600">Modern, production-quality components with smooth animations</p>
        </div>

        {/* Icons Section */}
        <section className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Icon Interactions</h2>
          <p className="text-sm text-gray-600 mb-6">
            Hover and click to see micro-interactions (scale + color change)
          </p>
          <div className="flex gap-4">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-3 hover:bg-blue-50 rounded-full transition-all duration-200"
            >
              <CameraIcon className="w-7 h-7" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-3 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-all duration-200"
            >
              <Plus className="w-6 h-6" strokeWidth={2} />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-3 bg-blue-600 text-white hover:bg-blue-700 rounded-full shadow-md hover:shadow-lg transition-all duration-200"
            >
              <Send className="w-6 h-6" strokeWidth={2} />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-full font-medium shadow-lg transition-colors"
            >
              <StopCircle className="w-4 h-4" />
              Stop
            </motion.button>
          </div>
        </section>

        {/* Loading Animations */}
        <section className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Loading Animations</h2>
          <p className="text-sm text-gray-600 mb-6">
            Five different loading styles - all smooth and premium
          </p>
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Wave Dots (Default) - Gradient Colors</h3>
              <LoadingIndicator variant="light" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Pulsing Wave with Glow</h3>
              <PulsingWaveLoader />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Smooth Sine Wave</h3>
              <SineWaveLoader />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Shimmer Effect</h3>
              <ShimmerLoader />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Pulsing Dots</h3>
              <PulsingLoader />
            </div>
          </div>
        </section>

        {/* Chat Bubbles */}
        <section className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Chat Bubbles</h2>
          <p className="text-sm text-gray-600 mb-6">
            Smooth entry animations with fade + slide up
          </p>
          <div className="space-y-4">
            {/* User Message */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="flex justify-end"
            >
              <div className="max-w-[75%] rounded-2xl px-4 py-3 shadow-sm bg-gradient-to-br from-blue-600 to-blue-700 text-white">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-blue-100">
                    You
                  </span>
                </div>
                <p className="text-sm">This is a user message with a beautiful gradient background!</p>
              </div>
            </motion.div>

            {/* Assistant Message */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, ease: 'easeOut', delay: 0.2 }}
              className="flex justify-start"
            >
              <div className="max-w-[75%] rounded-2xl px-4 py-3 shadow-sm bg-white border border-gray-200 text-gray-900">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                    Assistant
                  </span>
                </div>
                <p className="text-sm">This is an assistant message with clean styling and soft shadows.</p>
              </div>
            </motion.div>

            {/* Loading Message */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, ease: 'easeOut', delay: 0.4 }}
              className="flex justify-start"
            >
              <div className="max-w-[75%] rounded-2xl px-4 py-3 shadow-sm bg-white border border-gray-200 text-gray-900">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                    Assistant
                  </span>
                </div>
                <LoadingIndicator variant="light" />
              </div>
            </motion.div>
          </div>
        </section>

        {/* Input Bar */}
        <section className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Input Bar</h2>
          <p className="text-sm text-gray-600 mb-6">
            Pill-shaped design with focus glow effect
          </p>
          <div
            className="
              flex items-end gap-2 px-4 py-2 
              bg-gray-50 border-2 border-gray-200 
              rounded-full shadow-sm
              transition-all duration-200 ease-in-out
              hover:border-blue-500 hover:shadow-md hover:bg-white
            "
          >
            <motion.button
              type="button"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-all duration-200"
            >
              <Plus className="w-5 h-5" strokeWidth={2} />
            </motion.button>

            <motion.button
              type="button"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 hover:bg-blue-50 rounded-full transition-all duration-200"
            >
              <CameraIcon className="w-6 h-6" />
            </motion.button>

            <input
              type="text"
              placeholder="Message the assistant..."
              className="flex-1 bg-transparent border-none outline-none text-gray-900 placeholder-gray-400 text-sm"
            />

            <motion.button
              type="button"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 bg-blue-600 text-white hover:bg-blue-700 rounded-full shadow-md hover:shadow-lg transition-all duration-200"
            >
              <Send className="w-5 h-5" strokeWidth={2} />
            </motion.button>
          </div>
        </section>

        {/* File Chips */}
        <section className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">File Attachments</h2>
          <p className="text-sm text-gray-600 mb-6">
            Smooth scale + fade animations on add/remove
          </p>
          <div className="flex flex-wrap gap-2">
            {['document.pdf', 'image.png', 'data.csv'].map((file, i) => (
              <motion.div
                key={file}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
                className="flex items-center gap-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-xl text-sm"
              >
                <div className="flex flex-col">
                  <span className="font-medium text-gray-900">{file}</span>
                  <span className="text-xs text-gray-500">2.4 KB</span>
                </div>
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  className="p-1 hover:bg-red-50 rounded-full transition-colors"
                >
                  <span className="text-red-500 text-xs">✕</span>
                </motion.button>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500">
          <p>All animations powered by Framer Motion</p>
          <p className="mt-1">Icons from Lucide React • Styled with Tailwind CSS</p>
        </div>
      </div>
    </div>
  )
}
