import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'
import './index.css'
import Layout from './components/layout/Layout'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import DashboardPage from './pages/DashboardPage'
import SessionPage from './pages/SessionPage'
import CalendarPage from './pages/CalendarPage'
import HistoryPage from './pages/HistoryPage'
import InsightsPage from './pages/InsightsPage'
import SettingsPage from './pages/SettingsPage'
import { AuthProvider } from './context/AuthContext'

// Development-only: exposes window.testBackendHealth() for Phase 3 testing
import './utils/devHealthCheck'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/session" element={<SessionPage />} />
            <Route path="/calendar" element={<CalendarPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/insights" element={<InsightsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  </StrictMode>,
)