import { Menu, CalendarDays, PlayCircle } from 'lucide-react'
import { Link } from 'react-router-dom'
import { demoUser } from '../../data/demoData'

/**
 * Navbar = the thin bar across the top of every signed-in page.
 *
 * It holds the mobile menu button, a short page title, and a small avatar.
 */
const Navbar = ({ title, onMenuClick }) => {
  // "Atharva" -> "A". This is only a placeholder until a real profile picture
  // comes from the backend.
  const initials = demoUser.name.charAt(0).toUpperCase()

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-slate-200 bg-white/80 px-4 backdrop-blur md:px-8">
      {/* Only shown on small screens; the sidebar is always visible on desktop. */}
      <button
        type="button"
        onClick={onMenuClick}
        className="-ml-1 rounded-lg p-2 text-slate-600 transition-colors hover:bg-slate-100 md:hidden"
        aria-label="Open navigation menu"
      >
        <Menu size={20} />
      </button>

      <h1 className="flex-1 truncate text-base font-semibold text-slate-900">
        {title}
      </h1>

      {/* Two shortcuts for the pages a student uses most. */}
      <Link
        to="/calendar"
        className="hidden items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 sm:flex"
      >
        <CalendarDays size={18} />
        Calendar
      </Link>

      <Link
        to="/session"
        className="flex items-center gap-2 rounded-lg bg-slate-900 px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-slate-700"
      >
        <PlayCircle size={18} />
        <span className="hidden sm:inline">Start Session</span>
      </Link>

      <span
        className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-slate-200 text-sm font-semibold text-slate-700"
        title={demoUser.email}
      >
        {initials}
      </span>
    </header>
  )
}

export default Navbar
