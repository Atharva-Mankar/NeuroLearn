import { CheckCircle } from 'lucide-react'

const ProgressCard = ({ title, value, description }) => {
  const percentage = typeof value === 'number' ? value : parseInt(value) || 0

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm transition-all duration-200 hover:shadow-md">
      <div className="mb-3">
        <h3 className="text-sm font-medium text-slate-600">{title}</h3>
        {description && (
          <p className="text-xs text-slate-500 mt-1">{description}</p>
        )}
      </div>

      <div className="w-full bg-slate-100 rounded-full h-2.5 mb-3">
        <div
          className={`bg-slate-900 h-2.5 rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>

      <div className="flex justify-between text-xs text-slate-500">
        <span>0%</span>
        <span>{percentage}%</span>
      </div>

      {percentage >= 100 && (
        <CheckCircle size={16} className="ml-2 text-green-500" />
      )}
    </div>
  )
}

export default ProgressCard