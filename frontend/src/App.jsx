import { Navigate } from 'react-router-dom'

// The root path has no page of its own, so it sends the user to the dashboard.
function App() {
  return <Navigate to="/dashboard" replace />
}

export default App
