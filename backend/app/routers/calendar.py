"""Calendar API router.

Returns a per-day summary of the current user's real study sessions for one
month, queried from the database.

Timestamps are stored as naive UTC (see ``StudySession.started_at``) but grouped
by the *local* calendar date, matching the dates the user actually sees. Grouping
in UTC would push a late-evening session onto the wrong day for anyone east of
UTC. The helpers for that conversion live in ``app/routers/dashboard.py`` and are
reused rather than reimplemented.
"""

from datetime import date, datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.database.connection import get_db
from app.models import StudySession, User
from app.routers.dashboard import _local_date
from app.schemas.calendar import CalendarDay, CalendarResponse

router = APIRouter(prefix="/api", tags=["calendar"])


def _session_minutes(session: StudySession) -> float:
    """Minutes a session actually contributed.

    A completed session reports its measured elapsed time. An active one has no
    elapsed time yet, so its planned length is used -- which is what the user
    asked for, and is all that exists at that point.
    """
    if session.elapsed_seconds is not None:
        return session.elapsed_seconds / 60
    return float(session.duration_minutes)


@router.get("/calendar", response_model=CalendarResponse)
def get_calendar(
    month: int = Query(
        default=None,
        ge=1,
        le=12,
        description="Month to return, 1-12. Defaults to the current month.",
    ),
    year: int = Query(
        default=None,
        ge=1970,
        le=9999,
        description="Year to return. Defaults to the current year.",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CalendarResponse:
    """Summarise the current user's sessions for one month.

    Ownership is enforced in the query itself -- ``StudySession.user_id ==
    current_user.id`` -- so another user's sessions are never loaded into
    memory, let alone returned. The React layer plays no part in this.

    Only days that have at least one session are returned. An empty month is an
    empty list rather than a list of zeroed days, which keeps the "no sessions"
    state unambiguous instead of a month of fake zeros.
    """
    today_local = datetime.now().astimezone().date()
    month = month if month is not None else today_local.month
    year = year if year is not None else today_local.year

    # The month is bounded by local midnights on either side, so the UTC range
    # that gets translated into local dates is exactly the local month.
    month_start = datetime.combine(date(year, month, 1), time.min)
    next_month_start = (
        datetime.combine(date(year + 1, 1, 1), time.min)
        if month == 12
        else datetime.combine(date(year, month + 1, 1), time.min)
    )

    sessions = (
        db.query(StudySession)
        .filter(StudySession.user_id == current_user.id)
        .filter(StudySession.started_at >= month_start)
        .filter(StudySession.started_at < next_month_start)
        .order_by(StudySession.started_at.asc())
        .all()
    )

    by_day: dict[date, dict] = {}
    for session in sessions:
        day = _local_date(session.started_at)
        entry = by_day.setdefault(
            day, {"sessions": 0, "subjects": set(), "total_duration": 0.0}
        )
        entry["sessions"] += 1
        entry["subjects"].add(session.subject)
        entry["total_duration"] += _session_minutes(session)

    days = [
        CalendarDay(
            date=day,
            sessions=entry["sessions"],
            subjects=sorted(entry["subjects"]),
            # Sessions shorter than a minute round down to 0, which is honest:
            # there is no partial-minute study time to report.
            total_duration=int(entry["total_duration"]),
        )
        for day, entry in sorted(by_day.items())
    ]

    return CalendarResponse(month=month, year=year, days=days)


__all__ = ["router"]