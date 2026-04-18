import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { clearAuthError, fetchCurrentUser, loginUser, loginWithGoogle } from '../features/auth/authSlice'
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

function GoogleIcon() {
  return (
    <svg viewBox="0 0 24 24" style={{ width: 16, height: 16, flexShrink: 0 }} fill="none">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
    </svg>
  )
}

function AppleIcon() {
  return (
    <svg viewBox="0 0 24 24" style={{ width: 15, height: 15, flexShrink: 0 }} fill="currentColor">
      <path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/>
    </svg>
  )
}

export default function LoginPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { token, status, error } = useSelector((state) => state.auth)

  const [form, setForm] = useState({ email: '', password: '' })
  const [googleReady, setGoogleReady] = useState(false)
  const [focusedField, setFocusedField] = useState(null)

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
    if (!clientId) return
    const initGoogle = () => {
      if (!window.google?.accounts?.id) return
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: ({ credential }) => { if (credential) dispatch(loginWithGoogle(credential)) },
      })
      setGoogleReady(true)
    }
    const existing = document.getElementById('google-identity-script')
    if (existing) { initGoogle(); return }
    const script = document.createElement('script')
    script.id = 'google-identity-script'
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true; script.defer = true
    script.onload = initGoogle
    script.onerror = () => setGoogleReady(false)
    document.head.appendChild(script)
  }, [dispatch])

  useEffect(() => {
    if (token) { dispatch(fetchCurrentUser()); navigate('/dashboard', { replace: true }) }
  }, [token, dispatch, navigate])

  const onChange = (e) => {
    dispatch(clearAuthError())
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }
  const onSubmit = async (e) => { e.preventDefault(); await dispatch(loginUser(form)) }
  const handleGoogleSignIn = () => {
    if (!window.google?.accounts?.id) { dispatch(clearAuthError()); return }
    window.google.accounts.id.prompt()
  }

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

          <div style={{ marginTop: 20, display: 'flex', gap: 12 }}>
            {[
              { label: 'Google', icon: <GoogleIcon />, onClick: handleGoogleSignIn, disabled: !googleReady || loading },
              { label: 'Apple',  icon: <AppleIcon />,  onClick: undefined,          disabled: false },
            ].map(({ label, icon, onClick, disabled }) => (
              <button key={label} type="button" onClick={onClick} disabled={disabled}
                style={{
                  flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
                  background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: 12, padding: '12px', fontSize: 13, fontWeight: 600,
                  color: 'rgba(255,255,255,0.85)', cursor: disabled ? 'not-allowed' : 'pointer',
                  fontFamily: 'inherit', opacity: disabled ? 0.5 : 1,
                }}
              >
                {icon} {label}
              </button>
            ))}
          </div>

          <p style={{ marginTop: 32, textAlign: 'center', fontSize: 13, color: 'rgba(255,255,255,0.5)' }}>
            Don&apos;t have an account?{' '}
            <Link to="/register" style={{ color: '#fff', fontWeight: 500, textDecoration: 'none' }}>Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
