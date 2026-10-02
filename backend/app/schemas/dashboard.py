"""
Pydantic schemas for the dashboard endpoint.

`percentage` on StudyProgress and `value` on FatigueLevel are Optional because
the features that would produce them do not exist yet: there is no stored
weekly study goal, and fatigue estimation is not implemented. Sending `null`
lets the frontend render an honest "not available" state instead of a made-up
number. See backend/app/routers/dashboard.py for the matching constants.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class UserInfo(BaseModel):
    name: str
    email: Optional[str] = None


class StudyProgress(BaseModel):
    # None until a weekly goal is stored per user. The frontend shows the
    # `description` on its own when this is None.
    percentage: Optional[int] = None
    description: str


class FatigueLevel(BaseModel):
    label: str
    # None until webcam-based fatigue estimation is implemented.
    value: Optional[int] = None  # 0-100 score
    level: str  # "Unavailable" until fatigue estimation exists
    disclaimer: str


class TimelineItem(BaseModel):
    time: str  # e.g., "7:00 PM", read from the session's real ended_at
    subject: str
    duration: str  # e.g., "45 min"
    kind: str  # study, break, etc.


class RecentSession(BaseModel):
    id: int
    subject: str
    topic: str
    duration: str
    fatigue: str  # "Unavailable" until fatigue estimation exists
    date: str  # e.g., "Sep 28"


class AdaptiveSuggestion(BaseModel):
    title: str
    description: str


class CalendarPreviewItem(BaseModel):
    date: str  # YYYY-MM-DD format
    sessions: int  # number of sessions on this day


class DashboardResponse(BaseModel):
    user: UserInfo
    study_progress: StudyProgress
    fatigue: FatigueLevel
    today_timeline: List[TimelineItem]
    recent_sessions: List[RecentSession]
    adaptive_suggestions: List[AdaptiveSuggestion]
    calendar_preview: List[CalendarPreviewItem]
