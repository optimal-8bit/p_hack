import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import { useDispatch, useSelector } from 'react-redux'

import { fetchCurrentUser, logout } from '../features/auth/authSlice'

export default function DashboardPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const user = useSelector((state) => state.auth.user)

  useEffect(() => {
    if (!user) {
      dispatch(fetchCurrentUser())
    }
  }, [dispatch, user])

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login', { replace: true })
  }

  return (
    <main className="dashboard-shell">
      <section className="dashboard-card">
        <h1>Dashboard</h1>
        <p>Authentication is wired with Redux + service layer + central API client.</p>

        <div className="profile-box">
          <p>
            <strong>Name:</strong> {user?.name || 'Loading...'}
          </p>
          <p>
            <strong>Email:</strong> {user?.email || 'Loading...'}
          </p>
          <p>
            <strong>Provider:</strong> {user?.auth_provider || 'local'}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <button onClick={() => navigate('/chat')}>Open Mental Health Chat</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </section>
    </main>
  )
}
