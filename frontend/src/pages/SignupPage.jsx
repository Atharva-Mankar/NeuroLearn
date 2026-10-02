import { useState } from 'react'
import { Mail, Lock, Send } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { signup } from '../services/api'

const SignupPage = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const validateForm = () => {
    if (!name.trim()) {
      setError('Name is required')
      return false
    }
    if (!email || !email.includes('@')) {
      setError('Valid email is required')
      return false
    }
    if (!password) {
      setError('Password is required')
      return false
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return false
    }
    return true
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validateForm()) return

    setError(null)
    setLoading(true)

    try {
      await signup({ name, email, password })
      // Navigate to login on success
      setTimeout(() => {
        setLoading(false)
        navigate('/login')
      }, 800)
    } catch (err) {
      // Handle duplicate email error
      if (err.message.includes('already exists')) {
        setError('An account with this email already exists.')
      } else if (err.message.includes('Network error')) {
        setError('Unable to reach the server. Please try again later.')
      } else {
        setError(err.message || 'Signup failed. Please try again.')
      }
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-slate-900">Create Account</h2>
          <p className="text-sm text-slate-600">
            Join NeuroLearn and start optimizing your study sessions
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-2">
            <label htmlFor="name" className="block text-sm font-medium text-slate-700">
              Name
            </label>
            <div className="flex items-center gap-2 border border-slate-300 rounded-lg px-3 py-2 focus-within:border-slate-500 focus-within:ring-2 focus-within:ring-slate-200">
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
                className="flex-1 border-none outline-none text-sm"
                required
              />
            </div>
          </div>

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
                placeholder="Create a password"
                className="flex-1 border-none outline-none text-sm"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="confirm" className="block text-sm font-medium text-slate-700">
              Confirm Password
            </label>
            <div className="flex items-center gap-2 border border-slate-300 rounded-lg px-3 py-2 focus-within:border-slate-500 focus-within:ring-2 focus-within:ring-slate-200">
              <Lock size={20} className="text-slate-400" />
              <input
                id="confirm"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
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
              }`}
          >
            {loading ? (
              <>
                <Send size={20} className="animate-spin h-5 w-5" />
                <span>Creating account...</span>
              </>
            ) : (
              <>
                <Mail size={20} />
                <span>Create Account</span>
              </>
            )}
          </button>

          <div className="text-center mt-4">
            <p className="text-sm text-slate-500">
              Already have an account?{' '}
              <Link to="/login" className="font-medium text-slate-900 hover:text-slate-800">
                Log in
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SignupPage