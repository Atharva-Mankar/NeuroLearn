"""
Insights API router.

Every number this router returns is calculated from the authenticated user's
own completed ``StudySession`` rows. Nothing is sampled, seeded or estimated,
and the response carries explicit empty states rather than filler values when
the user has no data yet.

Isolation is enforced in the query itself (``StudySession.user_id ==
current_user.id``), so another user's rows are never loaded into memory -- not
merely hidden by the frontend. The endpoint accepts no user id parameter at all,
so there is nothing for a client to override.

Fatigue is not estimated here. It has no data source in this phase, so it is
reported as unavailable rather than inferred from study duration.
"""

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.database.connection import get_db
from app.models import StudySession, User
from app.schemas.insights import (
    ActivityPoint,
    InsightsFatigue,
    InsightsResponse,
    InsightsStreak,
    InsightsSummary,
    SubjectSlice,
)

router = APIRouter(prefix="/api", tags=["insights"])

# Fatigue estimation needs webcam signal processing, which does not exist yet.
# Inferred-from-duration would be a guess presented as a measurement, so the
# endpoint says so plainly instead.
FATIGUE_UNAVAILABLE_REASON = (
    "Fatigue estimation requires webcam monitoring, which is not implemented "
    "in this phase. No fatigue data has been recorded for this account."
)

# Upper bound on the activity chart window. Bounded so a hand-crafted
# ?days=100000 cannot ask the server to build a million-element array.
MAX_ACTIVITY_DAYS = 365


def _to_local(timestamp: datetime) -> datetime:
    """Convert a stored naive-UTC timestamp into local time.

    ``StudySession`` timestamps are written with ``datetime.utcnow()``, so UTC
    has to be attached explicitly before converting -- otherwise Python would
    treat the naive value as already-local and shift it a second time.
    """
    return timestamp.replace(tzinfo=timezone.utc).astimezone()


def _local_date(timestamp: datetime):
    """Return the local calendar date a stored UTC timestamp falls on."""
    return _to_local(timestamp).date()


def _session_minutes(session: StudySession) -> float:
    """Real minutes a completed session contributed.

    Prefers the server-measured ``elapsed_seconds``. Rows completed before that
    column existed have no measurement, so they fall back to the planned
    duration -- which is what was actually recorded at the time, rather than an
    invented figure.
    """
    if session.elapsed_seconds is not None:
        return session.elapsed_seconds / 60
    return float(session.duration_minutes)


def _week_start(reference: datetime) -> datetime:
    """Start of the ISO week (Monday 00:00) containing ``reference``."""
    local = _to_local(reference)
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
    # ``weekday()`` is Monday=0, so subtracting it lands on the Monday.
    return midnight - timedelta(days=local.weekday())


def _calculate_streaks(session_dates: set) -> InsightsStreak:
    """Current and longest consecutive-day streaks.

    A streak is a run of local calendar dates with at least one completed
    session. The current streak may legitimately start yesterday: someone who
    studied yesterday but not yet today still has an unbroken run going, and
    reporting 0 until they open the app again would be wrong.
    """
    if not session_dates:
        return InsightsStreak(current=0, longest=0)

    ordered = sorted(session_dates)

    # Longest run across the whole history.
    longest = 1
    run = 1
    for previous, current in zip(ordered, ordered[1:]):
        if (current - previous).days == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1

    today = datetime.now().astimezone().date()
    latest = ordered[-1]

    # Anchor on today, or on yesterday when today has no session yet.
    if latest == today:
        anchor = today
    elif latest == today - timedelta(days=1):
        anchor = latest
    else:
        # The run was broken before yesterday, so there is no live streak.
        return InsightsStreak(current=0, longest=longest)

    current = 0
    walk = anchor
    while walk in session_dates:
        current += 1
        walk -= timedelta(days=1)

    return InsightsStreak(current=current, longest=max(current, longest))


