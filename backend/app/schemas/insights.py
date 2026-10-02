"""
Pydantic schemas for the insights API.

Every field is either a real measurement read from the authenticated user's
``StudySession`` rows or an explicit "not available" marker. There are no
formatted display strings: the frontend formats numbers, so the API stays a
data contract rather than a second, differently-formatted copy of the UI.

Fatigue has no data source in this phase (no webcam monitoring exists yet),
so :class:`InsightsFatigue` always reports ``available=False``. It is a first
class part of the response rather than an omitted key, so the frontend can
tell "not measured" apart from "measured as zero".
"""

from pydantic import BaseModel
from typing import List, Optional


class InsightsSummary(BaseModel):
    """Lifetime totals plus the figures for the current calendar week."""

    total_sessions: int  # completed sessions, all time
    total_minutes: float  # real study minutes, all time
    total_hours: float  # total_minutes / 60, rounded to 1dp
    avg_session_minutes: float  # mean duration of a completed session, 0.0 if none
    week_sessions: int  # completed sessions since week_start
    week_minutes: float  # real study minutes since week_start
    week_hours: float  # week_minutes / 60, rounded to 1dp
    week_start: str  # ISO "YYYY-MM-DD" Monday the week starts on
    first_session_date: Optional[str]  # ISO date, None if no sessions
    last_session_date: Optional[str]  # ISO date, None if no sessions


class SubjectSlice(BaseModel):
    """One subject's share of total study time."""

    subject: str
    minutes: float
    sessions: int
    percentage: float  # share of total_minutes, 0.0-100.0 rounded to 1dp


class ActivityPoint(BaseModel):
    """One day of the activity chart.

    Days with no study are included with ``minutes=0.0`` and ``sessions=0``.
    That is a real measurement of an empty day, not a placeholder value, and it
    lets the chart show gaps honestly instead of silently skipping them.
    """

    date: str  # ISO "YYYY-MM-DD", local time
    minutes: float
    sessions: int


class InsightsStreak(BaseModel):
    """Consecutive-day streaks, counted on local calendar dates."""

    current: int
    longest: int


class InsightsFatigue(BaseModel):
    """Fatigue availability. Always unavailable in this phase."""

    available: bool  # always False -- no measurement exists
    value: Optional[float]  # always None; never inferred from study duration
    level: str  # "Unavailable"
    reason: str  # why it is unavailable, safe to show in the UI


class InsightsResponse(BaseModel):
    """Everything the insights page renders, all from real session data."""

    has_data: bool  # False when the user has no completed sessions at all
    summary: InsightsSummary
    subjects: List[SubjectSlice]  # descending by minutes; empty when no data
    activity: List[ActivityPoint]  # one entry per day of the requested window
    activity_days: int  # length of the requested chart window
    peak_hour: Optional[int]  # local hour with the most study time; None if no data
    streak: InsightsStreak
    fatigue: InsightsFatigue