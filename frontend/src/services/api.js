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

// Export the base request helper for future endpoints
export { request }
