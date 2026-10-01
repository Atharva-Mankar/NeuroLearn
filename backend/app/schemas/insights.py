"""
Pydantic schemas for the insights API.
"""
from pydantic import BaseModel
from typing import List, Optional


class Insight(BaseModel):
    title: str
    description: str
    category: str  # e.g. "fatigue", "productivity", "schedule"
    value: str  # display value e.g. "72%"
    trend: str  # e.g. "+8%", "steady", "-3%"
    recommendation: str


class InsightResponse(BaseModel):
    insights: List[Insight]