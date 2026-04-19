import { useState } from 'react'
import MorphingLoader, { LoadingWrapper } from '../components/MorphingLoader'

/**
 * Demo page to showcase the MorphingLoader component
 * Access at: /morphing-loader-demo
 */
export default function MorphingLoaderDemo() {
  const [showFullScreen, setShowFullScreen] = useState(false)
  const [simulateLoading, setSimulateLoading] = useState(false)

  const handleSimulateLoad = () => {
    setSimulateLoading(true)
    setTimeout(() => {
      setSimulateLoading(false)
    }, 3000)
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
      padding: '2rem',
      color: '#ffffff',
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: 700,
          marginBottom: '1rem',
          background: 'linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
        }}>
          Morphing Loader Demo
        </h1>
        <p style={{ color: 'rgba(255,255,255,0.7)', marginBottom: '3rem', fontSize: '1.125rem' }}>
          Modern loading animation with shape morphing and gradient transitions
        </p>

        {/* Size Variations */}
        <section style={{ marginBottom: '4rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>
            Size Variations
          </h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '2rem',
          }}>
            {['sm', 'md', 'lg', 'xl'].map(size => (
              <div key={size} style={{
                padding: '2rem',
                background: 'rgba(255,255,255,0.05)',
                borderRadius: '12px',
                border: '1px solid rgba(255,255,255,0.1)',
                textAlign: 'center',
              }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem', textTransform: 'uppercase' }}>
                  {size}
                </h3>
                <MorphingLoader size={size} color="gradient" />
              </div>
            ))}
          </div>
        </section>

        {/* Color Themes */}
        <section style={{ marginBottom: '4rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>
            Color Themes
          </h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '2rem',
          }}>
            {['blue', 'purple', 'gradient'].map(color => (
              <div key={color} style={{
                padding: '2rem',
                background: 'rgba(255,255,255,0.05)',
                borderRadius: '12px',
                border: '1px solid rgba(255,255,255,0.1)',
                textAlign: 'center',
              }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem', textTransform: 'capitalize' }}>
                  {color}
                </h3>
                <MorphingLoader size="lg" color={color} />
              </div>
            ))}
          </div>
        </section>

        {/* With Messages */}
        <section style={{ marginBottom: '4rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>
            With Loading Messages
          </h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '2rem',
          }}>
            <div style={{
              padding: '2rem',
              background: 'rgba(255,255,255,0.05)',
              borderRadius: '12px',
              border: '1px solid rgba(255,255,255,0.1)',
            }}>
              <MorphingLoader 
                size="md" 
                color="blue" 
                message="Loading dashboard data..."
              />
            </div>
            <div style={{
              padding: '2rem',
              background: 'rgba(255,255,255,0.05)',
              borderRadius: '12px',
              border: '1px solid rgba(255,255,255,0.1)',
            }}>
              <MorphingLoader 
                size="md" 
                color="purple" 
                message="Finding specialists..."
              />
            </div>
            <div style={{
              padding: '2rem',
              background: 'rgba(255,255,255,0.05)',
              borderRadius: '12px',
              border: '1px solid rgba(255,255,255,0.1)',
            }}>
              <MorphingLoader 
                size="md" 
                color="gradient" 
                message="Processing your request..."
              />
            </div>
          </div>
        </section>

        {/* Full Screen Demo */}
        <section style={{ marginBottom: '4rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>
            Full Screen Overlay
          </h2>
          <div style={{
            padding: '2rem',
            background: 'rgba(255,255,255,0.05)',
            borderRadius: '12px',
            border: '1px solid rgba(255,255,255,0.1)',
            textAlign: 'center',
          }}>
            <p style={{ color: 'rgba(255,255,255,0.7)', marginBottom: '1rem' }}>
              Click the button to see the full-screen loader overlay
            </p>
            <button
              onClick={() => {
                setShowFullScreen(true)
                setTimeout(() => setShowFullScreen(false), 3000)
              }}
              style={{
                padding: '12px 24px',
                background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'transform 0.2s',
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              Show Full Screen Loader
            </button>
          </div>
        </section>

        {/* LoadingWrapper Demo */}
        <section style={{ marginBottom: '4rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>
            LoadingWrapper Component
          </h2>
          <div style={{
            padding: '2rem',
            background: 'rgba(255,255,255,0.05)',
            borderRadius: '12px',
            border: '1px solid rgba(255,255,255,0.1)',
          }}>
            <p style={{ color: 'rgba(255,255,255,0.7)', marginBottom: '1rem', textAlign: 'center' }}>
              Simulates a 3-second data load with minimum visible time handling
            </p>
            <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
              <button
                onClick={handleSimulateLoad}
                disabled={simulateLoading}
                style={{
                  padding: '12px 24px',
                  background: simulateLoading ? 'rgba(255,255,255,0.1)' : 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  fontWeight: 600,
                  cursor: simulateLoading ? 'not-allowed' : 'pointer',
                  opacity: simulateLoading ? 0.6 : 1,
                }}
              >
                {simulateLoading ? 'Loading...' : 'Simulate Data Load'}
              </button>
            </div>
            <LoadingWrapper 
              loading={simulateLoading}
              loaderProps={{ size: 'lg', color: 'gradient', message: 'Loading data...' }}
            >
              <div style={{
                padding: '2rem',
                background: 'rgba(34, 197, 94, 0.1)',
                border: '1px solid rgba(34, 197, 94, 0.3)',
                borderRadius: '8px',
                textAlign: 'center',
              }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#22c55e', marginBottom: '0.5rem' }}>
                  ✓ Data Loaded Successfully
                </h3>
                <p style={{ color: 'rgba(255,255,255,0.7)' }}>
                  This content appears after the loading state completes
                </p>
              </div>
            </LoadingWrapper>
          </div>
        </section>

        {/* Usage Code */}
        <section>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>
            Usage Example
          </h2>
          <div style={{
            padding: '1.5rem',
            background: 'rgba(0,0,0,0.3)',
            borderRadius: '12px',
            border: '1px solid rgba(255,255,255,0.1)',
            fontFamily: 'monospace',
            fontSize: '0.875rem',
            overflow: 'auto',
          }}>
            <pre style={{ margin: 0, color: '#e2e8f0' }}>
{`import MorphingLoader from '@/components/MorphingLoader'

// Basic usage
<MorphingLoader 
  size="lg" 
  color="gradient" 
  message="Loading..."
/>

// In a component
{loading ? (
  <MorphingLoader 
    size="lg" 
    color="blue" 
    message="Loading data..."
  />
) : (
  <YourContent />
)}`}
            </pre>
          </div>
        </section>
      </div>

      {/* Full Screen Loader */}
      {showFullScreen && (
        <MorphingLoader 
          fullScreen={true}
          size="xl"
          color="gradient"
          message="Loading application..."
        />
      )}
    </div>
  )
}
