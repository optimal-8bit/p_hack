import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useDispatch, useSelector } from 'react-redux'

import { clearAuthError, fetchCurrentUser, registerUser } from '../features/auth/authSlice'

export default function RegisterPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { token, status, error } = useSelector((state) => state.auth)

  const [form, setForm] = useState({ name: '', email: '', password: '' })

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
    await dispatch(registerUser(form))
  }

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <h1>Create account</h1>
        <p className="auth-subtitle">Set up your workspace access in seconds.</p>

        <form onSubmit={onSubmit} className="auth-form">
          <label>
            Name
            <input type="text" name="name" value={form.name} onChange={onChange} required />
          </label>

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
              minLength={8}
              autoComplete="new-password"
            />
          </label>

          {error ? <p className="form-error">{error}</p> : null}

          <button type="submit" disabled={status === 'loading'}>
            {status === 'loading' ? 'Creating...' : 'Create account'}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </section>
    </main>
  )
}
