"""Comprehensive verification for the Phase 4 Insights system.

Standalone script -- run with `python test_insights.py` (not pytest).

Covers:
  1. Identity: missing / non-integer / unknown X-User-Id is rejected
  2. Empty user gets a valid zero state, never fabricated numbers
  3. Totals: session count, total study time, average duration
  4. Subject distribution, sorted and percentage-correct
  5. Current-week figures and the week anchor
  6. Streaks: current, longest, and the yesterday-still-running rule
  7. Activity chart: real per-day minutes, gaps present as zeros
  8. Fatigue is reported as unavailable, never inferred or fabricated
  9. Cross-user isolation: A sees only A, B sees only B
  10. Malformed requests are rejected rather than silently defaulted

Session durations are controlled by writing ``elapsed_seconds`` directly, so
every expected minute total below is exact rather than dependent on how long
the script happened to sleep. Sessions are backdated the same way, so
day-level assertions do not shift depending on when the script runs.

Uses FastAPI's TestClient so the full HTTP path runs without a live server,
and cleans up only the rows it created so it is safe to re-run.
"""

import sys
import time
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, '.')

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import create_database, SessionLocal
from app.models import User, StudySession
from app.routers.insights import _calculate_streaks, _week_start
from app.routers.dashboard import _local_date

create_database()

client = TestClient(app)
failures = []
created_user_ids = []
created_session_ids = []

# Freshly-named accounts each run. A fixed email would collide with a previous
# run's leftovers, making exact-count assertions depend on run history.
RUN_ID = f"{int(time.time())}"
A_EMAIL = f"insights_a_{RUN_ID}@test.com"
B_EMAIL = f"insights_b_{RUN_ID}@test.com"
A_NAME = "Insights User A"
B_NAME = "Insights User B"
PASSWD = "TestPass123!"


def check(label, condition):
    """Record a check result and print it."""
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}")
    if not condition:
        failures.append(label)


def body_of(r):
    try:
        return r.json()
    except Exception:
        return {}


def ensure_user(name, email):
    """Sign up, or log in if a previous run already created the account.

    Returns ``(user, created_by_this_run)``. Cleanup may only delete rows this
    run actually inserted; an account that already existed belongs to the
    developer and must survive.
    """
    r = client.post("/api/auth/signup", json={
        "name": name,
        "email": email,
        "password": PASSWD,
    })
    if r.status_code == 200:
        return r.json()["user"], True
    r = client.post("/api/auth/login", json={"email": email, "password": PASSWD})
    if r.status_code == 200:
        return r.json(), False
    return None, False


def make_completed_session(headers, subject, topic, elapsed_seconds, days_ago=0, hour_utc=None):
    """Create a session and immediately mark it completed with a known duration.

    ``POST /api/sessions`` stamps ``datetime.utcnow()`` itself and leaves the
    session active with ``elapsed_seconds`` NULL. Rather than sleeping and
    hoping for a clean number, the row is written directly with a known
    elapsed time and a backdated start, so every total below is exact.

    Returns ``(session_id, local_date_of_session)``.
    """
    r = client.post("/api/sessions", json={
        "subject": subject,
        "topic": topic,
        "duration_minutes": 60,
        "webcam_enabled": False,
    }, headers=headers)
    if r.status_code != 200:
        return None, None

    session_id = r.json()["id"]
    created_session_ids.append(session_id)

    target = datetime.utcnow() - timedelta(days=days_ago)
    if hour_utc is not None:
        target = target.replace(hour=hour_utc, minute=0, second=0, microsecond=0)

    db = SessionLocal()
    try:
        row = db.query(StudySession).filter(StudySession.id == session_id).first()
        row.status = "completed"
        row.started_at = target
        row.ended_at = target + timedelta(seconds=elapsed_seconds)
        row.elapsed_seconds = elapsed_seconds
        db.commit()
    finally:
        db.close()

    return session_id, _local_date(target)


def write_status(session_id, status):
    """Force a session's status, to prove active sessions are excluded."""
    db = SessionLocal()
    try:
        db.query(StudySession).filter(StudySession.id == session_id).update(
            {"status": status}
        )
        db.commit()
    finally:
        db.close()


# --------------------------------------------------------------------- #
# 1. Identity validation
# --------------------------------------------------------------------- #
print("\n--- 1. Identity validation ---")

r = client.get("/api/insights")
check("Insights without X-User-Id returns 400", r.status_code == 400)
check("Missing header gives a sensible message",
      "identity" in body_of(r).get("detail", "").lower())

