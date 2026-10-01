import { useEffect, useState } from 'react'
import { subjects, fatigueDisclaimer } from '../data/demoData'
import Button from '../components/ui/Button'
import { createSession } from '../services/api'

const SessionPage = () => {
  const [form, setForm] = useState({
    subject: subjects[0],
    topic: '',
    durationMinutes: 45,
    webcamEnabled: false,
  })
  const [timerSeconds, setTimerSeconds] = useState(0)
  const [isActive, setIsActive] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const startSession = async () => {
    // Basic client-side validation
    if (!form.subject.trim()) {
      setError('Subject is required')
      return
    }
    if (!form.topic.trim()) {
      setError('Topic is required')
      return
    }
    if (form.durationMinutes < 5 || form.durationMinutes > 180) {
      setError('Duration must be between 5 and 180 minutes')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await createSession({
        subject: form.subject.trim(),
        topic: form.topic.trim(),
        duration_minutes: form.durationMinutes,
        webcam_enabled: form.webcamEnabled,
      })
      setSessionId(response.id)
      setTimerSeconds(0)
      setIsActive(true)
      setIsPaused(false)
    } catch (err) {
      setError(err.message || 'Failed to start session. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const pauseSession = () => {
    setIsPaused(true)
  }

  const resumeSession = () => {
    setIsPaused(false)
  }

  const endSession = () => {
    setIsActive(false)
    setIsPaused(false)
    alert('Session ended - saving logic will be added in a later phase.')
  }

  useEffect(() => {
    if (!isActive || isPaused) return undefined

    const intervalId = window.setInterval(() => {
      setTimerSeconds(seconds => seconds + 1)
    }, 1000)

    return () => window.clearInterval(intervalId)
  }, [isActive, isPaused])

  const formatTimer = (totalSeconds) => {
    const hours = Math.floor(totalSeconds / 3600)
    const minutes = Math.floor((totalSeconds % 3600) / 60)
    const seconds = totalSeconds % 60
    return [hours, minutes, seconds]
      .map(n => String(n).padStart(2, '0'))
      .join(':')
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-xl space-y-8 bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex-1 space-y-4">
            <h2 className="text-xl font-bold text-slate-900">Study Session</h2>
            <p className="text-sm text-slate-600">
              Configure your session below and click Start Session to begin.
            </p>
          </div>

          <div className="flex-1 space-y-4 text-center">
            <div className="text-2xl font-bold text-slate-900">
              {formatTimer(timerSeconds)}
            </div>
            <p className="text-sm text-slate-500">
              {isActive ? (isPaused ? 'Paused' : 'Active') : 'Idle'}
            </p>
            {isActive && sessionId && (
              <p className="text-xs text-slate-400">Session #{sessionId}</p>
            )}
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-700 mb-3">{error}</p>
            <button
              onClick={startSession}
              className="px-4 py-2 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700 transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        <form onSubmit={(e) => e.preventDefault()} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <label className="block text-sm font-medium text-slate-700">Subject</label>
              <select
                value={form.subject}
                onChange={(e) => setForm(prev => ({ ...prev, subject: e.target.value }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                required
              >
                {subjects.map(subject => (
                  <option key={subject} value={subject}>{subject}</option>
                ))}
              </select>
            </div>

            <div className="space-y-3">
              <label className="block text-sm font-medium text-slate-700">Topic (optional)</label>
              <input
                type="text"
                value={form.topic}
                onChange={(e) => setForm(prev => ({ ...prev, topic: e.target.value }))}
                placeholder="e.g., Neural networks, Pandas, Linear algebra"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
              />
            </div>
          </div>

          <div className="space-y-3">
            <label className="block text-sm font-medium text-slate-700">Duration (minutes)</label>
            <input
              type="number"
              value={form.durationMinutes}
              onChange={(e) => setForm(prev => ({ ...prev, durationMinutes: parseInt(e.target.value) || 45 }))}
              min="5"
              max="180"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
            />
          </div>

          <div className="space-y-3">
            <label className="flex items-center gap-3">
              <input
                type="checkbox"
                checked={form.webcamEnabled}
                onChange={(e) => setForm(prev => ({ ...prev, webcamEnabled: e.target.checked }))}
                className="w-4 h-4 text-slate-600"
              />
              <span className="text-sm font-medium text-slate-700">
                Enable webcam monitoring (estimates fatigue locally)
              </span>
            </label>
            <p className="mt-1 text-xs text-slate-500">
              {fatigueDisclaimer}
            </p>
          </div>

          <div className="flex items-center gap-4">
            <Button
              variant="secondary"
              onClick={isActive ? (isPaused ? resumeSession : pauseSession) : startSession}
              disabled={loading}
            >
              {loading ? 'Starting...' : (isActive ? (isPaused ? 'Resume Session' : 'Pause Session') : 'Start Session')}
            </Button>
            <Button
              variant="ghost"
              onClick={endSession}
              disabled={!isActive || loading}
            >
              End Session
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SessionPage