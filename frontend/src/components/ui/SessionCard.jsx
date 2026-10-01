import { PlayCircle } from 'lucide-react'

const SessionCard = ({ session }) => {
  const statusMap = {
    completed: 'Completed',
    'in-progress': 'In Progress',
    paused: 'Paused',
    cancelled: 'Cancelled',
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm transition-all duration-200 hover:shadow-md">
      <div className="flex items-center gap-4 mb-4">
        <PlayCircle size={20} className="text-slate-400" />
        <div className="flex-1">
          <p className="text-sm font-medium text-slate-800">{session.subject}</p>
          <p className="text-xs text-slate-500">{session.topic}</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="px-2 py-1 bg-slate-100 rounded-full text-xs text-slate-600">{session.duration}</span>
          <span className="px-2 py-1 bg-slate-50 rounded-full text-xs text-slate-600">{session.fatigue}</span>
          <span className="px-2 py-1 bg-slate-100 rounded-full text-xs text-slate-600">{session.date}</span>
        </div>
        <span className="text-xs font-medium text-slate-800">{statusMap[session.status]}</span>
      </div>
      <div className="mt-4 pt-3 border-t border-slate-200">
        <span className="text-sm text-slate-500">{session.date}</span>
      </div>
    </div>
  )
}

export default SessionCard