import { Navigate, Route, Routes } from 'react-router-dom'

import ProtectedRoute from '../components/ProtectedRoute'
import DashboardPage from '../pages/DashboardPage'
import IntroPage from '../pages/intro/IntroPage'
import LoginPage from '../pages/LoginPage'
import RegisterPage from '../pages/RegisterPage'
import MentalHealthChatPage from '../pages/MentalHealthChatPage'
import MedicineReminderPage from '../pages/MedicineReminderPage'

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<IntroPage />} />
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
      <Route path="/chat" element={<MentalHealthChatPage />} />
      <Route path="/medicine-reminder" element={<MedicineReminderPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
