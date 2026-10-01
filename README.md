# NeuroLearn

Personalized Cognitive Fatigue Detector and Adaptive Study Scheduler.

NeuroLearn is a student productivity platform. In a later phase it will estimate
study-related fatigue signals from local computer-vision analysis of eye and face
signals, and use a student's study history to suggest study periods and breaks.

**NeuroLearn is a study productivity tool, not a medical diagnostic system.**
Any fatigue output is an approximate signal for study planning, not a medical result.

## Technology Stack

- Frontend: React, Vite, Tailwind CSS
- Backend: Python 3.11, FastAPI, Uvicorn, Pydantic
- Database: SQLite (planned for a later phase)
- Computer vision: OpenCV, MediaPipe, a local eye model (planned for a later phase)
- Tools: VS Code, Git, GitHub, Python virtual environment, npm
- Everything runs locally. No paid APIs and no cloud services are used.

## Project Structure

```text
Neuro Learn/
├── frontend/          # React + Vite + Tailwind user interface
├── backend/           # FastAPI application and Python virtual environment
├── docs/              # Supporting documentation
├── .gitignore         # Files Git should not track
├── README.md          # This file
├── CLAUDE_RULES.md    # Permanent development rules for this project
└── NEUROLEARN_DEVELOPMENT_PLAN.md
```

The planned full structure and the development phases are documented in
`NEUROLEARN_DEVELOPMENT_PLAN.md`.

## How to Start the Frontend

Open a terminal in the `frontend` folder and run:

```bash
npm install
npm run dev
```

Then open the address Vite prints in the browser, usually:

```text
http://localhost:5173
```

The page should show "NeuroLearn", "Personalized Cognitive Fatigue Detector and
Adaptive Study Scheduler", and "NeuroLearn frontend is running."

## How to Start the Backend

Open a terminal in the `backend` folder.

The first time, create the Python virtual environment and install dependencies:

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

On Windows PowerShell the equivalent is:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then start the backend:

```bash
.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

Verify it:

- Health check: <http://127.0.0.1:8000/health>
- Interactive API docs: <http://127.0.0.1:8000/docs>

The health endpoint should return:

```json
{
  "status": "ok",
  "project": "NeuroLearn",
  "version": "0.1.0"
}
```

## Current Phase

**Phase 1 — Project Foundation (complete).**

The frontend and backend both run independently on your own computer. The backend
has a working `/health` endpoint and the frontend has a simple welcome page. They
are not yet connected to each other in the interface.

## Current Limitations

- No user accounts or login.
- No database, so nothing is saved between sessions yet.
- No study sessions, dashboard, or scheduler.
- No webcam access, computer vision, or fatigue estimation.
- The frontend page does not yet display live data from the backend.
- Nothing has been tested beyond the basic startup and health checks.
