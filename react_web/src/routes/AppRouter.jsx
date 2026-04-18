import { Navigate, Route, Routes } from 'react-router-dom'

import ProtectedRoute from '../components/ProtectedRoute'
import DashboardPage from '../pages/DashboardPage'
import DiagnosisPage from '../pages/DiagnosisPage'
import LoginPage from '../pages/LoginPage'
import RegisterPage from '../pages/RegisterPage'

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      {/* Public diagnosis page - no login required */}
      <Route path="/diagnosis" element={<DiagnosisPage />} />
      <Route path="/" element={<Navigate to="/diagnosis" replace />} />
      <Route path="*" element={<Navigate to="/diagnosis" replace />} />
    </Routes>
  )
}
