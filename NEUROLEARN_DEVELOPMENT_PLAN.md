# NeuroLearn Development Plan

## 1. Project Objective

NeuroLearn is a local-first student productivity platform that estimates study-related cognitive fatigue signals and uses them to help create more adaptive study schedules.

The planned user flow is:

1. A student creates an account and logs in.
2. The student opens a personalized dashboard.
3. The student starts a study session.
4. The student may enable local webcam monitoring.
5. The computer vision system processes face/eye-related signals locally when monitoring is enabled.
6. The application aggregates extracted features over time instead of storing raw webcam video.
7. The application estimates a fatigue level for productivity purposes.
8. The student ends the session and receives a summary.
9. Session information is stored locally in SQLite.
10. The adaptive scheduler uses study history, workload, and fatigue-related information to suggest future study periods and breaks.

NeuroLearn is a productivity aid, not a medical diagnostic system. Its fatigue estimate must be presented as an approximate study-related signal and not as medical advice.

## 2. Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- JavaScript or JSX initially, keeping the code easy to understand

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### Database

- SQLite initially
- A simple local database layer before considering any migration or hosted database

### Computer Vision

- OpenCV
- MediaPipe
- An existing local eye-detection model only when it is evaluated and integrated in a later phase
- Local frame processing whenever possible
- No raw webcam video storage

### Development Tools

- VS Code
- Git and GitHub
- Python virtual environment
- npm
- Local development servers only for the first version

## 3. Planned Architecture

The application will use a small three-layer local architecture:

```text
React + Vite frontend
        |
        | HTTP requests to a local API
        v
FastAPI backend
        |
        +-- authentication and user-related routes
        +-- study-session routes
        +-- fatigue-feature aggregation and estimation
        +-- scheduler/recommendation logic
        +-- Pydantic request and response schemas
        v
SQLite database
```

The webcam will be accessed only with explicit user permission. Frames should be processed locally, converted into non-video feature data, and discarded. The first prototype should prioritize transparent rules and simple calculations over complicated machine-learning infrastructure.

Planned boundaries:

- The frontend is responsible for pages, forms, dashboard presentation, session controls, and user-facing feedback.
- The backend is responsible for validation, application rules, persistence, and API responses.
- The database stores accounts, study sessions, aggregated features, summaries, and scheduling information as the design becomes ready.
- Computer-vision code will be isolated from authentication and scheduling code so it can be tested or replaced independently.
- The scheduler will initially use understandable rule-based recommendations. More advanced models are optional future work, not a requirement for the first working prototype.

## 4. Development Phases

### Phase 0 — Workspace and Tooling Inspection (current phase)

- Inspect the existing workspace.
- Confirm whether the workspace is empty or already contains code.
- Check Node.js, npm, Python, and Git availability and versions.
- Record the agreed project rules and plan.
- Do not install packages or begin implementation yet.

### Phase 1 — Project Foundation

- Create the initial frontend and backend folder structure without unnecessary files.
- Create a Python virtual environment and backend dependency configuration when approved.
- Create the Vite React application and basic styling setup when approved.
- Add a minimal local health-check path so the frontend and backend can be verified independently.

### Phase 2 — Backend and Database Foundation

- Add FastAPI application structure.
- Add SQLite connection and simple database initialization.
- Define clear Pydantic schemas and database models.
- Add basic error handling and local configuration.
- Avoid implementing full authentication until the foundation is understandable and testable.

### Phase 3 — Authentication and User Flow

- Add account creation and login using local, appropriately hashed passwords.
- Add a protected dashboard route.
- Keep secrets and configuration outside source code.
- Add beginner-friendly validation and error messages.

### Phase 4 — Study Sessions

- Add start, pause/resume if needed, and end-session actions.
- Store session metadata and basic study outcomes.
- Build the first dashboard summary without webcam monitoring.

### Phase 5 — Local Computer-Vision Prototype

- Request webcam permission only when the student enables monitoring.
- Process frames locally using OpenCV and MediaPipe where practical.
- Extract and aggregate eye/face-related signals.
- Discard frames after processing and never store raw webcam video.
- Clearly label the output as an approximate productivity signal.
- Test the feature with monitoring disabled as a complete fallback path.

