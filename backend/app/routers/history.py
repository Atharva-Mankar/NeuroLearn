"""History API router.

Returns the current user's real study session history, newest first, queried
from the database.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.database.connection import get_db
from app.models import StudySession, User
from app.routers.dashboard import FATIGUE_UNAVAILABLE_LABEL, _local_date
from app.schemas.history import HistoryResponse, HistorySession, HistorySummary

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history", response_model=HistoryResponse)
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> HistoryResponse:
    """Return every session belonging to the current user, newest first.

    Ownership is enforced in the query -- ``StudySession.user_id ==
    current_user.id`` -- so another user's rows are never loaded, not merely
    hidden by the frontend.

    Fatigue estimation is not implemented, so it reports the same honest
    ``Unavailable`` state the dashboard uses rather than a fabricated level.
    """
    sessions = (
        db.query(StudySession)
        .filter(StudySession.user_id == current_user.id)
        .order_by(StudySession.started_at.desc())
        .all()
    )

    records: list[HistorySession] = []
    total_minutes = 0

    for session in sessions:
        # Real study time for a finished session; a still-running one has no
        # elapsed time yet, so its planned length is what can honestly be shown.
        if session.elapsed_seconds is not None:
            duration_minutes = round(session.elapsed_seconds / 60)
        else:
            duration_minutes = session.duration_minutes

        total_minutes += duration_minutes

        records.append(
            HistorySession(
                id=session.id,
                subject=session.subject,
                topic=session.topic,
                duration=duration_minutes,
                fatigue=FATIGUE_UNAVAILABLE_LABEL,
                # Local calendar date, matching the date shown on the calendar.
                date=_local_date(session.started_at).isoformat(),
                status=session.status,
            )
        )

    total_sessions = len(records)
    summary = HistorySummary(
        total_sessions=total_sessions,
        total_hours=round(total_minutes / 60, 1),
        avg_fatigue=FATIGUE_UNAVAILABLE_LABEL,
        avg_duration=round(total_minutes / total_sessions) if total_sessions else 0,
    )

    return HistoryResponse(summary=summary, sessions=records)


__all__ = ["router"]