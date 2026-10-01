"""NeuroLearn FastAPI application entry point.

This is the main file Uvicorn loads. It creates the web application,
allows the local React frontend to talk to it, and exposes a simple
/health endpoint used to check that the backend is running.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dashboard

PROJECT_NAME = "NeuroLearn"
VERSION = "0.1.0"

# The Vite development server runs on port 5173 by default.
# CORS is a browser security rule. Because the frontend (port 5173) and the
# backend (port 8000) are different addresses, the browser would normally
# block the request. Listing the local frontend addresses here tells the
# backend that this local connection is allowed.
LOCAL_FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI(
    title=PROJECT_NAME,
    description=(
        "Personalized Cognitive Fatigue Detector and Adaptive Study Scheduler. "
        "NeuroLearn is a study productivity tool, not a medical system."
    ),
    version=VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=LOCAL_FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(dashboard.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple check used to confirm the backend is running correctly."""
    return {
        "status": "ok",
        "project": PROJECT_NAME,
        "version": VERSION,
    }
