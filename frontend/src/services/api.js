/**
 * API communication layer for the NeuroLearn frontend.
 *
 * All backend requests go through this service so the base URL and error
 * handling stay consistent. Uses the browser's native fetch API.
 */

// Backend base URL - update this when deploying to production
const API_BASE_URL = 'http://127.0.0.1:8000'

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

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
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
 * Calendar endpoint.
 *
 * @param {number} month - Month (1-12, defaults to 9)
 * @param {number} year - Year (defaults to 2026)
 * @returns {Promise<CalendarResponse>} - Calendar data
 */
export async function getCalendar(month = 9, year = 2026) {
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

// Export the base request helper for future endpoints
export { request }
