/**
 * Development-only health check utility.
 *
 * This file tests the backend API connection during Phase 3 development.
 * It can be removed once the integration is verified and real endpoints
 * are connected.
 *
 * Usage:
 * 1. Start the backend: uvicorn app.main:app --reload
 * 2. Start the frontend: npm run dev
 * 3. Open browser console and run: window.testBackendHealth()
 */

import { getHealth } from '../services/api'

/**
 * Test the backend /health endpoint and log the result.
 * Exposed as window.testBackendHealth() for manual testing in the console.
 */
async function testBackendHealth() {
  console.log('🔍 Testing backend connection...')

  try {
    const response = await getHealth()
    console.log('✅ Backend is reachable!')
    console.log('Response:', response)
    return response
  } catch (error) {
    console.error('❌ Backend connection failed!')
    console.error('Error:', error.message)
    throw error
  }
}

// Expose to window for manual testing in the browser console
if (typeof window !== 'undefined') {
  window.testBackendHealth = testBackendHealth
  console.log(
    '💡 Backend health check available. Run: window.testBackendHealth()'
  )
}

export { testBackendHealth }
