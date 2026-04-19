import { useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import PropTypes from 'prop-types'
import { logout } from '../../features/auth/authSlice'

function getInitials(name) {
  if (!name) return '??'
  const parts = name.trim().split(' ')
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

export default function UserProfileSection({ user }) {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const initials = getInitials(user.name)

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <div className="user-profile-section">
      <div className="user-info-container">
        <div className="user-avatar">
          <span>{initials}</span>
        </div>
        <div className="user-info">
          <div className="user-name">{user.name}</div>
          <div className="user-plan">{user.plan}</div>
        </div>
      </div>
      <button 
        className="logout-btn" 
        onClick={handleLogout}
        title="Logout"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path
            d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>
    </div>
  )
}

UserProfileSection.propTypes = {
  user: PropTypes.shape({
    name: PropTypes.string.isRequired,
    plan: PropTypes.string.isRequired,
  }).isRequired,
}
