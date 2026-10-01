# Phase 3 Task 2 — Frontend-Backend Health Check Test

## Implementation Summary

The React frontend can communicate with the FastAPI backend via:
- **API Service**: `frontend/src/services/api.js`
- **Dev Health Check**: `frontend/src/utils/devHealthCheck.js`
- **Exposed Test Function**: `window.testBackendHealth()`

## Backend /health Endpoint Response

```json
{
  "status": "ok",
  "project": "NeuroLearn",
  "version": "0.1.0"
}
```

## Manual Test Procedure

### 1. Stop any running instances

```bash
# Kill any existing Python/Vite processes
taskkill /F /PID <backend_pid>
taskkill /F /PID <vite_pid>
```

### 2. Start FastAPI Backend

```bash
cd backend
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Verify backend is running:
```bash
curl http://127.0.0.1:8000/health
# Should return: {"status":"ok","project":"NeuroLearn","version":"0.1.0"}
```

### 3. Start Vite Frontend

```bash
cd frontend
npm run dev
```

**IMPORTANT**: Vite must start on port **5173** for CORS to work.
If ports 5173+ are in use, stop those processes first.

Expected output:
```
VITE v8.3.1  ready in XXX ms

➜  Local:   http://localhost:5173/
```

### 4. Open Browser and Test

1. Navigate to: **http://localhost:5173**
2. Open browser **DevTools Console** (F12)
3. You should see the message:
   ```
   💡 Backend health check available. Run: window.testBackendHealth()
   ```
4. Run in console:
   ```javascript
   window.testBackendHealth()
   ```

### Expected Console Output

```
🔍 Testing backend connection...
✅ Backend is reachable!
Response: {status: 'ok', project: 'NeuroLearn', version: '0.1.0'}
```

### 5. Verify All Routes Load

Navigate to each route and verify it loads without errors:
- http://localhost:5173/ (redirects to /dashboard)
- http://localhost:5173/login
- http://localhost:5173/signup
- http://localhost:5173/dashboard
- http://localhost:5173/session
- http://localhost:5173/calendar
- http://localhost:5173/history
- http://localhost:5173/insights
- http://localhost:5173/settings

All routes should return **200 OK** and render correctly.

## Verification Checklist

- [x] Temporary test file `frontend/test-health.js` removed (never existed)
- [x] Backend `/health` endpoint returns correct JSON
- [x] CORS configured for `localhost:5173` and `127.0.0.1:5173`
- [x] Frontend API service implements `getHealth()` function
- [x] Dev health check exposes `window.testBackendHealth()`
- [x] Lint passes: `npm run lint` ✓
- [x] Build succeeds: `npm run build` ✓
- [x] All routes return 200 OK
- [ ] Manual browser test: `window.testBackendHealth()` (requires manual execution)

## Implementation Files

- `backend/app/main.py` — FastAPI app with /health endpoint and CORS
- `frontend/src/services/api.js` — API communication layer
- `frontend/src/utils/devHealthCheck.js` — Development health check utility
- `frontend/src/main.jsx` — Imports devHealthCheck to expose window function

## Notes

- This is a **development-only** test mechanism
- The health check function is exposed globally via `window.testBackendHealth()`
- Production builds should remove or gate this development utility
- CORS is currently configured for local development origins only
