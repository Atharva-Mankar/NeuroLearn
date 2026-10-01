/**
 * Small formatting helpers shared by several pages.
 *
 * Keeping them here means the date and time formats stay the same everywhere,
 * instead of each page inventing its own version.
 */

/** "2024-09-28" -> "28 Sep 2024" */
export const formatDate = (isoDate) => {
  const date = new Date(`${isoDate}T00:00:00`)
  return date.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

/** "2024-09-28" -> "Sat, 28 Sep" */
export const formatDayShort = (isoDate) => {
  const date = new Date(`${isoDate}T00:00:00`)
  return date.toLocaleDateString('en-GB', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
  })
}

/** "19:00" -> "7:00 PM" */
export const formatTime12 = (time24) => {
  const [hours, minutes] = time24.split(':').map(Number)
  const period = hours >= 12 ? 'PM' : 'AM'
  const hours12 = hours % 12 === 0 ? 12 : hours % 12
  return `${hours12}:${String(minutes).padStart(2, '0')} ${period}`
}

/** 90 -> "1h 30m" */
export const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const rest = minutes % 60
  if (hours === 0) return `${rest}m`
  if (rest === 0) return `${hours}h`
  return `${hours}h ${rest}m`
}

/** Seconds -> "00:00:00" (HH:MM:SS) */
export const formatTimer = (totalSeconds) => {
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60
  return [hours, minutes, seconds]
    .map((n) => String(n).padStart(2, '0'))
    .join(':')
}

/**
 * Shared colours for the three fatigue levels.
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