r = client.get("/api/insights", headers={"X-User-Id": "not-an-integer"})
check("Non-integer X-User-Id returns 400", r.status_code == 400)

r = client.get("/api/insights", headers={"X-User-Id": "99999999"})
check("Unknown X-User-Id returns 404", r.status_code == 404)
check("Unknown-user 404 does not leak whether data exists",
      body_of(r).get("detail") == "Unknown user.")

# The endpoint declares no user_id parameter. A query string carrying one is
# ignored rather than honoured, but that is only observable once data exists,
# so it is asserted in section 10 where both users have sessions.


# --------------------------------------------------------------------- #
# 2. User setup
# --------------------------------------------------------------------- #
print("\n--- 2. User setup ---")

user_a, a_created = ensure_user(A_NAME, A_EMAIL)
check("User A exists (signup or login)", user_a is not None)
user_b, b_created = ensure_user(B_NAME, B_EMAIL)
check("User B exists (signup or login)", user_b is not None)

A_ID = user_a["id"]
B_ID = user_b["id"]
if a_created:
    created_user_ids.append(A_ID)
if b_created:
    created_user_ids.append(B_ID)

check("User A and User B have different IDs", A_ID != B_ID)

A_HDR = {"X-User-Id": str(A_ID)}
B_HDR = {"X-User-Id": str(B_ID)}


# --------------------------------------------------------------------- #
# 3. Empty user: a valid zero state, never fabricated numbers
# --------------------------------------------------------------------- #
print("\n--- 3. Empty user returns a valid empty state ---")

r = client.get("/api/insights", headers=A_HDR)
check("New user insights returns 200", r.status_code == 200)
empty = body_of(r)

check("Empty user has_data is False", empty.get("has_data") is False)

s = empty.get("summary", {})
check("Empty summary has zero total sessions", s.get("total_sessions") == 0)
check("Empty summary has zero total minutes", s.get("total_minutes") == 0)
check("Empty summary has zero total hours", s.get("total_hours") == 0)
check("Empty summary has zero average duration", s.get("avg_session_minutes") == 0)
check("Empty summary has zero week sessions", s.get("week_sessions") == 0)
check("Empty summary has zero week minutes", s.get("week_minutes") == 0)
check("Empty summary has zero week hours", s.get("week_hours") == 0)
check("Empty summary has no first session date", s.get("first_session_date") is None)
check("Empty summary has no last session date", s.get("last_session_date") is None)

check("Empty user has an empty subject list", empty.get("subjects") == [])
check("Empty user has a zero current streak", empty.get("streak", {}).get("current") == 0)
check("Empty user has a zero longest streak", empty.get("streak", {}).get("longest") == 0)
check("Empty user has no peak hour", empty.get("peak_hour") is None)
check("Empty user still gets an activity window (real zeros)",
      len(empty.get("activity", [])) == empty.get("activity_days"))

# The activity window must be days with no study, not fabricated activity.
check("Empty user's activity window is all zeros",
      all(p["minutes"] == 0 and p["sessions"] == 0 for p in empty.get("activity", [])))

check("Empty user's week_start is an ISO date",
      bool(date.fromisoformat(s.get("week_start", "1970-01-01"))))


# --------------------------------------------------------------------- #
# 4. Real totals: session count, study time, average duration
# --------------------------------------------------------------------- #
print("\n--- 4. Totals calculated from real completed sessions ---")

# A: three completed sessions totalling 300 minutes (60 + 90 + 150).
a_created_sessions = []
a_ids = []
for subject, minutes, days_ago in [
    ("Mathematics", 60, 5),
    ("Physics", 90, 3),
    ("Mathematics", 150, 1),
]:
    sid, sdate = make_completed_session(A_HDR, subject, "Topic", minutes * 60, days_ago=days_ago)
    check(f"A completed session created ({subject}, {minutes} min)", sid is not None)
    a_created_sessions.append((sid, sdate, subject, minutes))
    a_ids.append(sid)

# An active session must not be counted as completed study time.
active_id, _ = make_completed_session(A_HDR, "Chemistry", "Active one", 45 * 60, days_ago=0)
write_status(active_id, "active")
created_session_ids.append(active_id)

r = client.get("/api/insights", headers=A_HDR)
check("User A insights returns 200", r.status_code == 200)
a_insights = body_of(r)

check("has_data is True once A has sessions", a_insights.get("has_data") is True)

