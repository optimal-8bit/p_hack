import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useDispatch, useSelector } from 'react-redux'

import { clearAuthError, fetchCurrentUser, loginUser, loginWithGoogle } from '../features/auth/authSlice'

export default function LoginPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { token, status, error } = useSelector((state) => state.auth)

  const [form, setForm] = useState({ email: '', password: '' })
  const [googleReady, setGoogleReady] = useState(false)

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
    if (!clientId) {
      return
    }

    const existingScript = document.getElementById('google-identity-script')

    const initGoogle = () => {
      if (!window.google?.accounts?.id) {
        return
      }

      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: ({ credential }) => {
          if (credential) {
            dispatch(loginWithGoogle(credential))
          }
        },
      })

      setGoogleReady(true)
    }

    if (existingScript) {
      initGoogle()
      return
    }

    const script = document.createElement('script')
    script.id = 'google-identity-script'
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.onload = initGoogle
    script.onerror = () => setGoogleReady(false)
    document.head.appendChild(script)
  }, [dispatch])

  useEffect(() => {
    if (token) {
      dispatch(fetchCurrentUser())
      navigate('/dashboard', { replace: true })
    }
  }, [token, dispatch, navigate])

  const onChange = (event) => {
    dispatch(clearAuthError())
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }))
  }

  const onSubmit = async (event) => {
    event.preventDefault()
    await dispatch(loginUser(form))
  }

  const handleGoogleSignIn = () => {
    if (!window.google?.accounts?.id) {
      dispatch(clearAuthError())
      return
    }

    window.google.accounts.id.prompt()
  }

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <h1>Sign in</h1>
        <p className="auth-subtitle">Welcome back. Continue building fast.</p>

        <form onSubmit={onSubmit} className="auth-form">
          <label>
            Email
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={onChange}
              required
              autoComplete="email"
            />
          </label>

          <label>
            Password
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={onChange}
              required
              autoComplete="current-password"
            />
          </label>

          {error ? <p className="form-error">{error}</p> : null}

          <button type="submit" disabled={status === 'loading'}>
            {status === 'loading' ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <div className="oauth-block">
          <button type="button" onClick={handleGoogleSignIn} disabled={!googleReady || status === 'loading'}>
            Continue with Google
          </button>
        </div>

        <p className="auth-footer">
          No account yet? <Link to="/register">Create one</Link>
        </p>
      </section>
    </main>
  )
}
