"""
Dashboard API router.

Returns demo data for the NeuroLearn dashboard. In a later phase, this will
pull real data from the database and adapt recommendations based on the user's
fatigue history and study patterns.
"""
from fastapi import APIRouter
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

router = APIRouter(prefix="/api", tags=["dashboard"])

# Demo data - matches the frontend demoData.js structure
FATIGUE_DISCLAIMER = "An approximate study-productivity signal, not a medical diagnosis."


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard() -> DashboardResponse:
    """
    Get dashboard data for the current user.

    Returns demo data for Phase 3. In Phase 4+, this will:
    - Fetch the authenticated user's profile
    - Calculate real study progress from completed sessions
    - Estimate fatigue from webcam analysis (when enabled)
    - Generate adaptive recommendations from the scheduler
    - Pull calendar events from the database
    """
    return DashboardResponse(
        user=UserInfo(
            name="Atharva",
            email="atharva@example.com"
        ),
        study_progress=StudyProgress(
            percentage=68,
            description="8.5 of 12.5 hours this week"
        ),
        fatigue=FatigueLevel(
            label="Estimated fatigue",
            value=52,  # 0-100 score for visualization
            level="Medium",
            disclaimer=FATIGUE_DISCLAIMER
        ),
        today_timeline=[
            TimelineItem(time="7:00 PM", subject="Machine Learning", duration="45 min", kind="study"),
            TimelineItem(time="8:00 PM", subject="Data Science", duration="30 min", kind="study"),
            TimelineItem(time="9:00 PM", subject="Break", duration="15 min", kind="break"),
            TimelineItem(time="9:30 PM", subject="Review notes", duration="20 min", kind="study"),
        ],
        recent_sessions=[
            RecentSession(
                id=1,
                subject="Machine Learning",
                topic="Neural networks",
                duration="45 min",
                fatigue="Low",
                date="Sep 28"
            ),
            RecentSession(
                id=2,
                subject="Data Science",
                topic="Pandas and NumPy",
                duration="30 min",
                fatigue="Medium",
                date="Sep 27"
            ),
            RecentSession(
                id=3,
                subject="Mathematics",
                topic="Linear algebra",
                duration="60 min",
                fatigue="High",
                date="Sep 26"
            ),
            RecentSession(
                id=4,
                subject="Computer Vision",
                topic="OpenCV basics",
                duration="40 min",
                fatigue="Low",
                date="Sep 25"
            ),
        ],
        adaptive_suggestions=[
            AdaptiveSuggestion(
                title="Take a short break first",
                description="Your estimated fatigue is medium, and your last two sessions were back to back."
            ),
            AdaptiveSuggestion(
                title="Best focus window is 7-9 PM",
                description="Across your recent history, sessions in this window ended with the lowest fatigue estimate."
            ),
            AdaptiveSuggestion(
                title="One session from your weekly goal",
                description="You are at 68% of this week's study target with four days remaining."
            ),
        ],
        calendar_preview=[
            CalendarPreviewItem(date="2026-09-28", sessions=3),
            CalendarPreviewItem(date="2026-09-27", sessions=1),
            CalendarPreviewItem(date="2026-09-26", sessions=1),
            CalendarPreviewItem(date="2026-09-25", sessions=1),
            CalendarPreviewItem(date="2026-09-24", sessions=1),
            CalendarPreviewItem(date="2026-09-23", sessions=1),
            CalendarPreviewItem(date="2026-09-22", sessions=1),
        ]
    )