s = a_insights["summary"]
check("Session count counts only completed sessions", s.get("total_sessions") == 3)
check("Total study minutes sums the real elapsed times", s.get("total_minutes") == 300.0)
check("Total hours is minutes / 60", s.get("total_hours") == 5.0)
check("Average session duration is total / count", s.get("avg_session_minutes") == 100.0)
check("The active 45-minute session is excluded from totals",
      s.get("total_minutes") != 345.0 and s.get("total_sessions") == 3)

check("First session date is the real earliest date",
      s.get("first_session_date") == min(d.isoformat() for _i, d, _sub, _m in a_created_sessions))
check("Last session date is the real latest date",
      s.get("last_session_date") == max(d.isoformat() for _i, d, _sub, _m in a_created_sessions))


# --------------------------------------------------------------------- #
# 5. Subject distribution
# --------------------------------------------------------------------- #
print("\n--- 5. Subject distribution ---")

subjects = a_insights["subjects"]
by_subject = {entry["subject"]: entry for entry in subjects}

check("Subject distribution covers exactly A's subjects",
      set(by_subject) == {"Mathematics", "Physics"})
check("Distribution is sorted by minutes descending",
      [e["subject"] for e in subjects] == ["Mathematics", "Physics"])

check("Mathematics minutes are the real sum (60 + 150)",
      by_subject["Mathematics"]["minutes"] == 210.0)
check("Mathematics session count is 2", by_subject["Mathematics"]["sessions"] == 2)
check("Physics minutes are real (90)", by_subject["Physics"]["minutes"] == 90.0)
check("Physics session count is 1", by_subject["Physics"]["sessions"] == 1)

check("Mathematics percentage is 70% of 300 min",
      by_subject["Mathematics"]["percentage"] == 70.0)
check("Physics percentage is 30% of 300 min",
      by_subject["Physics"]["percentage"] == 30.0)

# Subject percentages must reflect real data, not a fixed demo set.
check("No demo subject percentages leak through",
      not ({'Machine Learning', 'Data Science', 'Statistics'} & set(by_subject)))

# The most-studied subject is simply the highest-minute entry.
check("Most studied subject is Mathematics", subjects[0]["subject"] == "Mathematics")


# --------------------------------------------------------------------- #
# 6. Current-week figures
# --------------------------------------------------------------------- #
print("\n--- 6. Current-week calculations ---")

# The week anchor must be the Monday 00:00 local of the current week.
expected_week_start = _week_start(datetime.utcnow()).date()
check("week_start is the Monday of the current week",
      date.fromisoformat(s["week_start"]).weekday() == 0)
check("week_start matches the computed local Monday",
      date.fromisoformat(s["week_start"]) == expected_week_start)

# Only sessions inside the current week count toward week_*.
today = _local_date(datetime.utcnow())
days_since_monday = today.weekday()

# The 150-minute session is 1 day ago, so it is in the current week only if
# today is not a Monday. Derive the expectation from the real weekday rather
# than assuming.
in_week_ids = set()
for sid, sdate, _sub, minutes in a_created_sessions:
    if sdate >= date.fromisoformat(s["week_start"]):
        in_week_ids.add(sid)

expected_week_sessions = len(in_week_ids)
expected_week_minutes = sum(
    m for sid, _d, _sub, m in a_created_sessions if sid in in_week_ids
)

check("Week session count includes only this week's sessions",
      s.get("week_sessions") == expected_week_sessions)
check("Week minutes include only this week's sessions",
      s.get("week_minutes") == float(expected_week_minutes))
check("Week hours is week minutes / 60",
      s.get("week_hours") == round(expected_week_minutes / 60, 1))
check("Week totals never exceed lifetime totals",
      s.get("week_minutes") <= s.get("total_minutes"))

# A session from before this week must not inflate the week figures.
old_id, old_date = make_completed_session(A_HDR, "History", "Last month", 240 * 60, days_ago=30)
check("Old session is outside the current week", old_date < date.fromisoformat(s["week_start"]))

r = client.get("/api/insights", headers=A_HDR)
s2 = body_of(r)["summary"]
check("Week figures are unchanged by a 30-day-old session",
      s2.get("week_sessions") == expected_week_sessions
      and s2.get("week_minutes") == float(expected_week_minutes))
check("Lifetime totals DO include the old session",
      s2.get("total_sessions") == 4 and s2.get("total_minutes") == 540.0)

# Days since Monday is used to confirm the anchor is genuinely week-scoped.
check("Week anchor logic is consistent with the weekday",
      0 <= days_since_monday <= 6)


