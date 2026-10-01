import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Navbar from './Navbar'

/**
 * Layout = the shared "frame" around every signed-in page.
 *
 * It provides the left sidebar, the top navbar, and the main content area.
 * Pages are rendered into the content area through <Outlet />, which is how
 * React Router delivers a child route to a parent layout.
 */
const Layout = () => {
  // Tracks whether the sidebar is visible on mobile. On desktop the sidebar
  // is always shown, so this value only matters for small screens.
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <Navbar
          title={document.title || 'NeuroLearn'}
          onMenuClick={() => setIsSidebarOpen(true)}
        />

        <main className="flex-1 px-4 py-6 md:px-8 md:py-8">
          <div className="mx-auto max-w-6xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout
