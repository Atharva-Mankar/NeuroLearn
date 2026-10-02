"""
Session API router.

Handles creating and managing study sessions with persistence to the database.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.session import (
    CreateSessionRequest,
    CreateSessionResponse,
    SessionHealthResponse,
)
from app.database.connection import get_db
from app.models import StudySession, User
from app.core.current_user import get_current_user
from datetime import datetime
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["sessions"])


@router.post("/sessions", response_model=CreateSessionResponse)
def create_session(
    session_request: CreateSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CreateSessionResponse:
    """
    Create a new study session belonging to the current user.

    The session is persisted to the database with start timestamp.
    """
    # Create and persist the session
    db_session = StudySession(
        user_id=current_user.id,
        subject=session_request.subject,
        topic=session_request.topic,
        duration_minutes=session_request.duration_minutes,
        status="active",
        started_at=datetime.utcnow(),
        # elapsed_seconds is left NULL until the session is completed
    )

    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    # Return response matching the schema
    return CreateSessionResponse(
        id=db_session.id,
        subject=db_session.subject,
        topic=db_session.topic,
        planned_duration=db_session.duration_minutes,
        actual_duration=None,  # active sessions have no elapsed time yet
        status=db_session.status,
        start_time=db_session.started_at.isoformat(),
        webcam_monitoring=session_request.webcam_enabled,
    )


@router.get("/sessions", response_model=list[CreateSessionResponse])
def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CreateSessionResponse]:
    """
    Get all study sessions belonging to the current user.
    """
    sessions = (
        db.query(StudySession)
        .filter(StudySession.user_id == current_user.id)
        .order_by(StudySession.started_at.desc())
        .all()
    )

    return [
        CreateSessionResponse(
            id=session.id,
            subject=session.subject,
            topic=session.topic,
            planned_duration=session.duration_minutes,
            # A user looking at their history wants real elapsed time, not what
            # they originally planned. Plan and actual are shown side by side.
            actual_duration=(
                None if session.elapsed_seconds is None
                else round(session.elapsed_seconds / 60)
            ),
            status=session.status,
            start_time=session.started_at.isoformat(),
            webcam_monitoring=False,  # legacy field, not tracked in model yet
        )
        for session in sessions
    ]


@router.get("/sessions/{session_id}/health", response_model=SessionHealthResponse)
def get_session_health(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SessionHealthResponse:
    """
    Get basic health/status of a session, ensuring it belongs to the current user.
    """
    session = (
        db.query(StudySession)
        .filter(StudySession.id == session_id)
        .filter(StudySession.user_id == current_user.id)
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # For active sessions compute elapsed live; for completed use stored value.
    if session.status == "active":
        elapsed = int((datetime.utcnow() - session.started_at).total_seconds())
    else:
        # When finished the elapsed_seconds column holds the total.
        elapsed = session.elapsed_seconds or 0

    return SessionHealthResponse(
        is_active=session.status == "active",
        elapsed_seconds=elapsed,
    )


@router.post("/sessions/{session_id}/complete", response_model=CreateSessionResponse)
def complete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CreateSessionResponse:
    """
    Mark a study session as completed, updating the existing record.
    """
    session = (
        db.query(StudySession)
        .filter(StudySession.id == session_id)
        .filter(StudySession.user_id == current_user.id)
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != "active":
        raise HTTPException(
            status_code=400, detail="Only active sessions can be completed"
        )

    # Update the session to completed status. The elapsed time is measured from
    # the stored started_at rather than taken from the client, so the recorded
    # duration reflects real server-side time and cannot be inflated or faked.
    ended_at = datetime.utcnow()
    session.status = "completed"
    session.ended_at = ended_at
    session.elapsed_seconds = max(
        int((ended_at - session.started_at).total_seconds()), 0
    )

    db.commit()
    db.refresh(session)

    # Return response matching the schema.
    # planned_duration is what the user asked for; actual_duration is the real
    # elapsed time derived from server-side timestamps.
    return CreateSessionResponse(
        id=session.id,
        subject=session.subject,
        topic=session.topic,
        planned_duration=session.duration_minutes,
        actual_duration=(
            None if session.elapsed_seconds is None
            else round(session.elapsed_seconds / 60)
        ),
        status=session.status,
        start_time=session.started_at.isoformat(),
        webcam_monitoring=False,  # legacy field, not tracked in model yet
    )