@router.get("/insights", response_model=InsightsResponse)
def get_insights(
    days: int = Query(
        default=14,
        ge=1,
        le=MAX_ACTIVITY_DAYS,
        description="Length in days of the study activity chart window.",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InsightsResponse:
    """Return study insights calculated from the current user's own sessions.

    Args:
        days: Length of the activity chart window, counted backwards from
            today. Clamped by FastAPI to 1-365.
        current_user: The acting user, resolved by the shared auth dependency.
        db: Database session.

    Returns:
        An :class:`InsightsResponse`. A user with no completed sessions gets
        ``has_data=False`` with zeroes and empty lists -- a valid empty state,
        never fabricated numbers.
    """
    # User isolation is part of the query, not a filter applied afterwards.
    sessions = (
        db.query(StudySession)
        .filter(StudySession.user_id == current_user.id)
        .filter(StudySession.status == "completed")
        .order_by(StudySession.started_at.asc())
        .all()
    )

    total_minutes = 0.0
    hourly_minutes: dict[int, float] = defaultdict(float)
    subject_minutes: dict[str, float] = defaultdict(float)
    subject_counts: dict[str, int] = defaultdict(int)
    per_day_minutes: dict = defaultdict(float)
    per_day_counts: dict = defaultdict(int)
    session_dates: set = set()

    for session in sessions:
        minutes = _session_minutes(session)
        total_minutes += minutes

        local_start = _to_local(session.started_at)
        hourly_minutes[local_start.hour] += minutes

        subject_minutes[session.subject] += minutes
        subject_counts[session.subject] += 1

        day = local_start.date()
        per_day_minutes[day] += minutes
        per_day_counts[day] += 1
        session_dates.add(day)

    # The week is anchored on the local Monday so "this week" matches what the
    # user sees on a calendar, not a UTC day boundary.
    week_start = _week_start(datetime.utcnow())
    week_cutoff = week_start.astimezone(timezone.utc).replace(tzinfo=None)

    week_sessions = 0
    week_minutes = 0.0
    for session in sessions:
        if session.started_at >= week_cutoff:
            week_sessions += 1
            week_minutes += _session_minutes(session)

    ordered_days = sorted(session_dates)

    summary = InsightsSummary(
        total_sessions=len(sessions),
        total_minutes=round(total_minutes, 1),
        total_hours=round(total_minutes / 60, 1),
        avg_session_minutes=(
            round(total_minutes / len(sessions), 1) if sessions else 0.0
        ),
        week_sessions=week_sessions,
        week_minutes=round(week_minutes, 1),
        week_hours=round(week_minutes / 60, 1),
        week_start=week_start.date().isoformat(),
        first_session_date=ordered_days[0].isoformat() if ordered_days else None,
        last_session_date=ordered_days[-1].isoformat() if ordered_days else None,
    )

    # Subject share of real study time. Sorted by minutes descending so the
    # "most studied subject" is simply the first entry.
    subjects = [
        SubjectSlice(
            subject=name,
            minutes=round(subject_minutes[name], 1),
            sessions=subject_counts[name],
            percentage=(
                round(subject_minutes[name] / total_minutes * 100, 1)
                if total_minutes > 0
                else 0.0
            ),
        )
        for name in sorted(subject_minutes, key=lambda n: subject_minutes[n], reverse=True)
    ]

    # Chart window. Days with no sessions are present with zero counts so gaps
    # are visible rather than being compressed out of the timeline.
    today = datetime.now().astimezone().date()
    activity = [
        ActivityPoint(
            date=(today - timedelta(days=offset)).isoformat(),
            minutes=round(per_day_minutes.get(today - timedelta(days=offset), 0.0), 1),
            sessions=per_day_counts.get(today - timedelta(days=offset), 0),
        )
        for offset in reversed(range(days))
    ]

    return InsightsResponse(
        has_data=bool(sessions),
        summary=summary,
        subjects=subjects,
        activity=activity,
        activity_days=days,
        peak_hour=max(hourly_minutes, key=lambda h: hourly_minutes[h]) if hourly_minutes else None,
        streak=_calculate_streaks(session_dates),
        fatigue=InsightsFatigue(
            available=False,
            value=None,
            level="Unavailable",
            reason=FATIGUE_UNAVAILABLE_REASON,
        ),
    )


__all__ = ["router"]