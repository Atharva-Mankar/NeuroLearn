"""
Session API router.

Handles creating and managing study sessions.
In a later phase, this will connect to a database and implement
full session lifecycle with pause/resume/end functionality.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.session import (
    CreateSessionRequest,
    CreateSessionResponse,
    SessionHealthResponse,
)
from datetime import datetime
import uuid

router = APIRouter(prefix="/api", tags=["sessions"])

# In-memory session store for demo purposes
# In production, this would be replaced with a database
demo_sessions = {}
session_counter = 1


@router.post("/sessions", response_model=CreateSessionResponse)
def create_session(session_request: CreateSessionRequest) -> CreateSessionResponse:
    """
    Create a new study session.

    For Phase 5, this returns demo data. In Phase 6+:
    - Save session to database with start timestamp
    - Generate unique session ID
    - Return the created session record
    """
    global session_counter

    # Generate demo session data
    session_id = session_counter
    session_counter += 1

    # Create session response
    response = CreateSessionResponse(
        id=session_id,
        subject=session_request.subject,
        topic=session_request.topic,
        planned_duration=session_request.duration_minutes,
        status="active",
        start_time=datetime.now().isoformat(),
        webcam_monitoring=session_request.webcam_enabled,
    )

    # Store in demo cache (would be database in production)
    demo_sessions[session_id] = {
        **response.dict(),
        "elapsed_seconds": 0,
    }

    return response


@router.get("/sessions/{session_id}/health", response_model=SessionHealthResponse)
def get_session_health(session_id: int) -> SessionHealthResponse:
    """
    Get basic health/status of a session.
    Demo endpoint for Phase 5 - in later phases this would
    pull real-time data from active session.
    """
    if session_id not in demo_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = demo_sessions[session_id]
    return SessionHealthResponse(
        is_active=session["status"] == "active",
        elapsed_seconds=session.get("elapsed_seconds", 0),
    )