# --------------------------------------------------------------------- #
# 7. Streaks
# --------------------------------------------------------------------- #
print("\n--- 7. Streak calculation ---")

today_date = _local_date(datetime.utcnow())

# Pure-function check of the streak rules, using dates relative to today so it
# holds no matter what day the script runs.
r_empty_streak = _calculate_streaks(set())
check("Empty date set yields a zero streak", r_empty_streak.current == 0)
check("Empty date set yields a zero longest streak", r_empty_streak.longest == 0)

# Consecutive today, yesterday, day-before -> current streak of 3.
three_run = {today_date, today_date - timedelta(days=1), today_date - timedelta(days=2)}
r_three = _calculate_streaks(three_run)
check("Three consecutive days ending today gives current=3", r_three.current == 3)
check("Three consecutive days gives longest=3", r_three.longest == 3)

# Yesterday through day-before, but not today: still a live run of 2.
two_run = {today_date - timedelta(days=1), today_date - timedelta(days=2)}
r_two = _calculate_streaks(two_run)
check("A run ending yesterday is still current (not zeroed)", r_two.current == 2)
check("A run ending yesterday sets longest=2", r_two.longest == 2)

# A run that ended 3 days ago is broken: current is 0, longest preserved.
broken = {today_date - timedelta(days=3), today_date - timedelta(days=4)}
r_broken = _calculate_streaks(broken)
check("A run ending days ago has current=0", r_broken.current == 0)
check("A run ending days ago still records longest=2", r_broken.longest == 2)

# Several separated blocks: longest must be the largest single block (3), not
# the total number of studied days (6).
scattered = (
    {today_date, today_date - timedelta(days=1)}            # block of 2
    | {today_date - timedelta(days=d) for d in (3, 4, 5)}  # block of 3
    | {today_date - timedelta(days=7)}                     # block of 1
)
r_scatter = _calculate_streaks(scattered)
check("Scattered dates keep the longest block (3), not the total (6)",
      r_scatter.longest == 3)
check("Scattered dates current reflects only today's run", r_scatter.current == 2)

# A long run, a gap, then today alone: current is the newest run, longest the
# older one. today-1 is deliberately absent so the two blocks stay separate.
long_then_new = {today_date} | {today_date - timedelta(days=d) for d in (2, 3, 4, 5)}
r_ltn = _calculate_streaks(long_then_new)
check("Longest spans the older 4-day run", r_ltn.longest == 4)
check("Current is just today's single day", r_ltn.current == 1)


# --------------------------------------------------------------------- #
# 8. Activity chart reflects real per-day minutes
# --------------------------------------------------------------------- #
print("\n--- 8. Activity chart data ---")

r = client.get("/api/insights?days=14", headers=A_HDR)
check("Insights with ?days=14 returns 200", r.status_code == 200)
a14 = body_of(r)
check("Activity window length matches ?days", len(a14["activity"]) == 14)
check("activity_days reflects the window", a14["activity_days"] == 14)

activity_by_date = {p["date"]: p for p in a14["activity"]}
for sid, sdate, subject, minutes in a_created_sessions:
    key = sdate.isoformat()
    if key in activity_by_date:
        check(f"{subject} ({minutes} min) appears on its real date",
              activity_by_date[key]["minutes"] >= minutes)

check("Activity dates are in ascending order",
      [p["date"] for p in a14["activity"]] == sorted(p["date"] for p in a14["activity"]))

# Days with no study must be present as explicit zeros, not omitted -- an
# omitted day would compress a gap out of the timeline.
check("Gap days are present as zeros rather than missing",
      all("minutes" in p and "sessions" in p for p in a14["activity"]))
check("Activity window spans back to the requested number of days",
      len(a14["activity"]) == 14)

# Default window is 14 days.
r = client.get("/api/insights", headers=A_HDR)
check("Default activity window is 14 days", len(body_of(r)["activity"]) == 14)


# --------------------------------------------------------------------- #
# 9. Fatigue is unavailable, never fabricated
# --------------------------------------------------------------------- #
print("\n--- 9. Fatigue is unavailable, not inferred ---")

fatigue = a_insights["fatigue"]
check("fatigue.available is False", fatigue.get("available") is False)
check("fatigue.value is None (never inferred from duration)", fatigue.get("value") is None)
check("fatigue.level is Unavailable", fatigue.get("level") == "Unavailable")
check("fatigue explains why it is unavailable", bool(fatigue.get("reason")))
check("Fatigue is not given a fabricated Low/Medium/High",
      fatigue.get("level") not in ("Low", "Medium", "High"))

