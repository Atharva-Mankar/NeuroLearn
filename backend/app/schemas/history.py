"""
Pydantic schemas for the history API.

``fatigue`` is ``Unavailable`` until webcam-based fatigue estimation is
implemented. The average is therefore also unavailable.
"""
from pydantic import BaseModel
from typing import List, Optional


class HistorySession(BaseModel):
    id: int
    subject: str
    topic: str
    duration: int  # in minutes
    fatigue: str  # "Unavailable" until fatigue estimation exists
    date: str  # ISO format "YYYY-MM-DD"
    status: str  # completed, abandoned, in_progress


class HistorySummary(BaseModel):
    total_sessions: int
    total_hours: float
    avg_fatigue: str  # "Unavailable" until fatigue estimation exists
    avg_duration: int  # in minutes


class HistoryResponse(BaseModel):
    summary: HistorySummary
    sessions: List[HistorySession]