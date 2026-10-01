"""
Insights API router.

Returns structured insight information.
In-memory demo data - would be replaced with database queries later.
"""
from fastapi import APIRouter
from app.schemas.insights import InsightResponse, Insight


router = APIRouter(prefix="/api", tags=["insights"])

# Demo insights data
demo_insights = [
    Insight(
        title="Average Focus Duration",
        description="Your average focused study session length over the past week",
        category="productivity",
        value="48 min",
        trend="+5 min",
        recommendation="Try extending your sessions by 5-10 minutes to build endurance"
    ),
    Insight(
        title="Peak Productivity Hours",
        description="When you tend to have the highest focus and lowest fatigue",
        category="schedule",
        value="9:00-11:00 AM",
        trend="steady",
        recommendation="Schedule your most challenging subjects during this window"
    ),
    Insight(
        title="Fatigue Level Trend",
        description="How your average fatigue level has changed over time",
        category="fatigue",
        value="Low",
        trend="improving",
        recommendation="Maintain your current break schedule and hydration habits"
    ),
    Insight(
        title="Subject Distribution",
        description="Breakdown of your study time by subject this month",
        category="productivity",
        value="Math: 30%, Physics: 25%, Chemistry: 20%, Biology: 15%, Other: 10%",
        trend="balanced",
        recommendation="Consider allocating more time to weaker subjects for balanced progress"
    ),
    Insight(
        title="Weekly Consistency",
        description="How regularly you've been studying compared to your goals",
        category="schedule",
        value="72%",
        trend="+8%",
        recommendation="Aim for at least 4 sessions per week to maintain momentum"
    ),
]


@router.get("/insights", response_model=InsightResponse)
def get_insights() -> InsightResponse:
    """
    Get personalized insights and recommendations.
    Returns actionable insights based on study patterns.
    In production, this would analyze real session data from the database.
    """
    return InsightResponse(insights=demo_insights)