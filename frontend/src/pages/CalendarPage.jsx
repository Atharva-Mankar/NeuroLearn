import { useState } from 'react'
import { Plus } from 'lucide-react'
import { calendarEvents } from '../data/demoData'

// Resolved once at module scope so rendering stays pure and stable across
// re-renders — the calendar grid and the "today" filter must agree.
const today = new Date()
const currentMonth = today.getMonth()
const currentYear = today.getFullYear()
const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate()
const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay()

const CalendarPage = () => {
  const [selectedDate, setSelectedDate] = useState(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [events, setEvents] = useState(calendarEvents)

  const getEventsForDate = (date) => {
    return events.filter(event => event.date === date)
  }

  const handleAddEvent = () => {
    setShowAddModal(true)
  }

  const handleCloseModal = () => {
    setShowAddModal(false)
  }

  const handleDeleteEvent = (id) => {
    setEvents(prev => prev.filter(event => event.id !== id))
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

        {/* Event Modal */}
        {showAddModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-8 w-full max-w-md space-y-6">
              <h2 className="text-xl font-bold text-slate-900">Add Study Task</h2>
              <form className="space-y-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-slate-700">Subject</label>
                  <select className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500">
                    <option value="">Select subject</option>
                    <option value="Machine Learning">Machine Learning</option>
                    <option value="Data Science">Data Science</option>
                    <option value="Mathematics">Mathematics</option>
                    <option value="Computer Vision">Computer Vision</option>
                    <option value="Statistics">Statistics</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-slate-700">Date</label>
                  <input
                    type="date"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                    value={selectedDate || ''}
                    onChange={(e) => setSelectedDate(e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-slate-700">Start Time</label>
                  <input
                    type="time"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                  />
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-slate-700">End Time</label>
                  <input
                    type="time"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-500"
                  />
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={handleCloseModal}
                    className="px-4 py-2 border border-slate-300 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={handleCloseModal}
                    className="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors"
                  >
                    Save Task
                  </button>
                </div>
              </form>
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
                onClick={() => {/* Previous month - placeholder */}}
                className="p-2 rounded hover:bg-slate-100 text-slate-500"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
              </button>
              <button
                type="button"
                onClick={() => {/* Next month - placeholder */}}
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
            {/* Empty cells for days before month start */}
            {Array(firstDayIndex).fill(null).map((_, i) => (
              <div key={`empty-${i}`} className="h-12" />
            ))}

            {/* Days of the month */}
            {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => {
              const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
              const dayEvents = getEventsForDate(dateStr)
              const hasEvents = dayEvents.length > 0
              const totalMinutes = dayEvents.reduce((sum, event) => {
                const start = event.startTime.split(':').map(Number)
                const end = event.endTime.split(':').map(Number)
                const duration = (end[0] * 60 + end[1]) - (start[0] * 60 + start[1])
                return sum + duration
              }, 0)

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
                      <span className="text-slate-600">{dayEvents.length}</span>
                    </div>
                  )}
                  {totalMinutes > 0 && (
                    <div className="mt-1 text-xs text-slate-500">
                      {totalMinutes} min
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Events List */}
        <div className="mt-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Today's Events</h2>
          <div className="space-y-4">
            {events
              .filter(event => {
                const eventDate = new Date(event.date)
                return eventDate.toDateString() === today.toDateString()
              })
              .map((event) => (
                <div key={event.id} className="flex items-center gap-3 px-4 py-3 bg-slate-50 rounded-lg">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-900">{event.title}</p>
                    <p className="text-xs text-slate-500">{event.title}</p>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-600">
                    <span>{event.startTime} - {event.endTime}</span>
                  </div>
                  <button
                    onClick={() => handleDeleteEvent(event.id)}
                    className="p-1 rounded hover:bg-slate-200 text-slate-400 hover:text-slate-600"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default CalendarPage