import { ChevronLeft, ChevronRight } from 'lucide-react'

const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

// Resolved once at module scope so rendering stays pure and stable across re-renders
const today = new Date()
const currentMonth = today.getMonth()
const currentYear = today.getFullYear()
const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate()
const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay()

const Calendar = ({ previewData }) => {
  const getDayData = (day) => {
    const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const dayData = previewData.find(d => d.date === dateStr)
    return dayData || { sessions: 0, totalMinutes: 0 }
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-slate-900">
          {new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long', year: 'numeric' })}
        </h2>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => {/* Previous month - future implementation */}}
            className="p-2 rounded hover:bg-slate-100 text-slate-500"
          >
            <ChevronLeft size={20} />
          </button>
          <button
            type="button"
            onClick={() => {/* Next month - future implementation */}}
            className="p-2 rounded hover:bg-slate-100 text-slate-500"
          >
            <ChevronRight size={20} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-2 text-xs text-center">
        {DAYS.map((day) => (
          <div key={day} className="font-medium text-slate-600">{day}</div>
        ))}
      </div>

      <div className="grid grid-cols-7 gap-2">
        {/* Empty cells for days before month start */}
        {Array(firstDayIndex).fill(null).map((_, i) => (
          <div key={`empty-${i}`} className="h-10" />
        ))}

        {/* Days of the month */}
        {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => {
          const data = getDayData(day)
          const hasActivity = data.sessions > 0
          return (
            <div key={day} className={`
              min-h-10 flex flex-col items-center justify-center rounded-md
              ${hasActivity ? 'bg-slate-50 hover:bg-slate-100' : 'hover:bg-slate-50'}
              transition-colors cursor-pointer
            `}>
              <div className="text-xs font-medium text-slate-800">{day}</div>
              {hasActivity && (
                <div className="flex items-center gap-1 mt-1 text-xs">
                  <div className="w-2 h-2 bg-slate-600 rounded-full" />
                  <span className="text-slate-600">{data.sessions}</span>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Calendar