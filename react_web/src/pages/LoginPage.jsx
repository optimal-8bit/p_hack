import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { clearAuthError, fetchCurrentUser, loginUser } from '../features/auth/authSlice'
import GoogleOAuthButton from '../components/auth/GoogleOAuthButton'
import '../components/auth/GoogleOAuthButton.css'
import SoftAurora from '../components/ui/SoftAurora'

// Aurora constants outside component — prevents WebGL restart on every keystroke
const AURORA_SPEED          = 0.6;
const AURORA_SCALE          = 1.5;
const AURORA_BRIGHTNESS     = 1;
const AURORA_COLOR1         = '#f7f7f7';
const AURORA_COLOR2         = '#e100ff';
const AURORA_NOISE_FREQ     = 2.5;
const AURORA_NOISE_AMP      = 1;
const AURORA_BAND_HEIGHT    = 0.5;
const AURORA_BAND_SPREAD    = 1;
const AURORA_OCTAVE_DECAY   = 0.1;
const AURORA_LAYER_OFFSET   = 0;
const AURORA_COLOR_SPEED    = 1;
const AURORA_MOUSE_INFLUENCE = 0.25;

const inputStyle = {
  width: '100%',
  background: 'rgba(255,255,255,0.05)',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: '12px',
  padding: '14px 16px',
  fontSize: '14px',
  color: '#fff',
  outline: 'none',
  fontFamily: 'inherit',
  fontWeight: 500,
  boxSizing: 'border-box',
  transition: 'border-color 0.2s, background 0.2s',
}

