"""
Dashboard API router.

Returns user-specific dashboard data pulled from the database.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.dashboard import (
    DashboardResponse,
    UserInfo,
    StudyProgress,
    FatigueLevel,
    TimelineItem,
    RecentSession,
    AdaptiveSuggestion,
    CalendarPreviewItem,
)
from app.database.connection import get_db
from app.models import StudySession, User
from app.core.current_user import get_current_user
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["dashboard"])

# Fatigue estimation belongs to a later phase (it needs webcam-based signal
# processing). Until then the dashboard states plainly that it has no value
# rather than showing a made-up score.
FATIGUE_UNAVAILABLE_LABEL = "Unavailable"

FATIGUE_UNAVAILABLE_DISCLAIMER = (
    "Not available yet. Fatigue estimation requires webcam monitoring, "
    "which is not implemented in this phase. NeuroLearn is a study "
    "productivity tool, not a medical device."
)


def _to_local(timestamp: datetime) -> datetime:
    """Convert a stored naive-UTC timestamp into local time.

    ``StudySession`` timestamps are written with ``datetime.utcnow()``, so UTC
    has to be attached explicitly before converting -- otherwise Python would
    treat the naive value as already-local and shift it by the UTC offset a
    second time.
    """
    return timestamp.replace(tzinfo=timezone.utc).astimezone()


def _format_local_time(timestamp: datetime) -> str:
    """Render a stored UTC timestamp as a 12-hour clock time, e.g. "7:05 PM".

    This is the real time the session ended, read from the database row. No
    timestamp is ever invented.

    ``%-I`` is deliberately avoided: it is a glibc extension and raises on
    Windows, so the hour is formatted explicitly.
    """
    local = _to_local(timestamp)
    hour_12 = local.hour % 12 or 12
    return f"{hour_12}:{local.minute:02d} {'AM' if local.hour < 12 else 'PM'}"


def _local_date(timestamp: datetime):
    """Return the local calendar date a stored UTC timestamp falls on.

    Grouping "today" and the calendar preview in UTC while rendering times in
    local time would put a late-evening session on the wrong day, so both use
    this helper and stay consistent with the clock time shown to the user.
    """
    return _to_local(timestamp).date()


def _format_actual_duration(session) -> str:
    """Render how long a session really lasted.

    Prefers the measured ``elapsed_seconds``. Sessions completed before that
    column existed have no measurement, so the planned duration is shown
    instead -- clearly marked, rather than passed off as actual study time.
    """
    if session.elapsed_seconds is None:
        return f"{session.duration_minutes} min (planned)"
    return f"{round(session.elapsed_seconds / 60)} min"


def _calculate_study_progress(sessions):
    """Summarise how much the user actually studied in the last 7 days.

    There is no stored study goal yet, so no percentage is produced. Showing
    "0%" next to real hours would read as "you have achieved nothing", which is
    just as misleading as inventing a goal, so the percentage is left unset and
    the frontend renders the hours alone.
    """
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    completed_this_week = [
        s for s in sessions
        if s.status == "completed" and s.ended_at and s.ended_at >= one_week_ago
    ]

    # Sum real elapsed time, falling back to the planned duration only for
    # sessions completed before elapsed_seconds was tracked.
    total_minutes = sum(
        (s.elapsed_seconds / 60.0) if s.elapsed_seconds is not None else s.duration_minutes
        for s in completed_this_week
    )
    total_hours = total_minutes / 60.0

    return StudyProgress(
        percentage=None,
        description=f"{total_hours:.1f} hours completed in the last 7 days",
    )


def _get_recent_sessions(sessions, limit=4):
    """Get recent completed sessions for display."""
    completed_sessions = [s for s in sessions if s.status == "completed" and s.ended_at]
    completed_sessions.sort(key=lambda s: s.ended_at, reverse=True)

    recent = completed_sessions[:limit]
    return [
        RecentSession(
            id=session.id,
            subject=session.subject,
            topic=session.topic,
            duration=_format_actual_duration(session),
            fatigue=FATIGUE_UNAVAILABLE_LABEL,
            date=_to_local(session.ended_at).strftime("%b %d")
        )
        for session in recent
    ]


def _get_today_timeline(sessions):
    """Get today's timeline from completed sessions."""
    today = datetime.now().astimezone().date()
    todays_sessions = [
        s for s in sessions
        if s.status == "completed" and s.ended_at and _local_date(s.ended_at) == today
    ]

    # Sort by end time
    todays_sessions.sort(key=lambda s: s.ended_at)

    timeline_items = []
    for session in todays_sessions:
        timeline_items.append(
            TimelineItem(
                time=_format_local_time(session.ended_at),
                subject=session.subject,
                duration=f"{session.duration_minutes} min",
                kind="study"
            )
        )

    # If no sessions today, return empty timeline (frontend can handle this)
    return timeline_items


