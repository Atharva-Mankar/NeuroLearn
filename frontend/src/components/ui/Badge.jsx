/**
 * Badge = a small coloured pill, used for fatigue levels and session status.
 */
const TONE_CLASSES = {
  slate: 'bg-slate-100 text-slate-700',
  green: 'bg-green-50 text-green-700',
  yellow: 'bg-yellow-50 text-yellow-700',
  red: 'bg-red-50 text-red-700',
  blue: 'bg-blue-50 text-blue-700',
}

const Badge = ({ tone = 'slate', children }) => {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
        TONE_CLASSES[tone] || TONE_CLASSES.slate
      }`}
    >
      {children}
    </span>
  )
}

export default Badge
