import { Navigate, Route, Routes } from 'react-router-dom'

import ProtectedRoute from '../components/ProtectedRoute'
import DashboardPage from '../pages/DashboardPage'
import IntroPage from '../pages/intro/IntroPage'
import LoginPage from '../pages/LoginPage'
import RegisterPage from '../pages/RegisterPage'
import MentalHealthChatPage from '../pages/MentalHealthChatPage'
import MedicineReminderPage from '../pages/MedicineReminderPage'
import DoctorDashboardPage from '../pages/doctor/DoctorDashboardPage'
import DoctorAppointmentsPage from '../pages/doctor/DoctorAppointmentsPage'
import DoctorPatientsPage from '../pages/doctor/DoctorPatientsPage'
import DoctorPrescriptionsPage from '../pages/doctor/DoctorPrescriptionsPage'
import DoctorProfilePage from '../pages/doctor/DoctorProfilePage'
import TestTailwind from '../pages/TestTailwind'
import TestDoctorRecommendation from '../components/chat/TestDoctorRecommendation'

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
      
      {/* Doctor Dashboard Routes */}
      <Route path="/doctor-dashboard" element={<DoctorDashboardPage />} />
      <Route path="/doctor-appointments" element={<DoctorAppointmentsPage />} />
      <Route path="/doctor-patients" element={<DoctorPatientsPage />} />
      <Route path="/doctor-prescriptions" element={<DoctorPrescriptionsPage />} />
      <Route path="/doctor-profile" element={<DoctorProfilePage />} />
      
      {/* Test Routes */}
      <Route path="/test-tailwind" element={<TestTailwind />} />
      <Route path="/test-doctor-recommendation" element={<TestDoctorRecommendation />} />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
