"""
Pydantic schemas for the dashboard endpoint.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class UserInfo(BaseModel):
    name: str
    email: Optional[str] = None


class StudyProgress(BaseModel):
    percentage: int
    description: str


class FatigueLevel(BaseModel):
    label: str
    value: int  # 0-100 score
    level: str  # Low, Medium, High
    disclaimer: str


class TimelineItem(BaseModel):
    time: str  # e.g., "7:00 PM"
    subject: str
    duration: str  # e.g., "45 min"
    kind: str  # study, break, etc.


class RecentSession(BaseModel):
    id: int
    subject: str
    topic: str
    duration: str
    fatigue: str  # Low, Medium, High
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