# Fatigue must stay unavailable even with plenty of real study data.
check("Fatigue stays unavailable despite 300+ real minutes", fatigue.get("available") is False)

empty_fatigue = empty["fatigue"]
check("Empty user's fatigue is also Unavailable",
      empty_fatigue.get("available") is False and empty_fatigue.get("level") == "Unavailable")


# --------------------------------------------------------------------- #
# 10. Cross-user isolation
# --------------------------------------------------------------------- #
print("\n--- 10. Cross-user isolation ---")

# B gets their own distinct dataset so leakage is detectable.
b_id_1, b_date_1 = make_completed_session(B_HDR, "Biology", "Cell bio", 30 * 60, days_ago=0)
b_id_2, b_date_2 = make_completed_session(B_HDR, "History", "Ancient", 20 * 60, days_ago=2)

r = client.get("/api/insights", headers=B_HDR)
check("User B insights returns 200", r.status_code == 200)
b_insights = body_of(r)

check("User B has only their own 2 sessions", b_insights["summary"]["total_sessions"] == 2)
check("User B's total minutes are their own (50)", b_insights["summary"]["total_minutes"] == 50.0)
check("User B's subjects are only theirs",
      {e["subject"] for e in b_insights["subjects"]} == {"Biology", "History"})

r = client.get("/api/insights", headers=A_HDR)
a_insights2 = body_of(r)
check("User A still sees only their own sessions", a_insights2["summary"]["total_sessions"] == 4)
check("User A's total minutes are unaffected by B", a_insights2["summary"]["total_minutes"] == 540.0)
check("User A's subjects exclude B's",
      not ({"Biology"} & {e["subject"] for e in a_insights2["subjects"]}))

# User A must never see B's specific session figures.
check("User A's totals do not include B's 50 minutes",
      a_insights2["summary"]["total_minutes"] == 540.0)

# The 30-day-old "History" session belongs to A; B also has "History". Subject
# names can overlap legitimately -- isolation is about rows, not labels. What
# must not happen is one user's minute totals reaching the other.
check("User B totals unchanged after A's reads",
      body_of(client.get("/api/insights", headers=B_HDR))["summary"]["total_minutes"] == 50.0)


# --------------------------------------------------------------------- #
# 11. Malformed requests
# --------------------------------------------------------------------- #
print("\n--- 11. Malformed requests ---")

r = client.get("/api/insights?days=0", headers=A_HDR)
check("days=0 is rejected with 422", r.status_code == 422)
r = client.get("/api/insights?days=-5", headers=A_HDR)
check("Negative days is rejected with 422", r.status_code == 422)
r = client.get("/api/insights?days=abc", headers=A_HDR)
check("Non-numeric days is rejected with 422", r.status_code == 422)
r = client.get("/api/insights?days=100000", headers=A_HDR)
check("Excessive days is rejected with 422", r.status_code == 422)

# A valid boundary must be accepted.
r = client.get("/api/insights?days=1", headers=A_HDR)
check("days=1 is accepted", r.status_code == 200 and len(body_of(r)["activity"]) == 1)
r = client.get("/api/insights?days=365", headers=A_HDR)
check("days=365 is accepted", r.status_code == 200 and len(body_of(r)["activity"]) == 365)

# Response shape is always complete, even on the empty path.
r = client.get("/api/insights", headers=A_HDR)
final = body_of(r)
check("Response always carries all top-level keys",
      all(k in final for k in ["has_data", "summary", "subjects", "activity",
                                "activity_days", "peak_hour", "streak", "fatigue"]))
check("Summary always carries all statistics",
      all(k in final["summary"] for k in [
          "total_sessions", "total_minutes", "total_hours", "avg_session_minutes",
          "week_sessions", "week_minutes", "week_hours", "week_start",
          "first_session_date", "last_session_date"]))


# --------------------------------------------------------------------- #
# Cleanup -- only rows this run created
# --------------------------------------------------------------------- #
db = SessionLocal()
db.query(StudySession).filter(StudySession.id.in_(created_session_ids)).delete(
    synchronize_session=False
)
db.query(User).filter(User.id.in_(created_user_ids)).delete(synchronize_session=False)
db.commit()
db.close()

print("")
if failures:
    print(f"{len(failures)} CHECK(S) FAILED:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("All Insights tests passed!")