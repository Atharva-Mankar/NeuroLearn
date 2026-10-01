/**
 * Shared styles for the three fatigue levels.
 * Defined once so the dashboard, history and insights all agree.
 */
export const fatigueStyles = {
  Low: {
    badge: 'bg-green-50 text-green-700',
    bar: 'bg-green-500',
    dot: 'bg-green-500',
  },
  Medium: {
    badge: 'bg-yellow-50 text-yellow-700',
    bar: 'bg-yellow-500',
    dot: 'bg-yellow-500',
  },
  High: {
    badge: 'bg-red-50 text-red-700',
    bar: 'bg-red-500',
    dot: 'bg-red-500',
  },
}