def _get_adaptive_suggestions(sessions):
    """Generate adaptive suggestions based on session history.

    The adaptive scheduler itself belongs to a later phase. These are simple
    observations read straight off the user's own rows -- no invented statistics
    such as a "best focus window", which cannot be derived without the fatigue
    data that does not exist yet.
    """
    completed_sessions = [s for s in sessions if s.status == "completed" and s.ended_at]
    if len(completed_sessions) < 2:
        return []

    # Sort by end time, most recent first
    sorted_sessions = sorted(completed_sessions, key=lambda s: s.ended_at, reverse=True)
    suggestions = []

    # If the two most recent sessions ended less than an hour apart
    time_diff = sorted_sessions[0].ended_at - sorted_sessions[1].ended_at
    if time_diff.total_seconds() < 3600:
        suggestions.append(
            AdaptiveSuggestion(
                title="Short break between sessions",
                description=(
                    "Your two most recent sessions ended less than an hour "
                    "apart. A short break between them may help you stay focused."
                )
            )
        )

    # If the same subject was studied three times in a row
    if (
        len(sorted_sessions) >= 3
        and sorted_sessions[0].subject
        == sorted_sessions[1].subject
        == sorted_sessions[2].subject
    ):
        suggestions.append(
            AdaptiveSuggestion(
                title="Try a different subject",
                description=(
                    f"You have studied {sorted_sessions[0].subject} for your "
                    "last three sessions. Switching subjects may help keep you engaged."
                )
            )
        )

    return suggestions[:3]


def _get_calendar_preview(sessions):
    """Get calendar preview of sessions per day."""
    # Group sessions by local date (completed sessions only)
    sessions_by_date = {}
    for session in sessions:
        if session.status == "completed" and session.ended_at:
            date_key = _local_date(session.ended_at).isoformat()
            sessions_by_date[date_key] = sessions_by_date.get(date_key, 0) + 1

    # Get last 7 days
    today = datetime.now().astimezone().date()
    preview_items = []
    for i in range(7):
        date = today - timedelta(days=i)
        date_str = date.isoformat()
        count = sessions_by_date.get(date_str, 0)
        preview_items.append(CalendarPreviewItem(date=date_str, sessions=count))

    # Reverse to show most recent first
    return list(reversed(preview_items))


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DashboardResponse:
    """
    Get dashboard data for the current user from the database.

    Returns real data calculated from the user's completed sessions.
    """
    # Fetch all sessions for the current user
    sessions = (
        db.query(StudySession)
        .filter(StudySession.user_id == current_user.id)
        .order_by(StudySession.started_at.desc())
        .all()
    )

    # Calculate dashboard components
    study_progress = _calculate_study_progress(sessions)
    recent_sessions = _get_recent_sessions(sessions)
    today_timeline = _get_today_timeline(sessions)
    adaptive_suggestions = _get_adaptive_suggestions(sessions)
    calendar_preview = _get_calendar_preview(sessions)

    # Fatigue estimation requires webcam monitoring which is not yet implemented.
    # Show an honest unavailable state rather than faking a value.
    fatigue_level = FatigueLevel(
        label="Fatigue estimation",
        value=None,
        level=FATIGUE_UNAVAILABLE_LABEL,
        disclaimer=FATIGUE_UNAVAILABLE_DISCLAIMER
    )

    return DashboardResponse(
        user=UserInfo(
            name=current_user.name,
            email=current_user.email
        ),
        study_progress=study_progress,
        fatigue=fatigue_level,
        today_timeline=today_timeline,
        recent_sessions=recent_sessions,
        adaptive_suggestions=adaptive_suggestions,
        calendar_preview=calendar_preview
    )
