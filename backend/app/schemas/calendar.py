"""
Pydantic schemas for the calendar API.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class CalendarDay(BaseModel):
    date: date
    sessions: int
    subjects: List[str] = []
    total_duration: int = 0  # in minutes


class CalendarResponse(BaseModel):
    month: int  # 1-12
    year: int
    days: List[CalendarDay]