export default function LoginPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { token, status, error } = useSelector((state) => state.auth)
  const user = useSelector((state) => state.auth.user)

  const [form, setForm] = useState({ email: '', password: '' })
  const [focusedField, setFocusedField] = useState(null)

  useEffect(() => {
    console.log('🔍 Login redirect check:', { token, status, user, role: user?.role })
    if (token && status === 'succeeded') {
      // Redirect based on role from login response
      const userRole = user?.role || 'patient'
      console.log('🚀 Redirecting to:', userRole === 'doctor' ? '/doctor-dashboard' : '/chat')
      if (userRole === 'doctor') {
        navigate('/doctor-dashboard', { replace: true })
      } else {
        navigate('/chat', { replace: true })
      }
    }
  }, [token, status, user, navigate])

  const onChange = (e) => {
    dispatch(clearAuthError())
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }
  const onSubmit = async (e) => { e.preventDefault(); await dispatch(loginUser(form)) }

  const loading = status === 'loading'

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: '100vh',
      minHeight: '100vh',
      overflow: 'hidden',
      background: '#0A0A10',
      fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      color: '#fff',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      {/* WebGL Aurora — fills the entire background */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
        <SoftAurora
          speed={AURORA_SPEED}
          scale={AURORA_SCALE}
          brightness={AURORA_BRIGHTNESS}
          color1={AURORA_COLOR1}
          color2={AURORA_COLOR2}
          noiseFrequency={AURORA_NOISE_FREQ}
          noiseAmplitude={AURORA_NOISE_AMP}
          bandHeight={AURORA_BAND_HEIGHT}
          bandSpread={AURORA_BAND_SPREAD}
          octaveDecay={AURORA_OCTAVE_DECAY}
          layerOffset={AURORA_LAYER_OFFSET}
          colorSpeed={AURORA_COLOR_SPEED}
          enableMouseInteraction
          mouseInfluence={AURORA_MOUSE_INFLUENCE}
        />
      </div>

      {/* Foreground */}
      <div style={{
        position: 'relative',
        zIndex: 10,
        width: '100%',
        padding: '2rem 1rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        {/* Glass card */}
        <div style={{
          width: '100%',
          maxWidth: 440,
          borderRadius: 24,
          border: '1px solid rgba(255,255,255,0.1)',
          background: 'rgba(12,12,22,0.45)',
          padding: 'clamp(1.5rem, 5vw, 2.5rem)',
          backdropFilter: 'blur(24px)',
          WebkitBackdropFilter: 'blur(24px)',
          boxShadow: '0 0 80px -20px rgba(82,39,255,0.3)',
        }}>
          <div style={{ marginBottom: 32 }}>
            <h1 style={{ fontSize: 28, fontWeight: 700, letterSpacing: '-0.03em', margin: '0 0 8px', lineHeight: 1.2, color: '#ffffff', textShadow: '0 0 24px rgba(255,255,255,0.25)' }}>
              Sign in
            </h1>
            <p style={{ color: 'rgba(255,255,255,0.65)', fontSize: 15, margin: 0 }}>
              Sign in to your MediScan AI account.
            </p>
          </div>

          <form onSubmit={onSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            {error && (
              <div style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '10px 14px',
                background: 'rgba(239,68,68,0.1)',
                border: '1px solid rgba(239,68,68,0.2)',
                borderRadius: 10, color: '#fca5a5', fontSize: 13,
              }}>
                <span style={{ fontSize: 16 }}>⚠</span>
                <span>{error}</span>
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <label style={{ fontSize: 13, fontWeight: 600, color: 'rgba(255,255,255,0.9)' }}>Email*</label>
              <input
                type="email" name="email" placeholder="Enter your email"
                value={form.email} onChange={onChange} required autoComplete="email"
                onFocus={() => setFocusedField('email')} onBlur={() => setFocusedField(null)}
                style={{
                  ...inputStyle,
                  borderColor: focusedField === 'email' ? 'rgba(110,59,252,0.6)' : 'rgba(255,255,255,0.1)',
                  background:  focusedField === 'email' ? 'rgba(255,255,255,0.08)' : 'rgba(255,255,255,0.05)',
                }}
              />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <label style={{ fontSize: 13, fontWeight: 600, color: 'rgba(255,255,255,0.9)' }}>Password*</label>
              <input
                type="password" name="password" placeholder="Enter your password"
                value={form.password} onChange={onChange} required autoComplete="current-password"
                onFocus={() => setFocusedField('password')} onBlur={() => setFocusedField(null)}
                style={{
                  ...inputStyle,
                  borderColor: focusedField === 'password' ? 'rgba(110,59,252,0.6)' : 'rgba(255,255,255,0.1)',
                  background:  focusedField === 'password' ? 'rgba(255,255,255,0.08)' : 'rgba(255,255,255,0.05)',
                }}
              />
            </div>

            <button
              type="submit" disabled={loading}
              style={{
                width: '100%', marginTop: 4,
                background: loading ? 'rgba(110,59,252,0.5)' : 'linear-gradient(135deg, #6E3BFC 0%, #4A1ACA 100%)',
                color: '#fff', fontWeight: 600, borderRadius: 12,
                padding: '14px 16px', fontSize: 15, border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer', fontFamily: 'inherit',
                boxShadow: '0 8px 32px -8px rgba(110,59,252,0.5)',
                opacity: loading ? 0.7 : 1,
              }}
            >
              {loading ? 'Signing in…' : 'Sign in'}
            </button>
          </form>

          {/* Divider */}
          <div className="divider" style={{ margin: '24px 0' }}>
            <span>or</span>
          </div>

          {/* Google OAuth Button */}
          <GoogleOAuthButton 
            text="Continue with Google"
            onSuccess={(result) => {
              console.log('✅ Google login successful from LoginPage:', result)
              // Navigation is handled by the button component
            }}
            onError={(error) => {
              console.error('❌ Google login error from LoginPage:', error)
            }}
          />

          <p style={{ marginTop: 32, textAlign: 'center', fontSize: 13, color: 'rgba(255,255,255,0.5)' }}>
            Don&apos;t have an account?{' '}
            <Link to="/register" style={{ color: '#fff', fontWeight: 500, textDecoration: 'none' }}>Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
