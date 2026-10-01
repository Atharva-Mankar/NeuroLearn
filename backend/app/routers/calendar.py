"""
Calendar API router.

Returns structured calendar/session information suitable for the CalendarPage.
In-memory demo data - would be replaced with database queries later.
"""
from fastapi import APIRouter
from app.schemas.calendar import CalendarResponse, CalendarDay
from datetime import datetime, timedelta


router = APIRouter(prefix="/api", tags=["calendar"])

# Demo calendar data - 30 days ending today
# In production, this would query a database

# September 2026 data (30 days)
_september_2026 = [
    {"date": datetime(2026, 9, 1).date(), "sessions": 1, "subjects": ["Mathematics"], "total_duration": 45},
    {"date": datetime(2026, 9, 2).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 3).date(), "sessions": 2, "subjects": ["Physics", "Chemistry"], "total_duration": 90},
    {"date": datetime(2026, 9, 4).date(), "sessions": 1, "subjects": ["Mathematics"], "total_duration": 45},
    {"date": datetime(2026, 9, 5).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 6).date(), "sessions": 1, "subjects": ["Biology"], "total_duration": 60},
    {"date": datetime(2026, 9, 7).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 8).date(), "sessions": 2, "subjects": ["Mathematics", "Physics"], "total_duration": 80},
    {"date": datetime(2026, 9, 9).date(), "sessions": 1, "subjects": ["Chemistry"], "total_duration": 50},
    {"date": datetime(2026, 9, 10).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 11).date(), "sessions": 1, "subjects": ["Mathematics"], "total_duration": 45},
    {"date": datetime(2026, 9, 12).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 13).date(), "sessions": 2, "subjects": ["Physics", "Biology"], "total_duration": 100},
    {"date": datetime(2026, 9, 14).date(), "sessions": 1, "subjects": ["Chemistry"], "total_duration": 55},
    {"date": datetime(2026, 9, 15).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 16).date(), "sessions": 1, "subjects": ["Mathematics"], "total_duration": 40},
    {"date": datetime(2026, 9, 17).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 18).date(), "sessions": 2, "subjects": ["Physics", "Chemistry"], "total_duration": 95},
    {"date": datetime(2026, 9, 19).date(), "sessions": 1, "subjects": ["Mathematics"], "total_duration": 50},
    {"date": datetime(2026, 9, 20).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 21).date(), "sessions": 1, "subjects": ["Biology"], "total_duration": 65},
    {"date": datetime(2026, 9, 22).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 23).date(), "sessions": 2, "subjects": ["Mathematics", "Physics"], "total_duration": 85},
    {"date": datetime(2026, 9, 24).date(), "sessions": 1, "subjects": ["Chemistry"], "total_duration": 55},
    {"date": datetime(2026, 9, 25).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 26).date(), "sessions": 1, "subjects": ["Mathematics"], "total_duration": 45},
    {"date": datetime(2026, 9, 27).date(), "sessions": 0, "subjects": [], "total_duration": 0},
    {"date": datetime(2026, 9, 28).date(), "sessions": 2, "subjects": ["Physics", "Chemistry"], "total_duration": 90},
    {"date": datetime(2026, 9, 29).date(), "sessions": 1, "subjects": ["Mathematics"], "total_duration": 40},
    {"date": datetime(2026, 9, 30).date(), "sessions": 0, "subjects": [], "total_duration": 0},
]

# October 2026 data (31 days) - based on September data shifted to October plus Oct 31
_october_2026 = []
for day_info in _september_2026:
    _october_2026.append({
        "date": datetime(day_info["date"].year, 10, day_info["date"].day),
        "sessions": day_info["sessions"],
        "subjects": day_info["subjects"],
        "total_duration": day_info["total_duration"],
    })
# Add October 31
_october_2026.append({
    "date": datetime(2026, 10, 31).date(),
    "sessions": 0,
    "subjects": [],
    "total_duration": 0,
})

demo_calendar_data = {
    2026: {
        9: _september_2026,
        10: _october_2026,
    }
}


@router.get("/calendar", response_model=CalendarResponse)
def get_calendar(month: int = 9, year: int = 2026) -> CalendarResponse:
    """
    Get calendar data for a given month.

    Returns structured session information for each day of the month.
    In production, this would query the database for real session data.
    """
    month_data = demo_calendar_data.get(year, {}).get(month, [])
    days = []
    for day_info in month_data:
        days.append(
            CalendarDay(
                date=day_info["date"],
                sessions=day_info["sessions"],
                subjects=day_info.get("subjects", []),
                total_duration=day_info.get("total_duration", 0),
            )
        )
    return CalendarResponse(month=month, year=year, days=days)
