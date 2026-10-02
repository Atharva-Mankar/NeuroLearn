import { useState } from 'react'
import { User, Clock, Video } from 'lucide-react'
import { settingsData } from '../settingsDefaults'

const SettingsPage = () => {
  const [formData, setFormData] = useState(settingsData)

  const handleChange = (section, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // Future phase: save to backend
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
                  value={formData.profile.name}
                  onChange={(e) => handleChange('profile', 'name', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
                <input
                  type="email"
                  value={formData.profile.email}
                  onChange={(e) => handleChange('profile', 'email', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Timezone</label>
                <select
                  value={formData.profile.timezone}
                  onChange={(e) => handleChange('profile', 'timezone', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                >
                  <option value="UTC+5:30">UTC+5:30</option>
                  <option value="UTC+0">UTC+0</option>
                  <option value="UTC-5">UTC-5</option>
                  <option value="UTC-8">UTC-8</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Language</label>
                <select
                  value={formData.profile.language}
                  onChange={(e) => handleChange('profile', 'language', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                >
                  <option value="English">English</option>
                  <option value="Spanish">Spanish</option>
                  <option value="French">French</option>
                  <option value="German">German</option>
                </select>
              </div>
            </div>
          </section>

          {/* Study Preferences */}
          <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Clock size={24} className="text-slate-400" />
              <h2 className="text-xl font-semibold text-slate-900">Study Preferences</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Weekly Goal (hours)</label>
                <input
                  type="number"
                  value={formData.studyPreferences.weeklyGoalHours}
                  onChange={(e) => handleChange('studyPreferences', 'weeklyGoalHours', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Daily Goal (minutes)</label>
                <input
                  type="number"
                  value={formData.studyPreferences.dailyGoalMinutes}
                  onChange={(e) => handleChange('studyPreferences', 'dailyGoalMinutes', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Preferred Start Time</label>
                <input
                  type="time"
                  value={formData.studyPreferences.preferredStartTime}
                  onChange={(e) => handleChange('studyPreferences', 'preferredStartTime', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Preferred End Time</label>
                <input
                  type="time"
                  value={formData.studyPreferences.preferredEndTime}
                  onChange={(e) => handleChange('studyPreferences', 'preferredEndTime', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Break Reminder (minutes)</label>
                <input
                  type="number"
                  value={formData.studyPreferences.breakReminderInterval}
                  onChange={(e) => handleChange('studyPreferences', 'breakReminderInterval', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
            </div>
          </section>

          {/* Session Preferences */}
          <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Clock size={24} className="text-slate-400" />
              <h2 className="text-xl font-semibold text-slate-900">Session Preferences</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Default Duration (minutes)</label>
                <input
                  type="number"
                  value={formData.sessionPreferences.defaultDuration}
                  onChange={(e) => handleChange('sessionPreferences', 'defaultDuration', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.sessionPreferences.autoPauseOnInactivity}
                  onChange={(e) => handleChange('sessionPreferences', 'autoPauseOnInactivity', e.target.checked)}
                  className="w-5 h-5 rounded border-slate-300 text-slate-600 focus:ring-slate-500"
                />
                <label className="text-sm font-medium text-slate-700">Auto-pause on inactivity</label>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Inactivity Threshold (minutes)</label>
                <input
                  type="number"
                  value={formData.sessionPreferences.inactivityThreshold}
                  onChange={(e) => handleChange('sessionPreferences', 'inactivityThreshold', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                />
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.sessionPreferences.showFatigueDuringSession}
                  onChange={(e) => handleChange('sessionPreferences', 'showFatigueDuringSession', e.target.checked)}
                  className="w-5 h-5 rounded border-slate-300 text-slate-600 focus:ring-slate-500"
                />
                <label className="text-sm font-medium text-slate-700">Show fatigue during session</label>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.sessionPreferences.playCompletionSound}
                  onChange={(e) => handleChange('sessionPreferences', 'playCompletionSound', e.target.checked)}
                  className="w-5 h-5 rounded border-slate-300 text-slate-600 focus:ring-slate-500"
                />
                <label className="text-sm font-medium text-slate-700">Play completion sound</label>
              </div>
            </div>
          </section>

          {/* Webcam Preferences */}
          <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Video size={24} className="text-slate-400" />
              <h2 className="text-xl font-semibold text-slate-900">Webcam Monitoring Preferences</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.webcamPreferences.enableMonitoring}
                  onChange={(e) => handleChange('webcamPreferences', 'enableMonitoring', e.target.checked)}
                  className="w-5 h-5 rounded border-slate-300 text-slate-600 focus:ring-slate-500"
                />
                <label className="text-sm font-medium text-slate-700">Enable webcam monitoring</label>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Monitoring Frequency</label>
                <select
                  value={formData.webcamPreferences.monitoringFrequency}
                  onChange={(e) => handleChange('webcamPreferences', 'monitoringFrequency', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.webcamPreferences.saveFrames}
                  onChange={(e) => handleChange('webcamPreferences', 'saveFrames', e.target.checked)}
                  className="w-5 h-5 rounded border-slate-300 text-slate-600 focus:ring-slate-500"
                />
                <label className="text-sm font-medium text-slate-700">Save frames for analysis</label>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.webcamPreferences.privacyMode}
                  onChange={(e) => handleChange('webcamPreferences', 'privacyMode', e.target.checked)}
                  className="w-5 h-5 rounded border-slate-300 text-slate-600 focus:ring-slate-500"
                />
                <label className="text-sm font-medium text-slate-700">Privacy mode</label>
              </div>
            </div>
          </section>

          <div className="flex justify-end">
            <button
              type="submit"
              className="px-6 py-3 bg-slate-900 text-white rounded-lg font-medium hover:bg-slate-800 transition-colors"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SettingsPage