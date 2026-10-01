import { Calendar } from 'lucide-react'

const Timeline = ({ items }) => {
  return (
    <div className="space-y-6">
      {items.map(item => (
        <div key={item.time} className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Calendar size={24} className="text-slate-400" />
            <p className="text-sm text-slate-500 font-medium">
              {item.time}
            </p>
          </div>
          <div className="flex-1">
            <p className="text-sm text-slate-600">{item.subject}</p>
            <p className="text-xs text-slate-500">{item.duration}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

export default Timeline