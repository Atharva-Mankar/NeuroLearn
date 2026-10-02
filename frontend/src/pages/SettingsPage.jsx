import { useState, useEffect } from 'react'
import { User, Clock, Video } from 'lucide-react'
import { getProfile, updateProfile } from '../services/api'
import { useAuthContext } from '../context/AuthContext'

const SettingsPage = () => {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [updateLoading, setUpdateLoading] = useState(false)
  const { updateUser } = useAuthContext()

  // Fetch real user data from API
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await getProfile()
        setProfile(response)
      } catch (err) {
        setError(err.message || 'Unable to load profile. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [])

  const handleNameChange = (e) => {
    setProfile(prev => ({
      ...prev,
      name: e.target.value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!profile) return

    try {
      setUpdateLoading(true)
      setError(null)

      // Only allow updating name (email is login identifier, should not change)
      const response = await updateProfile({ name: profile.name })

      // Update AuthContext and localStorage so Navbar initials update
      updateUser(response)

      // Show success message (could use toast, but for now just reset)
      setError('Profile updated successfully!')
      setTimeout(() => setError(null), 3000)
    } catch (err) {
      setError(err.message || 'Failed to update profile. Please try again.')
    } finally {
      setUpdateLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-lg text-slate-600">Loading settings...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="text-lg text-slate-900 mb-4">Unable to load settings</div>
          <div className="text-sm text-slate-600 mb-6">{error}</div>
          <button
            onClick={() => window.location.reload()}
            className="px-5 py-3 bg-slate-900 text-white rounded-lg font-medium transition-colors hover:bg-slate-800"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-lg text-slate-600">No profile data available</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-slate-900">Settings</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Profile Section */}
          <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <User size={24} className="text-slate-400" />
              <h2 className="text-xl font-semibold text-slate-900">Profile</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Name</label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={handleNameChange}
                  disabled={updateLoading}
                  className={`
                    w-full px-3 py-2 border border-slate-300 rounded-lg
                    focus:outline-none focus:ring-2 focus:ring-slate-500
                    ${updateLoading ? 'opacity-50' : ''}
                  `}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
                <input
                  type="email"
                  value={profile.email}
                  readOnly
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500 opacity-75"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Timezone</label>
                <select
                  disabled
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500 opacity-75"
                >
                  <option value="UTC+0">UTC+0</option>
                </select>
                <p className="text-xs text-slate-500 mt-1">Read-only (displayed from backend)</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Language</label>
                <select
                  disabled
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500 opacity-75"
                >
                  <option value="English">English</option>
                </select>
                <p className="text-xs text-slate-500 mt-1">Read-only (displayed from backend)</p>
              </div>
            </div>
          </section>

          {/* Study Preferences - Marked as unavailable */}
          <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Clock size={24} className="text-slate-400" />
              <h2 className="text-xl font-semibold text-slate-900">Study Preferences</h2>
            </div>
            <div className="bg-slate-50 p-4 rounded">
              <p className="text-sm text-slate-600">
                These settings are not yet implemented in this version.
                Weekly/daily goals, preferred times, and break reminders
                will be available in a future update.
              </p>
            </div>
          </section>

          {/* Session Preferences - Marked as unavailable */}
          <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Clock size={24} className="text-slate-400" />
              <h2 className="text-xl font-semibold text-slate-900">Session Preferences</h2>
            </div>
            <div className="bg-slate-50 p-4 rounded">
              <p className="text-sm text-slate-600">
                Session settings like auto-pause, fatigue display, and completion sounds
                are not yet implemented in this version. These will be available in a future update.
              </p>
            </div>
          </section>

          {/* Webcam Preferences - Marked as unavailable */}
          <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Video size={24} className="text-slate-400" />
              <h2 className="text-xl font-semibold text-slate-900">Webcam Monitoring Preferences</h2>
            </div>
            <div className="bg-slate-50 p-4 rounded">
              <p className="text-sm text-slate-600">
                Webcam monitoring settings are not yet implemented in this version.
                Enable/disable monitoring, frequency, frame saving, and privacy mode
                will be available in a future update.
              </p>
            </div>
          </section>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={updateLoading || !profile.name.trim()}
              className={`
                px-6 py-3
                ${!profile.name.trim() || updateLoading ? 'bg-slate-400' : 'bg-slate-900'}
                text-white rounded-lg font-medium
                hover:${!profile.name.trim() || updateLoading ? 'bg-slate-300' : 'bg-slate-800'}
                transition-colors
              `}
            >
              {updateLoading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SettingsPage