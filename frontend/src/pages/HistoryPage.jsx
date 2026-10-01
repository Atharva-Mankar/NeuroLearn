import { useState, useEffect } from 'react'
import { Search } from 'lucide-react'
import { getHistory } from '../services/api'

// Resolved once at module scope so rendering stays pure and stable across re-renders
const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)

const HistoryPage = () => {
  const [sessions, setSessions] = useState([])
  const [filters, setFilters] = useState({
    subject: 'all',
    fatigue: 'all',
    status: 'all',
    search: '',
    sort: 'date-desc'
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch history data from API
  useEffect(() => {
    const fetchHistoryData = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await getHistory()
        setSessions(response.sessions)
      } catch (err) {
        setError(err.message || 'Unable to load history data. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchHistoryData()
  }, [])

  const filteredSessions = sessions.filter(session => {
    // Subject filter
    if (filters.subject !== 'all' && session.subject !== filters.subject) return false

    // Fatigue filter
    if (filters.fatigue !== 'all' && session.fatigue !== filters.fatigue) return false

    // Status filter
    if (filters.status !== 'all' && session.status !== filters.status) return false

    // Search filter
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase()
      return session.subject.toLowerCase().includes(searchTerm) ||
             session.topic.toLowerCase().includes(searchTerm)
    }

    return true
  }).sort((a, b) => {
    if (filters.sort === 'date-asc') return new Date(a.date).getTime() - new Date(b.date).getTime()
    if (filters.sort === 'duration-asc') return a.duration - b.duration
    if (filters.sort === 'duration-desc') return b.duration - a.duration
    // Default: date descending
    return new Date(b.date).getTime() - new Date(a.date).getTime()
  })

  const handleFilterChange = (filter, value) => {
    setFilters(prev => ({ ...prev, [filter]: value }))
  }

  const handleDeleteSession = (id) => {
    setSessions(prev => prev.filter(session => session.id !== id))
  }

  const handleRetry = () => {
    setLoading(true)
    setError(null)
    getHistory()
      .then(response => setSessions(response.sessions))
      .catch(err => setError(err.message || 'Unable to load history data. Please try again.'))
      .finally(() => setLoading(false))
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-lg text-slate-600">Loading history...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="text-lg text-slate-900 mb-4">Unable to load history</div>
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

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-slate-900">Study History</h1>
          <button
            onClick={() => handleFilterChange('search', '')}
            className="flex items-center gap-2 px-4 py-2 bg-slate-100 rounded-lg hover:bg-slate-200 transition-colors"
          >
            <Search size={20} />
            <span>Clear Filters</span>
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Subject</label>
              <select
                value={filters.subject}
                onChange={(e) => handleFilterChange('subject', e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
              >
                <option value="all">All Subjects</option>
                {[...new Set(sessions.map(s => s.subject))].map((subject) => (
                  <option key={subject} value={subject}>{subject}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Fatigue Level</label>
              <select
                value={filters.fatigue}
                onChange={(e) => handleFilterChange('fatigue', e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
              >
                <option value="all">All Levels</option>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Status</label>
              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
              >
                <option value="all">All Statuses</option>
                <option value="completed">Completed</option>
                <option value="in-progress">In Progress</option>
                <option value="paused">Paused</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Sort By</label>
              <select
                value={filters.sort}
                onChange={(e) => handleFilterChange('sort', e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
              >
                <option value="date-desc">Date (Newest)</option>
                <option value="date-asc">Date (Oldest)</option>
                <option value="duration-asc">Duration (Shortest)</option>
                <option value="duration-desc">Duration (Longest)</option>
              </select>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <input
              type="text"
              placeholder="Search sessions..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              className="flex-1 px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
            />
            <button
              onClick={() => handleFilterChange('search', '')}
              className="px-3 py-2 border border-slate-300 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Stats Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600">Total Sessions</h3>
            <p className="text-2xl font-bold text-slate-900">{sessions.length}</p>
          </div>
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600">This Week</h3>
            <p className="text-2xl font-bold text-slate-900">{sessions.filter(s => new Date(s.date).getTime() >= oneWeekAgo).length}</p>
          </div>
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600">Avg Duration</h3>
            <p className="text-2xl font-bold text-slate-900">
              {sessions.length > 0
                ? Math.round(sessions.reduce((sum, s) => sum + s.duration, 0) / sessions.length)
                : 0} min
            </p>
          </div>
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600">Completion Rate</h3>
            <p className="text-2xl font-bold text-slate-900">
              {Math.round((sessions.filter(s => s.status === 'completed').length / sessions.length) * 100)}%
            </p>
          </div>
        </div>

        {/* Sessions List */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          {filteredSessions.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-slate-500">No sessions found matching your filters.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredSessions.map((session) => (
                <div key={session.id} className="border-t border-slate-200 pt-4">
                  <div className="flex items-center gap-4">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-900">{session.subject}</p>
                      <p className="text-xs text-slate-500">{session.topic}</p>
                    </div>

                    <div className="flex items-center gap-3 text-xs">
                      <span>{session.duration} min</span>
                      <span className={`px-2 py-1 rounded-full ${session.fatigue === 'Low' ? 'bg-green-50 text-green-800' :
  session.fatigue === 'Medium' ? 'bg-yellow-50 text-yellow-800' : 'bg-red-50 text-red-800'}`}>{session.fatigue}</span>
                      <span className="px-2 py-1 rounded-full bg-slate-100 text-slate-600">{formatDate(session.date)}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 rounded-full ${session.status === 'completed' ? 'bg-green-50 text-green-800' :
  session.status === 'in-progress' ? 'bg-blue-50 text-blue-800' :
  session.status === 'paused' ? 'bg-yellow-50 text-yellow-800' : 'bg-red-50 text-red-800'}`}>{session.status}</span>
                      <button
                        onClick={() => handleDeleteSession(session.id)}
                        className="p-1 rounded hover:bg-slate-200 text-slate-400 hover:text-slate-600"
                        aria-label="Delete session"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                      </button>
                    </div>
                  </div>
                  {session.id !== filteredSessions[filteredSessions.length - 1].id && (
                    <div className="mt-3 pt-3 border-t border-slate-200">
                      <p className="text-xs text-slate-400">Session completed • {formatDate(session.date)}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default HistoryPage