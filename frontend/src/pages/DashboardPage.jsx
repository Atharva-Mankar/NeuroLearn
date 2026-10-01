import { useNavigate } from 'react-router-dom'
import { TrendingUp, Coffee, ChevronRight, Clock } from 'lucide-react'
import { dashboardData } from '../data/demoData'

const DashboardPage = () => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 mb-2">
              Welcome back, {dashboardData.user.name}!
            </h1>
            <p className="text-slate-600">
              Ready for your next focused session?
            </p>
          </div>

          <div className="mt-4 md:mt-0">
            <button
              onClick={() => navigate('/session')}
              className="flex items-center gap-2 px-5 py-3 bg-slate-900 text-white rounded-lg font-medium transition-colors hover:bg-slate-800"
            >
              Start Session
              <ChevronRight size={20} />
            </button>
          </div>
        </div>

        {/* Dashboard Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Weekly Progress */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <TrendingUp size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">
                Weekly Study Progress
              </span>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-2">
                {dashboardData.studyProgress.percentage}%
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2.5 mb-2">
                <div
                  className="bg-slate-900 h-2.5 rounded-full"
                  style={{ width: `${dashboardData.studyProgress.percentage}%` }}
                />
              </div>
              <div className="text-sm text-slate-500">
                {dashboardData.studyProgress.description}
              </div>
            </div>
          </div>

          {/* Fatigue Level */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <Coffee size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">
                {dashboardData.fatigueLevel.label}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className={`text-2xl font-bold ${dashboardData.fatigueLevel.value === 'Low' ? 'text-green-600' :
                  dashboardData.fatigueLevel.value === 'Medium' ? 'text-yellow-600' : 'text-red-600'}
                }`}>{dashboardData.fatigueLevel.level}</span>
                <span className="text-xs text-slate-500">{dashboardData.fatigueLevel.label}</span>
              </div>
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${dashboardData.fatigueLevel.value === 'Low' ? 'bg-green-50 text-green-700' :
                dashboardData.fatigueLevel.value === 'Medium' ? 'bg-yellow-50 text-yellow-700' : 'bg-red-50 text-red-700'}
              `}>{dashboardData.fatigueLevel.level}</div>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-200">
              <p className="text-xs text-slate-500 italic">{dashboardData.fatigueLevel.disclaimer}</p>
            </div>
          </div>

          {/* Today's Stats */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <Clock size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">
                Today's Timeline
              </span>
            </div>

            <div className="space-y-3">
              {dashboardData.timeline.map((item) => (
                <div key={item.time} className="flex items-center gap-3">
                  <span className="text-xs font-medium text-slate-500 w-12">{item.time}</span>
                  <div className="flex-1">
                    <span className="text-xs font-medium text-slate-800">{item.subject}</span>
                    <span className="text-xs text-slate-500 ml-2">{item.duration}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Sessions */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm mb-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Recent Sessions</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {dashboardData.recentSessions.map((session) => (
              <div key={session.subject} className="border border-slate-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-sm font-medium text-slate-800">{session.subject}</span>
                  <span className="text-xs text-slate-500">{session.date}</span>
                </div>
                <div className="text-xs text-slate-600 mb-2">{session.topic}</div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-500">{session.duration}</span>
                  <span className="text-xs px-2 py-1 bg-slate-100 rounded-full">{session.fatigue}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Adaptive Suggestions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Adaptive Suggestions</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {dashboardData.suggestions.map((suggestion) => (
              <div key={suggestion.title} className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
                <div className="flex items-start gap-3">
                  <Coffee size={20} className="text-slate-400 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="text-base font-medium text-slate-900 mb-2">{suggestion.title}</h3>
                    <p className="text-sm text-slate-600">{suggestion.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Calendar Preview */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm mb-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Calendar Preview</h2>
          <div className="grid grid-cols-7 gap-1">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
              <div key={day} className="text-center text-xs font-medium text-slate-600 py-2">{day}</div>
            ))}
            {dashboardData.calendarPreview.map((day) => (
              <div key={day.date} className="h-10 flex items-center justify-center">
                <span className="text-sm text-slate-800">{day.date.split('-')[2]}</span>
                {day.sessions > 0 && (
                  <div className="w-2 h-2 bg-slate-900 rounded-full ml-1" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button
            onClick={() => navigate('/session')}
            className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow flex items-center justify-center"
          >
            <span className="text-sm font-medium text-slate-800">Start Session</span>
          </button>

          <button
            onClick={() => navigate('/calendar')}
            className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow flex items-center justify-center"
          >
            <span className="text-sm font-medium text-slate-800">Add Event</span>
          </button>

          <button
            onClick={() => navigate('/history')}
            className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow flex items-center justify-center"
          >
            <span className="text-sm font-medium text-slate-800">View History</span>
          </button>

          <button
            onClick={() => navigate('/settings')}
            className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow flex items-center justify-center"
          >
            <span className="text-sm font-medium text-slate-800">Settings</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage