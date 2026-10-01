import { TrendingUp } from 'lucide-react'

const StatCard = ({ title, value, description, icon }) => {
  const Icon = icon || TrendingUp

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-3 mb-4">
        <Icon size={20} className="text-slate-400" />
        <div>
          <h3 className="text-sm font-medium text-slate-600">{title}</h3>
          {description && <p className="mt-0.5 text-xs text-slate-500">{description}</p>}
        </div>
      </div>
      <div className="text-2xl font-bold text-slate-900">{value}</div>
    </div>
  )
}

export default StatCard