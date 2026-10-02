import { NavLink, useNavigate } from 'react-router-dom'
import {
  Brain,
  LayoutDashboard,
  PlayCircle,
  CalendarDays,
  History,
  BarChart3,
  Settings,
  LogOut,
} from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'

/**
 * The list of pages in the left sidebar.
 * Adding a new page to the app means adding one line here.
 */
const NAV_ITEMS = [
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Study Session', to: '/session', icon: PlayCircle },
  { label: 'Calendar', to: '/calendar', icon: CalendarDays },
  { label: 'History', to: '/history', icon: History },
  { label: 'Insights', to: '/insights', icon: BarChart3 },
  { label: 'Settings', to: '/settings', icon: Settings },
]

/**
 * Sidebar = the vertical menu shown on the left of every signed-in page.
 *
 * On desktop it is always visible.
 * On mobile it slides in and out. `isOpen` and `onClose` are controlled by
 * the parent Layout so the Navbar can open and close it.
 */
const Sidebar = ({ isOpen, onClose }) => {
  const { logout } = useAuth()
  const navigate = useNavigate()

  // Clears the stored user object and returns to the login page.
  const handleLogout = () => {
    logout()
    onClose()
    navigate('/login')
  }

  return (
    <>
      {/* On mobile, a dark overlay appears behind the sidebar so it is clear
          that the rest of the page is not usable while the menu is open. */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-30 bg-slate-900/50 md:hidden"
          aria-hidden="true"
        />
      )}

      <aside
        className={`
          fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-200 bg-slate-50
          transition-transform duration-200 ease-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          md:static md:translate-x-0
        `}
      >
        {/* Brand */}
        <div className="flex items-center gap-2.5 border-b border-slate-200 px-5 py-4">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900">
            <Brain size={18} className="text-white" />
          </span>
          <span className="text-base font-semibold tracking-tight text-slate-900">
            NeuroLearn
          </span>
        </div>

        {/* Navigation links */}
        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          {NAV_ITEMS.map(({ label, to, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-slate-900 text-white'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`
              }
            >
              <Icon size={18} className="shrink-0" />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Logout + version */}
        <div className="border-t border-slate-200 p-3">
          {/* Signs out of the frontend auth state and returns to /login. This is
              not backend session logout — no token or session exists yet. */}
          <button
            type="button"
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-900"
          >
            <LogOut size={18} className="shrink-0" />
            Logout
          </button>
          <p className="px-3 pt-2 text-xs text-slate-400">v0.1.0</p>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
