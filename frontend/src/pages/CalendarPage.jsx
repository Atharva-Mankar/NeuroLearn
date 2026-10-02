import { useState, useEffect } from 'react'
import { Plus } from 'lucide-react'
import { getCalendar } from '../services/api'

// Resolved once at module scope so rendering stays pure and stable across
// re-renders — the calendar grid and the "today" filter must agree.
const today = new Date()

const CalendarPage = () => {
  const [currentMonth, setCurrentMonth] = useState(today.getMonth())
  const [currentYear, setCurrentYear] = useState(today.getFullYear())
  // Removed unused date selection state (modal now disabled)
  const [showAddModal, setShowAddModal] = useState(false)
  const [calendarDays, setCalendarDays] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch calendar data from API
  useEffect(() => {
    const fetchCalendarData = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await getCalendar(currentMonth + 1, currentYear) // API expects 1-12
        setCalendarDays(response.days)
      } catch (err) {
        setError(err.message || 'Unable to load calendar data. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchCalendarData()
  }, [currentMonth, currentYear])

  const handlePreviousMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11)
      setCurrentYear(prev => prev - 1)
    } else {
      setCurrentMonth(prev => prev - 1)
    }
  }

  const handleNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0)
      setCurrentYear(prev => prev + 1)
    } else {
      setCurrentMonth(prev => prev + 1)
    }
  }

  const handleRetry = () => {
    setLoading(true)
    setError(null)
    getCalendar(currentMonth + 1, currentYear)
      .then(response => setCalendarDays(response.days))
      .catch(err => setError(err.message || 'Unable to load calendar data. Please try again.'))
      .finally(() => setLoading(false))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-lg text-slate-600">Loading calendar...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="text-lg text-slate-900 mb-4">Unable to load calendar</div>
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

  const handleAddEvent = () => {
    setShowAddModal(true)
  }

  const handleCloseModal = () => {
    setShowAddModal(false)
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-slate-900">Calendar</h1>
          <div className="flex items-center gap-3">
            <button
              onClick={handleAddEvent}
              className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg font-medium hover:bg-slate-800 transition-colors"
            >
              <Plus size={20} />
              <span>Add Study Task</span>
            </button>
          </div>
        </div>

        {/* Event Modal - Marked as unavailable */}
        {showAddModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-8 w-full max-w-md space-y-6">
              <h2 className="text-xl font-bold text-slate-900">Add Study Task</h2>
              <div className="bg-slate-50 p-6 rounded">
                <p className="text-sm text-slate-600">
                  Study task scheduling is not yet implemented in this version.
                  The calendar displays real study sessions from your history,
                  but manual session creation will be available in a future update.
                </p>
              </div>
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Calendar Grid */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-slate-900">
              {new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long', year: 'numeric' })}
            </h2>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handlePreviousMonth}
                className="p-2 rounded hover:bg-slate-100 text-slate-500"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
              </button>
              <button
                type="button"
                onClick={handleNextMonth}
                className="p-2 rounded hover:bg-slate-100 text-slate-500"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </button>
            </div>
          </div>

          <div className="grid grid-cols-7 gap-2 text-xs text-center mb-4">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
              <div key={day} className="font-medium text-slate-600">{day}</div>
            ))}
          </div>

          <div className="grid grid-cols-7 gap-2">
            {/* Calculate first day index and days in month */}
            {(() => {
              const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay();
              const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

              // Empty cells for days before month start
              const emptyCells = Array(firstDayIndex).fill(null).map((_, i) => (
                <div key={`empty-${i}`} className="h-12" />
              ));

              // Days of the month
              const dayCells = Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => {
                const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                // Find matching day from API data
                const apiDay = calendarDays.find(d => d.date === dateStr);
                const hasEvents = apiDay && apiDay.sessions > 0;
                const totalMinutes = apiDay ? apiDay.total_duration : 0;

                return (
                  <div key={dateStr} className={`
                    min-h-12 flex flex-col items-center justify-center rounded-md
                    ${hasEvents ? 'bg-slate-50 hover:bg-slate-100' : 'hover:bg-slate-50'}
                    transition-colors cursor-pointer relative
                  `}>
                    <div className="text-xs font-medium text-slate-800">{day}</div>
                    {hasEvents && (
                      <div className="flex items-center gap-1 mt-1 text-xs">
                        <div className="w-2 h-2 bg-slate-600 rounded-full" />
                        <span className="text-slate-600">${apiDay.sessions}</span>
                      </div>
                    )}
                    {totalMinutes > 0 && (
                      <div className="mt-1 text-xs text-slate-500">
                        {totalMinutes} min
                      </div>
                    )}
                  </div>
                );
              });

              return [...emptyCells, ...dayCells];
            })()}
          </div>
        </div>

        {/* Events List */}
        <div className="mt-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Today's Sessions</h2>
          <div className="space-y-4">
            {calendarDays
              .filter(day => {
                const dayDate = new Date(day.date)
                return dayDate.toDateString() === today.toDateString()
              })
              .map((day) => (
                <div key={day.date} className="flex items-center gap-3 px-4 py-3 bg-slate-50 rounded-lg">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-900">
                      Study Session
                    </p>
                    {day.subjects.length > 0 && (
                      <p className="text-xs text-slate-500">
                        {day.subjects.join(', ')}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-600">
                    <span>{day.sessions} session{(day.sessions !== 1 && 's')}</span>
                    <span>{day.total_duration} min</span>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default CalendarPage