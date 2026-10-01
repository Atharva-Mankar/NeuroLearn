import { BatteryMedium, BatteryLow, BatteryHigh } from 'lucide-react'

/**
 * FatigueCard = one place to show the estimated fatigue value.
 *
 * The FatigueCard is very intentional about NOT calling the output a score,
 * diagnosis, measurement, etc. It is only ever labelled an "estimate" and the
 * disclaimer is always visible nearby.
 */
const ICON_MAP = {
  Low: BatteryLow,
  Medium: BatteryMedium,
  High: BatteryHigh,
}
const FatigueCard = ({ level, value, label, disclaimer }) => {
  const Icon = ICON_MAP[level] || BatteryMedium

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-3 mb-4">
        <Icon size={20} className="text-slate-500" />
        <div>
          <h3 className="text-sm font-medium text-slate-600">{label}</h3>
          <p className="mt-0.5 text-xs text-slate-500">{value}</p>
        </div>
      </div>

      <div className="flex h-2.5 w-full rounded-full bg-slate-200">
        <div
          className={`h-2.5 rounded-full ${level === 'Low' ? 'bg-green-500' :
            level === 'Medium' ? 'bg-yellow-500' : 'bg-red-500'}`}
          style={{ width: `${value}%` }}
        />
      </div>

      <p className="mt-3 text-xs text-slate-500">{disclaimer}</p>
    </section>
  )
}

export default FatigueCard