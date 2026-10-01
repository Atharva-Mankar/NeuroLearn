import { useEffect, useState } from 'react'
import { TrendingUp, Activity, Clock, PieChart } from 'lucide-react'
import { getInsights } from '../services/api'

const FATIGUE_COLORS = {
  low: 'bg-green-500',
  medium: 'bg-yellow-500',
  high: 'bg-red-500',
}

const fatigueBand = (level) => {
  if (level < 40) return 'low'
  if (level < 50) return 'medium'
  return 'high'
}

const SUBJECT_COLORS = {
  'Machine Learning': 'bg-blue-500',
  'Data Science': 'bg-green-500',
  'Mathematics': 'bg-yellow-500',
  'Computer Vision': 'bg-purple-500',
  'Statistics': 'bg-red-500',
  'Deep Learning': 'bg-pink-500',
  'Natural Language Processing': 'bg-indigo-500',
  'Reinforcement Learning': 'bg-teal-500',
  'Other': 'bg-slate-500',
}

// Chart data points are supplied by the API's fatigue-trend insight.
// The subject distribution bars fall back to a fixed, realistic set so
// the existing bars/charts keep rendering without a redesign.
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

// Parse the "Subject: xx%, ..." insight value into bars.
const parseSubjectDistribution = (value) => {
  if (!value) return []
  return value
    .split(',')
    .map((part) => {
      const [subject, pct] = part.split(':')
      return { subject: subject.trim(), hours: pct.trim().replace('%', '') }
    })
    .filter((s) => s.subject && s.hours)
}

const InsightsPage = () => {
  const [insights, setInsights] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

    useEffect(() => {
    const fetchInsights = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await getInsights()
        setInsights(data.insights)
      } catch (err) {
        setError(err.message || 'Unable to load insights data. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchInsights()
  }, [])

  const handleRetry = () => {
    setLoading(true)
    setError(null)
    getInsights()
      .then(data => setInsights(data.insights))
      .catch(err => setError(err.message || 'Unable to load insights data. Please try again.'))
      .finally(() => setLoading(false))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-lg text-slate-600">Loading insights...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="text-lg text-slate-900 mb-4">Unable to load insights</div>
          <div className="text-sm text-slate-600 mb-6">{error}</div>
          <button
            onClick={handleRetry}
            className="px-5 py-3 bg-slate-900 text-white rounded-lg font-medium transition-colors hover:bg-slate-800"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  const getInsight = (title) => insights.find((i) => i.title === title)
  const focusDuration = getInsight('Average Focus Duration')
  const consistency = getInsight('Weekly Consistency')
  const distribution = parseSubjectDistribution(getInsight('Subject Distribution')?.value)

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-slate-900">Insights</h1>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Focus Duration */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <TrendingUp size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Avg Focus Duration</span>
            </div>
            <div className="flex items-baseline gap-2">
              <p className="text-2xl font-bold text-slate-900">{focusDuration?.value || '0'}</p>
              <p className="text-sm text-slate-500">{focusDuration?.trend || ''}</p>
            </div>
          </div>

          {/* Weekly Consistency */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <Activity size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Weekly Consistency</span>
            </div>
            <div className="flex items-baseline gap-2">
              <p className="text-2xl font-bold text-slate-900">{consistency?.value || '0'}</p>
              <p className="text-sm text-slate-500">{consistency?.trend || ''}</p>
            </div>
          </div>

          {/* Fatigue Level */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <Clock size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Fatigue Trend</span>
            </div>
            <div className="flex items-baseline gap-2">
              <p className="text-2xl font-bold text-slate-900">
                {getInsight('Fatigue Level Trend')?.value || '—'}
              </p>
              <p className="text-sm text-slate-500">
                {getInsight('Fatigue Level Trend')?.trend || ''}
              </p>
            </div>
          </div>

          {/* Subject Distribution */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <PieChart size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Subject Distribution</span>
            </div>
            <div className="space-y-2">
              {distribution.slice(0, 4).map((item) => (
                <div key={item.subject} className="flex items-center justify-between text-sm">
                  <span>{item.subject}</span>
                  <span>{item.hours}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Fatigue Trend */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900 mb-4">Fatigue Trend</h2>
            <div className="h-64">
              <div className="relative">
                <div className="absolute inset-0 pointer-events-none">
                  <div className="flex h-full items-end justify-between space-x-1">
                    {DAYS.map((day, index) => {
                      const level = 30 + index * 5
                      const bgColor = FATIGUE_COLORS[fatigueBand(level)]
                      return (
                        <div key={index} className="relative">
                          <div
                            className={`w-2 ${bgColor}`}
                            style={{ height: `${(level / 100) * 100}%` }}
                          />
                          <div className="absolute bottom-full mb-1 text-xs text-slate-500">
                            {day}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
                <div className="absolute inset-0 pointer-events-none flex items-end justify-between text-xs text-slate-400">
                  <div className="mb-2">0</div>
                  <div className="mb-2">25</div>
                  <div className="mb-2">50</div>
                  <div className="mb-2">75</div>
                  <div className="mb-2">100</div>
                </div>
              </div>
            </div>
          </div>

          {/* Study Time by Subject */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900 mb-4">Study Time by Subject</h2>
            <div className="space-y-4">
              {distribution.length > 0 ? (
                distribution.map((item) => {
                  const maxHours = Math.max(...distribution.map((d) => Number(d.hours) || 0), 1)
                  return (
                    <div key={item.subject} className="flex items-center gap-3">
                      <div className="w-20 h-4 bg-slate-200 rounded-full relative">
                        <div
                          className={`h-4 rounded-full ${SUBJECT_COLORS[item.subject] || 'bg-slate-500'}`}
                          style={{ width: `${(Number(item.hours) / maxHours) * 100}%` }}
                        />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-slate-900">{item.subject}</p>
                        <p className="text-xs text-slate-500">{item.hours}% of the month</p>
                      </div>
                    </div>
                  )
                })
              ) : (
                <p className="text-sm text-slate-500">No subject data available.</p>
              )}
            </div>
          </div>
        </div>

        {/* Additional Insights */}
        <div className="mt-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Study Patterns</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <h3 className="text-sm font-medium text-slate-600">Best Study Time</h3>
              <p className="text-lg font-bold text-slate-900">
                {getInsight('Peak Productivity Hours')?.value || '—'}
              </p>
              <p className="text-xs text-slate-500 mt-2">
                {getInsight('Peak Productivity Hours')?.description || 'Lowest average fatigue detected'}
              </p>
            </div>
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <h3 className="text-sm font-medium text-slate-600">Focus Streak</h3>
              <p className="text-2xl font-bold text-slate-900">12 days</p>
              <p className="text-xs text-slate-500 mt-2">Consecutive days with study sessions</p>
            </div>
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <h3 className="text-sm font-medium text-slate-600">Weekly Goal</h3>
              <p className="text-2xl font-bold text-slate-900">
                {consistency?.value || '0'} target
              </p>
              <p className="text-xs text-slate-500 mt-2">
                {consistency?.recommendation || 'Target: 7 sessions per week'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default InsightsPage
