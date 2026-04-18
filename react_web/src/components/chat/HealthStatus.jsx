import { useState, useEffect } from 'react'
import { chatService } from '../../services/chatService'
import './HealthStatus.css'

export default function HealthStatus() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const loadHealth = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await chatService.getHealth()
      setHealth(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadHealth()
    // Refresh every 30 seconds
    const interval = setInterval(loadHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading && !health) {
    return (
      <div className="health-status">
        <div className="health-loading">Loading status...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="health-status">
        <div className="health-error">
          <div className="status-indicator error"></div>
          <div>
            <div className="status-text">Backend Offline</div>
            <div className="status-detail">Cannot connect to server</div>
          </div>
        </div>
        <button onClick={loadHealth} className="refresh-btn">Retry</button>
      </div>
    )
  }

  if (!health) return null

  const isHealthy = health.status === 'healthy'

  return (
    <div className="health-status">
      <div className="health-header">
        <div className="status-indicator" data-status={health.status}></div>
        <div>
          <div className="status-text">{health.status.toUpperCase()}</div>
          <div className="status-detail">v{health.version}</div>
        </div>
      </div>

      <div className="models-list">
        {Object.entries(health.models_loaded || {}).map(([model, loaded]) => (
          <div key={model} className="model-item">
            <span className="model-name">{model}</span>
            <span className={`model-status ${loaded ? 'loaded' : 'not-loaded'}`}>
              {loaded ? '✓' : '✗'}
            </span>
          </div>
        ))}
      </div>

      <button onClick={loadHealth} className="refresh-btn">Refresh</button>
    </div>
  )
}
