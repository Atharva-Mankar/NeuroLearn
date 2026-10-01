import Badge from './Badge'
import { fatigueStyles } from '../../utils/format'

/**
 * FatigueBadge = a Badge that always shows a fatigue level with the right
 * colour. Used in the dashboard, history and insights.
 */
const TONE_BY_LEVEL = {
  Low: 'green',
  Medium: 'yellow',
  High: 'red',
}

const FatigueBadge = ({ level }) => {
  return (
    <Badge tone={TONE_BY_LEVEL[level] || 'slate'}>
      <span className="flex items-center gap-1.5">
        <span
          className={`h-1.5 w-1.5 rounded-full ${
            (fatigueStyles[level] || fatigueStyles.Medium).dot
          }`}
        />
        {level}
      </span>
    </Badge>
  )
}

export default FatigueBadge
