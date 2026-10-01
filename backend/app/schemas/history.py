"""
Pydantic schemas for the history API.
"""
from pydantic import BaseModel
from typing import List, Optional


class HistorySession(BaseModel):
    id: int
    subject: str
    topic: str
    duration: int  # in minutes
    fatigue: str  # Low, Medium, High
    date: str  # e.g. "Today", "Yesterday", "3 days ago"
    status: str  # completed, abandoned, in_progress


class HistorySummary(BaseModel):
    total_sessions: int
    total_hours: float
    avg_fatigue: str
    avg_duration: int  # in minutes


class HistoryResponse(BaseModel):
    summary: HistorySummary
    sessions: List[HistorySession]