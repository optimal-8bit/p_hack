import PropTypes from 'prop-types'

function getInitials(name) {
  if (!name) return '??'
  const parts = name.trim().split(' ')
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

export default function UserProfileSection({ user }) {
  const initials = getInitials(user.name)

  return (
    <div className="user-profile-section">
      <div className="user-avatar">
        <span>{initials}</span>
      </div>
      <div className="user-info">
        <div className="user-name">{user.name}</div>
        <div className="user-plan">{user.plan}</div>
      </div>
    </div>
  )
}

UserProfileSection.propTypes = {
  user: PropTypes.shape({
    name: PropTypes.string.isRequired,
    plan: PropTypes.string.isRequired,
  }).isRequired,
}