### Phase 6 — Fatigue Estimation and Session Summary

- Convert aggregated features into a simple, explainable fatigue estimate.
- Add confidence/availability information where appropriate.
- Generate a post-session summary with limitations clearly explained.
- Handle missing camera data without breaking the study session.

### Phase 7 — Adaptive Scheduler

- Add workload and study-history inputs.
- Implement transparent recommendations for study duration and breaks.
- Store recommendations and outcomes for later improvement.
- Avoid claiming medical or scientific certainty.

### Phase 8 — Testing, Accessibility, and Hardening

- Add backend API tests and frontend interaction tests as appropriate.
- Test camera-denied, camera-unavailable, empty-data, and invalid-input cases.
- Improve accessibility, responsive layout, and clear privacy messaging.
- Review local data handling and remove accidental secrets or raw media files.

### Phase 9 — Documentation and Optional Future Improvements

- Document setup, running, testing, and troubleshooting steps.
- Review whether any component needs optimization.
- Consider optional improvements only after the local prototype is stable.
- Do not add cloud services or paid APIs unless requirements explicitly change and the decision is reviewed first.

## 5. Intended Folder Structure

The workspace is currently empty. When implementation begins, we intend to create a structure similar to this, adding folders only when they are needed:

```text
Neuro Learn/
├── frontend/                    # React + Vite + Tailwind application
│   ├── src/
│   │   ├── components/          # Reusable user-interface components
│   │   ├── pages/               # Main screens such as login and dashboard
│   │   ├── services/            # Small modules for calling the backend API
│   │   ├── hooks/               # Reusable React hooks, when needed
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── api/                 # API route modules
│   │   ├── core/                # Configuration and shared infrastructure
│   │   ├── db/                  # SQLite setup and database helpers
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/            # Session, fatigue, and scheduler logic
│   │   └── main.py              # FastAPI application entry point
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example             # Names/examples only; no real secrets
├── data/                        # Local runtime data; review before committing
├── docs/                        # Optional supporting documentation
├── .gitignore
├── CLAUDE_RULES.md
└── NEUROLEARN_DEVELOPMENT_PLAN.md
```

This is an intended structure, not a requirement to create every folder immediately. Empty folders and speculative modules should not be added before they are needed.

## 6. Important Development Rules

- Build a working local prototype phase by phase; do not build the entire application at once.
- Inspect the existing project structure before modifying important files.
- Preserve working code and make the smallest practical change.
- Do not delete existing files without explicit approval.
- Do not rewrite the entire project unnecessarily.
- Do not create duplicate versions of components or modules.
- Prefer free, open-source, and local technologies.
- Do not add paid APIs or require OpenAI, Gemini, or other external AI APIs.
- Do not add unnecessary cloud services.
- Keep secrets and API keys out of source code.
- Do not store raw webcam video.
- Process webcam frames locally whenever possible and request permission explicitly.
- Handle camera denial and unavailable camera hardware gracefully.
- Describe fatigue output as an approximate productivity signal, never as a medical diagnosis.
- Keep code clear and suitable for a beginner to read.
- Explain unfamiliar concepts before relying on them.
- Add packages only when they are needed and their purpose is clear.
- Verify each phase before moving to the next phase.
- Do not continue to a later phase automatically without the user's instruction.
- Use Git checkpoints once a repository has been initialized, without committing secrets or local runtime data.
- Update documentation when setup or behavior changes.

## 7. Current Project Status

**Status: Phase 0 — workspace inspection complete.**

Inspection completed on September 28, 2026:

- Workspace path: `C:\Users\ASUS VIVOBOOK\OneDrive\Desktop\Neuro Learn`
- Existing project files: none detected; the workspace appears to be empty.
- Existing application code: none detected.
- Node.js: available, version `v24.21.0`
- npm: available, version `12.1.0`
- Python: available, version `3.11.9`
- Git: available, version `2.55.0.windows.3`
- Packages installed for NeuroLearn during this phase: none.
- Existing files were not deleted or rewritten.

The next phase will begin only after the user gives a separate instruction.
