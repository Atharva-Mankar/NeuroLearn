"""
History API router.

Returns structured study session history.
In-memory demo data - would be replaced with database queries later.
"""
from fastapi import APIRouter
from app.schemas.history import HistoryResponse, HistorySession, HistorySummary
from typing import List
from datetime import date, timedelta


router = APIRouter(prefix="/api", tags=["history"])

# Demo history data
# `date` is an ISO string (YYYY-MM-DD) so the frontend can sort/parse it.
# Dates are anchored to "today" so the demo always looks current.
def _build_demo_sessions(today: date) -> List[HistorySession]:
    """Build demo sessions with ISO dates anchored to today."""
    raw = [
        (1, "Mathematics", "Linear Algebra", 45, "Low", 0, "completed"),
        (2, "Physics", "Quantum Mechanics", 60, "Medium", 0, "completed"),
        (3, "Chemistry", "Organic Reactions", 30, "Low", 1, "completed"),
        (4, "Biology", "Cell Biology", 55, "Medium", 1, "completed"),
        (5, "Mathematics", "Calculus", 45, "High", 2, "completed"),
        (6, "Physics", "Thermodynamics", 40, "Low", 2, "completed"),
        (7, "Chemistry", "Analytical Chemistry", 50, "Medium", 3, "completed"),
        (8, "Biology", "Genetics", 65, "High", 3, "completed"),
        (9, "Mathematics", "Statistics", 45, "Low", 4, "completed"),
        (10, "Physics", "Electrodynamics", 70, "Medium", 4, "completed"),
    ]
    return [
        HistorySession(
            id=sid,
            subject=subject,
            topic=topic,
            duration=duration,
            fatigue=fatigue,
            date=(today - timedelta(days=days_ago)).isoformat(),
            status=status,
        )
        for sid, subject, topic, duration, fatigue, days_ago, status in raw
    ]


@router.get("/history", response_model=HistoryResponse)
def get_history() -> HistoryResponse:
    """
    Get study session history.
    Returns all past sessions with summary statistics.
    In production, this would query the database for real session records.
    """
    sessions = _build_demo_sessions(date.today())
    total_sessions = len(sessions)
    total_minutes = sum(s.duration for s in sessions)
    total_hours = round(total_minutes / 60, 1)
    avg_duration = round(total_minutes / total_sessions) if total_sessions else 0

    # Calculate average fatigue (simple mapping)
    fatigue_scores = {"Low": 1, "Medium": 2, "High": 3}
    avg_score = sum(fatigue_scores.get(s.fatigue, 2) for s in sessions) / total_sessions if total_sessions else 0
    avg_fatigue = "Low" if avg_score < 1.5 else "Medium" if avg_score < 2.5 else "High"

    summary = HistorySummary(
        total_sessions=total_sessions,
        total_hours=total_hours,
        avg_fatigue=avg_fatigue,
        avg_duration=avg_duration,
    )

    return HistoryResponse(summary=summary, sessions=sessions)