/**
 * API communication layer for the NeuroLearn frontend.
 *
 * All backend requests go through this service so the base URL and error
 * handling stay consistent. Uses the browser's native fetch API.
 */

import { STORAGE_KEY } from '../context/authContextObject'

// Backend base URL - update this when deploying to production
const API_BASE_URL = 'http://127.0.0.1:8000'

// Get current user ID from localStorage (temporary identity mechanism)
function getCurrentUserId() {
  const storedUser = localStorage.getItem(STORAGE_KEY);
  if (storedUser) {
    try {
      const parsed = JSON.parse(storedUser);
      return parsed.id;
    } catch (err) {
      console.warn('Failed to parse auth data from localStorage', err);
      return null;
    }
  }
  return null;
}

/**
 * Generic request helper that handles errors and JSON parsing.
 *
 * @param {string} endpoint - API endpoint (e.g., '/health', '/sessions')
 * @param {object} options - fetch options (method, headers, body, etc.)
 * @returns {Promise<any>} - Parsed JSON response
 * @throws {Error} - On network or HTTP errors
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`

  // Merge caller-supplied headers with the default Content-Type, then apply the
  // temporary identity header LAST so that caller options can never accidentally
  // overwrite it. (Previously `...options` was spread after `headers`, which let
  // options.headers clobber X-User-Id.)
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  const userId = getCurrentUserId()
  if (userId && !endpoint.startsWith('/api/auth/')) {
    headers['X-User-Id'] = userId
  }

  // Strip `headers` out of options so the merged headers above are the only
  // source of truth for the fetch call.
  const { headers: _callerHeaders, ...fetchOptions } = options

  try {
    const response = await fetch(url, {
      headers,
      ...fetchOptions,
    })

    // Check if the response is successful (status 200-299)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`
      )
    }

    // Parse and return JSON
    return await response.json()
  } catch (error) {
    // Network errors (no response) or parsing errors
    if (error instanceof TypeError) {
      throw new Error('Network error: Cannot reach the backend server')
    }
    // Re-throw other errors (HTTP errors)
    throw error
  }
}

/**
 * Health check endpoint.
 *
 * @returns {Promise<{status: string, project: string, version: string}>}
 */
export async function getHealth() {
  return request('/health')
}

/**
 * Dashboard endpoint.
 *
 * @returns {Promise<DashboardResponse>} - Dashboard data for the current user
 */
export async function getDashboard() {
  return request('/api/dashboard')
}

/**
 * Create a new study session.
 *
 * @param {Object} sessionData - Session configuration
 * @param {string} sessionData.subject - Subject of study
 * @param {string} sessionData.topic - Topic being studied
 * @param {number} sessionData.durationMinutes - Duration in minutes
 * @param {boolean} sessionData.webcamEnabled - Enable webcam monitoring
 * @returns {Promise<CreateSessionResponse>} - Created session data
 */
export async function createSession(sessionData) {
  return request('/api/sessions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(sessionData),
  })
}

/**
 * Mark a study session as completed.
 *
 * Updates the existing record in place rather than creating a new one.
 *
 * @param {number} sessionId - The ID of the session to complete
 * @returns {Promise<CreateSessionResponse>} - Updated session data
 */
export async function completeSession(sessionId) {
  return request(`/api/sessions/${sessionId}/complete`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

/**
 * Calendar endpoint.
 *
 * @param {number} [month] - Month (1-12, defaults to current month)
 * @param {number} [year] - Year (defaults to current year)
 * @returns {Promise<CalendarResponse>} - Calendar data
 */
export async function getCalendar(month, year) {
  // If month/year not provided, use current month/year
  if (month === undefined || year === undefined) {
    const now = new Date()
    month = month === undefined ? now.getMonth() + 1 : month // API expects 1-12
    year = year === undefined ? now.getFullYear() : year
  }
  return request(`/api/calendar?month=${month}&year=${year}`)
}

/**
 * History endpoint.
 *
 * @returns {Promise<HistoryResponse>} - Study session history data
 */
export async function getHistory() {
  return request('/api/history')
}

/**
 * Insights endpoint.
 *
 * @returns {Promise<InsightResponse>} - Insight data
 */
export async function getInsights() {
  return request('/api/insights')
}

/**
 * Create a new user account.
 *
 * @param {Object} userData - User registration data
 * @param {string} userData.name - User's full name
 * @param {string} userData.email - User's email address
 * @param {string} userData.password - User's password
 * @returns {Promise<{message: string, user: {id: number, name: string, email: string}}>}
 */
export async function signup(userData) {
  return request('/api/auth/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  })
}

/**
 * Authenticate a user.
 *
 * @param {Object} credentials - Login credentials
 * @param {string} credentials.email - User's email address
 * @param {string} credentials.password - User's password
 * @returns {Promise<{id: number, name: string, email: string}>}
 */
export async function login(credentials) {
  return request('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  })
}

/**
 * Get current user's profile.
 *
 * @returns {Promise<{id: number, name: string, email: string, created_at: string}>}
 */
export async function getProfile() {
  return request('/api/users/me')
}

/**
 * Update current user's profile (name only).
 *
 * @param {Object} profileData - Profile update data
 * @param {string} profileData.name - New name
 * @returns {Promise<{id: number, name: string, email: string, created_at: string}>}
 */
export async function updateProfile(profileData) {
  return request('/api/users/me', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(profileData),
  })
}

// Export the base request helper for future endpoints
export { request }
