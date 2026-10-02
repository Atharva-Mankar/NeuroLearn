import { useState } from 'react'
import { LogIn, Mail, Lock } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login: loginUser } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Guard against duplicate submissions while a request is in flight
    if (loading) return

    setError(null)
    setLoading(true)

    try {
      await loginUser(email, password)
      // Credentials are valid. No session/JWT yet — AuthContext persists the
      // safe user object and navigates. This does NOT create backend auth.
      navigate('/dashboard')
    } catch (err) {
      if (err.message.includes('Network error')) {
        setError('Unable to reach the server. Please try again later.')
      } else if (err.message.includes('Invalid email or password')) {
        setError('Invalid email or password.')
      } else {
        setError(err.message || 'Login failed. Please try again.')
      }
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-slate-900">Welcome back</h2>
          <p className="text-sm text-slate-600">
            Sign in to your NeuroLearn account
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-2">
            <label htmlFor="email" className="block text-sm font-medium text-slate-700">
              Email
            </label>
            <div className="flex items-center gap-2 border border-slate-300 rounded-lg px-3 py-2 focus-within:border-slate-500 focus-within:ring-2 focus-within:ring-slate-200">
              <Mail size={20} className="text-slate-400" />
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                className="flex-1 border-none outline-none text-sm"
                autoFocus
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="block text-sm font-medium text-slate-700">
              Password
            </label>
            <div className="flex items-center gap-2 border border-slate-300 rounded-lg px-3 py-2 focus-within:border-slate-500 focus-within:ring-2 focus-within:ring-slate-200">
              <Lock size={20} className="text-slate-400" />
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="flex-1 border-none outline-none text-sm"
                required
              />
            </div>
          </div>

          {error && (
            <p className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg text-sm font-medium transition-colors
              ${loading
                ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
                : 'bg-slate-900 text-white hover:bg-slate-800'
              }
            `}
          >
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
                </svg>
                <span>Signing in...</span>
              </>
            ) : (
              <>
                <LogIn size={20} />
                <span>Sign In</span>
              </>
            )}
          </button>
        </form>

        <div className="text-center">
          <p className="text-sm text-slate-500">
            Don't have an account?{' '}
            <Link to="/signup" className="font-medium text-slate-900 hover:text-slate-800">
              Create one
            </Link>
          </p>
          <p className="text-xs text-slate-400">
            Forgot password?{' '}
            <Link to="#" className="font-medium text-slate-900 hover:text-slate-800">
              Reset it
            </Link>
          </p>
        </div>

        <div className="text-center text-xs text-slate-400">
          NeuroLearn v0.1.0
        </div>
      </div>
    </div>
  )
}

export default LoginPage