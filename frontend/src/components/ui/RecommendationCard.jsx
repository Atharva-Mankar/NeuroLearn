import { Coffee, Clock, Target, TrendingUp } from 'lucide-react'

const ICON_MAP = {
  Coffee: Coffee,
  Clock: Clock,
  Target: Target,
  TrendingUp: TrendingUp,
}

const RecommendationCard = ({ title, description, icon }) => {
  const Icon = ICON_MAP[icon] || TrendingUp

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm transition-all duration-200 hover:shadow-md">
      <div className="flex items-start gap-3 mb-4">
        <Icon size={24} className="mt-1 text-slate-400 flex-shrink-0" />
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <p className="text-sm text-slate-600 mt-1">{description}</p>
        </div>
      </div>
    </div>
  )
}

export default RecommendationCard