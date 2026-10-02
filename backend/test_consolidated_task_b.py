"""Comprehensive verification for Consolidated Task B.

Standalone script -- run with `python test_consolidated_task_b.py` (not pytest).

Covers:
  1. Identity validation: missing / non-integer / unknown X-User-Id is rejected
  2. Calendar: real per-user DB query, month scoping, empty months
  3. History: real per-user DB query, newest-first, honest fatigue state
  4. Profile: reads from the DB, name update persists across a refetch
  5. Cross-user isolation for all three surfaces

Uses FastAPI's TestClient so the full HTTP path runs without a live server,
and cleans up only the rows it created so it is safe to re-run.

DATE SENSITIVITY
----------------
Calendar tests must not assume the current month has a full complement of
days: run on the 2nd of a month and "3 days ago" lands in the previous one.
Every expectation below is derived from the local dates actually written,
and month-scoped tests use a month chosen to be unambiguously empty
(FEBRUARY 2020) rather than "the previous month".
"""

import sys
import time
from datetime import date, datetime, timedelta

sys.path.insert(0, '.')

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import create_database, SessionLocal
from app.models import User, StudySession
from app.routers.dashboard import _local_date

create_database()

client = TestClient(app)
failures = []
created_user_ids = []
created_session_ids = []

# Each run creates its own freshly-named accounts. A fixed email would collide
# with a previous run's leftovers, which would make the exact-count assertions
# below depend on whether the script had been run before.
RUN_ID = f"{int(time.time())}"
A_EMAIL = f"taskb_a_{RUN_ID}@test.com"
B_EMAIL = f"taskb_b_{RUN_ID}@test.com"
C_EMAIL = f"taskb_c_{RUN_ID}@test.com"
A_NAME = "Task B User A"
B_NAME = "Task B User B"
PASSWD = "TestPass123!"

# A month nobody has ever studied in, used for the "empty calendar" assertions.
EMPTY_MONTH = 2
EMPTY_YEAR = 2020


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

    Returns ``(user, created_by_this_run)``. The flag matters: cleanup may only
    delete rows this run actually inserted. An account that already existed
    belongs to the developer and must survive the test run.
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
        # Login returns {id, name, email} directly, not wrapped in "user"
        return r.json(), False
    return None, False


def start_session(headers, subject, topic, minutes, days_ago=0):
    """Create a session, then backdate ``started_at`` by ``days_ago`` days.

    ``POST /api/sessions`` stamps ``datetime.utcnow()`` itself, so without the
    backdating every session would land on today's date and the calendar's
    per-day grouping could not be exercised at all.

    Returns ``(session_id, local_date)`` -- the date the row was written to,
    which is what the calendar is expected to report it under.
    """
    r = client.post(
        "/api/sessions",
        json={
            "subject": subject,
            "topic": topic,
            "duration_minutes": minutes,
            "webcam_enabled": False,
        },
        headers=headers,
    )
    if r.status_code != 200:
        return None, None

    session_id = r.json()["id"]
    created_session_ids.append(session_id)

    target = datetime.utcnow() - timedelta(days=days_ago)
    db = SessionLocal()
    try:
        row = db.query(StudySession).filter(StudySession.id == session_id).first()
        row.started_at = target
        db.commit()
    finally:
        db.close()

    return session_id, _local_date(target)


def complete_session(session_id, headers):
    """Finish a session so its measured elapsed time is recorded."""
    return client.post(f"/api/sessions/{session_id}/complete", headers=headers)


# --------------------------------------------------------------------- #
# 1. Identity validation
# --------------------------------------------------------------------- #
print("\n--- 1. Identity validation ---")

r = client.get("/api/calendar")
check("Calendar without X-User-Id returns 400", r.status_code == 400)
check("Missing header gives a sensible message",
      "identity" in body_of(r).get("detail", "").lower())

r = client.get("/api/history")
check("History without X-User-Id returns 400", r.status_code == 400)

r = client.get("/api/users/me")
check("Profile without X-User-Id returns 400", r.status_code == 400)

r = client.put("/api/users/me", json={"name": "Test"})
check("Profile update without X-User-Id returns 400", r.status_code == 400)

r = client.get("/api/calendar", headers={"X-User-Id": "not-an-integer"})
check("Calendar with non-integer X-User-Id returns 400", r.status_code == 400)

r = client.get("/api/calendar", headers={"X-User-Id": "99999999"})
check("Calendar with unknown X-User-Id returns 404", r.status_code == 404)
check("Unknown-user 404 does not leak whether data exists",
      body_of(r).get("detail") == "Unknown user.")

# --------------------------------------------------------------------- #
# 2. Set up User A / User B
# --------------------------------------------------------------------- #
print("\n--- 2. User setup (User A / User B) ---")

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
check("Database returned the real name for A", user_a["name"] == A_NAME)

# Header values must be strings on the wire, which is what the browser sends.
A_HDR = {"X-User-Id": str(A_ID)}
B_HDR = {"X-User-Id": str(B_ID)}

# A malformed month is a client error, not a silent empty calendar -- an empty
# result would be indistinguishable from "you studied nothing that month".
# Uses User A's real id so the identity dependency resolves and the query
# validation is what decides the outcome.
r = client.get("/api/calendar?month=99", headers=A_HDR)
check("Out-of-range month is rejected with 422", r.status_code == 422)
r = client.get("/api/calendar?year=abc", headers=A_HDR)
check("Non-numeric year is rejected with 422", r.status_code == 422)

# Three sessions for A, on three different days, all inside the current month.
# Only offsets that stay inside the month are used, so the expectations below
# do not shift depending on what day of the month the script runs on.
today = _local_date(datetime.utcnow())
offsets = [0]
for candidate in (1, 2, 3):
    probe = today - timedelta(days=candidate)
    if probe.month == today.month and probe.year == today.year:
        offsets.append(candidate)
    if len(offsets) == 3:
        break

a_subjects = ["Mathematics", "Physics", "Chemistry"]
a_sessions = []
for subject, offset in zip(a_subjects, offsets):
    sid, sdate = start_session(A_HDR, subject, "Topic", 45, days_ago=offset)
    check(f"User A session created ({subject})", sid is not None)
    a_sessions.append((sid, sdate, subject, offset))

b_sid, b_date = start_session(B_HDR, "Biology", "Cell biology", 60, days_ago=0)


# --------------------------------------------------------------------- #
# 3. Calendar
# --------------------------------------------------------------------- #
print("\n--- 3. Calendar: real per-user DB query ---")

# Every A session must land in the current month.
for sid, sdate, subject, _offset in a_sessions:
    check(f"{subject} was written inside the current month",
          (sdate.year, sdate.month) == (today.year, today.month))

r = client.get(f"/api/calendar?month={today.month}&year={today.year}", headers=A_HDR)
check("User A calendar returns 200", r.status_code == 200)
a_cal = body_of(r)
check("Calendar echoes the requested month/year",
      a_cal.get("month") == today.month and a_cal.get("year") == today.year)

a_days = {day["date"]: day for day in a_cal.get("days", [])}
check("Calendar returns exactly one entry per session-bearing day",
      len(a_days) == len(a_sessions))

for sid, sdate, subject, _offset in a_sessions:
    key = sdate.isoformat()
    check(f"{subject} appears on its real date {key}", key in a_days)
    if key in a_days:
        check(f"{subject} is listed in that day's subjects",
              subject in a_days[key]["subjects"])

check("Every calendar entry is a real date with real counts",
      all(day["sessions"] >= 1 and isinstance(day["total_duration"], int)
          for day in a_days.values()))
check("No demo subjects from the old calendar appear",
      not ({"Biology", "Quantum Mechanics", "Thermodynamics"} & set(a_days)))

# Active sessions report their planned duration, since no elapsed time exists
# yet -- the same rule the history endpoint follows.
a_planned_total = sum(day["total_duration"] for day in a_days.values())
check("Calendar total equals the sum of the planned durations of A's sessions",
      a_planned_total == 45 * len(a_sessions))

# User B sees only their own single session.
r = client.get(f"/api/calendar?month={today.month}&year={today.year}", headers=B_HDR)
b_cal = body_of(r)
check("User B calendar returns 200", r.status_code == 200)
b_days = {day["date"]: day for day in b_cal.get("days", [])}
check("User B sees exactly one day", len(b_days) == 1)
b_key = b_date.isoformat()
check("User B's session is on its real date", b_key in b_days)
check("User B sees their own subject only",
      b_days.get(b_key, {}).get("subjects") == ["Biology"])
check("User B's calendar total is their own planned duration",
      sum(day["total_duration"] for day in b_days.values()) == 60)

# A month nobody studied in is genuinely empty, not zero-filled.
r = client.get(f"/api/calendar?month={EMPTY_MONTH}&year={EMPTY_YEAR}", headers=A_HDR)
check("Unstudied month returns 200", r.status_code == 200)
empty_cal = body_of(r)
check("Unstudied month returns no day entries", empty_cal.get("days") == [])

# The default (no query params) is the current month, not a hardcoded one.
r = client.get("/api/calendar", headers=A_HDR)
default_cal = body_of(r)
check("Calendar with no params defaults to the current month",
      default_cal.get("month") == today.month and default_cal.get("year") == today.year)
check("Default calendar matches the explicitly-requested one",
      default_cal.get("days") == a_cal.get("days"))


# --------------------------------------------------------------------- #
# 4. History
# --------------------------------------------------------------------- #
print("\n--- 4. History: real per-user DB query ---")

r = client.get("/api/history", headers=A_HDR)
check("User A history returns 200", r.status_code == 200)
a_hist = body_of(r)
check("History summary carries all four real statistics",
      {"total_sessions", "total_hours", "avg_fatigue", "avg_duration"}
      <= set(a_hist.get("summary", {})))

a_hist_sessions = a_hist.get("sessions", [])
check("History contains exactly A's sessions",
      len(a_hist_sessions) == len(a_sessions))
check("History contains no session belonging to another user",
      all(s["subject"] in a_subjects for s in a_hist_sessions))

# Newest first: the order must be strictly descending by date.
hist_dates = [s["date"] for s in a_hist_sessions]
check("History is sorted newest first",
      hist_dates == sorted(hist_dates, reverse=True))
check("History's newest entry is A's most recent session",
      hist_dates and hist_dates[0] == max(d.isoformat() for _s, d, _sub, _o in a_sessions))

check("History ids match the sessions that were created",
      sorted(s["id"] for s in a_hist_sessions) == sorted(s[0] for s in a_sessions))

# Every session in HistoryPage's UI needs a subject, topic and ISO date.
check("Every history row has subject/topic/status/date",
      all(s.get("subject") and s.get("topic") and s.get("status")
          and s.get("date") for s in a_hist_sessions))
check("History dates are parseable ISO YYYY-MM-DD",
      all(date.fromisoformat(s["date"]) for s in a_hist_sessions))

# Fatigue does not exist yet, so it must never be reported as a real level.
for s in a_hist_sessions:
    check(f"Session {s['id']} reports fatigue as Unavailable",
          s.get("fatigue") == "Unavailable")
    check(f"Session {s['id']} is not given a fabricated Low/Medium/High level",
          s.get("fatigue") not in ("Low", "Medium", "High"))
check("Summary average fatigue is Unavailable",
      a_hist["summary"]["avg_fatigue"] == "Unavailable")

# An unfinished session has no measured time; reporting the planned duration
# under a plain "duration" field would pass off a plan as study time.
active_rows = [s for s in a_hist_sessions if s["status"] == "active"]
check("A's sessions are still active at this point", len(active_rows) == len(a_sessions))

r = client.get("/api/history", headers=B_HDR)
check("User B history returns 200", r.status_code == 200)
b_hist = body_of(r)
check("User B sees exactly their one session",
      len(b_hist.get("sessions", [])) == 1)
check("User B's session is their own",
      b_hist["sessions"][0]["subject"] == "Biology")
check("User B's history excludes A's subjects",
      all(s["subject"] != "Mathematics" for s in b_hist["sessions"]))

# A brand-new account has an empty history, not fabricated demo rows.
user_c, c_created = ensure_user("Task B User C", C_EMAIL)
check("User C exists (signup or login)", user_c is not None)
if c_created:
    created_user_ids.append(user_c["id"])
C_HDR = {"X-User-Id": str(user_c["id"])}

r = client.get("/api/history", headers=C_HDR)
check("New user's history returns 200", r.status_code == 200)
c_hist = body_of(r)
check("New user has zero sessions", c_hist["summary"]["total_sessions"] == 0)
check("New user's session list is empty", c_hist["sessions"] == [])
check("New user's total_hours is 0.0, not a fabricated figure",
      c_hist["summary"]["total_hours"] == 0.0)
check("New user's avg_duration is 0", c_hist["summary"]["avg_duration"] == 0)
check("New user's avg_fatigue is Unavailable",
      c_hist["summary"]["avg_fatigue"] == "Unavailable")
check("New user's calendar is empty",
      body_of(client.get(f"/api/calendar?month={today.month}&year={today.year}",
                         headers=C_HDR)).get("days") == [])


# --------------------------------------------------------------------- #
# 5. Completed sessions report real elapsed time
# --------------------------------------------------------------------- #
print("\n--- 5. Elapsed time is measured, not planned ---")

# Finish one A session and wait, so elapsed_seconds is genuinely > 0 but far
# below the 45 planned minutes.
done_id = a_sessions[0][0]
time.sleep(2)
r = complete_session(done_id, A_HDR)
check("Completing A's session returns 200", r.status_code == 200)
completed_id = r.json()["id"]

db = SessionLocal()
try:
    row = db.query(StudySession).filter(StudySession.id == completed_id).first()
    elapsed_seconds = row.elapsed_seconds
    check("Completed session stored elapsed_seconds", elapsed_seconds is not None)
    check("Elapsed seconds reflect the real ~2s wait", 1 <= elapsed_seconds <= 10)
    check("Elapsed seconds are nowhere near the 45 planned minutes",
          elapsed_seconds <= 300)
finally:
    db.close()

r = client.get("/api/history", headers=A_HDR)
a_hist2 = body_of(r)
completed_row = next(s for s in a_hist2["sessions"] if s["id"] == completed_id)
check("History reports 0 minutes for a session that ran ~2 seconds",
      completed_row["duration"] == 0)
check("History does NOT report the 45 planned minutes as actual study time",
      completed_row["duration"] != 45)
check("Completed session keeps its 'completed' status",
      completed_row["status"] == "completed")

# The calendar must switch that session from planned to measured time.
r = client.get(f"/api/calendar?month={today.month}&year={today.year}", headers=A_HDR)
a_cal2 = body_of(r)
a_days2 = {day["date"]: day for day in a_cal2["days"]}
completed_date = a_sessions[0][1].isoformat()
check("Completed session's calendar day drops to 0 minutes",
      a_days2[completed_date]["total_duration"] == 0)
check("Calendar still counts the completed session",
      sum(day["sessions"] for day in a_days2.values()) == len(a_sessions))


# --------------------------------------------------------------------- #
# 6. Profile
# --------------------------------------------------------------------- #
print("\n--- 6. Profile: read and update ---")

r = client.get("/api/users/me", headers=A_HDR)
check("Profile read returns 200", r.status_code == 200)
initial_profile = body_of(r)
check("Profile name is the real stored name", initial_profile["name"] == A_NAME)
check("Profile email is the real stored email", initial_profile["email"] == A_EMAIL)
check("Profile exposes account creation time",
      bool(initial_profile.get("created_at")))
check("Profile never exposes the password hash",
      "password_hash" not in initial_profile and "password" not in initial_profile)

new_name = "Renamed Task B User"
r = client.put("/api/users/me", headers=A_HDR, json={"name": new_name})
check("Name update returns 200", r.status_code == 200)
updated_profile = body_of(r)
check("Updated name is echoed back", updated_profile["name"] == new_name)
check("Update leaves the email untouched", updated_profile["email"] == A_EMAIL)
check("Update leaves created_at untouched",
      updated_profile["created_at"] == initial_profile["created_at"])

# Persistence: a fresh request must read the new value from the database, not
# from any cached copy on the server.
r = client.get("/api/users/me", headers=A_HDR)
check("Re-reading the profile returns 200", r.status_code == 200)
refetched = body_of(r)
check("Name update persisted to the database", refetched["name"] == new_name)

db = SessionLocal()
try:
    stored = db.query(User).filter(User.id == A_ID).first()
    check("Database row itself holds the new name", stored.name == new_name)
finally:
    db.close()

# The frontend stores the user in localStorage and sends only the id, so the
# id must not change -- otherwise the app would lose access to its own data.
check("Profile update does not change the user id", refetched["id"] == A_ID)

# Logging in again returns the updated name, proving the change outlives the
# request that made it.
r = client.post("/api/auth/login", json={"email": A_EMAIL, "password": PASSWD})
check("Login after rename returns 200", r.status_code == 200)
check("Login reflects the new name", body_of(r).get("name") == new_name)

# Validation
r = client.put("/api/users/me", headers=A_HDR, json={"name": ""})
check("Empty name is rejected with 422", r.status_code == 422)
r = client.put("/api/users/me", headers=A_HDR, json={"name": "   "})
check("Whitespace-only name is rejected with 422", r.status_code == 422)
r = client.put("/api/users/me", headers=A_HDR, json={"name": "x" * 101})
check("Over-long name is rejected with 422", r.status_code == 422)
r = client.put("/api/users/me", headers=A_HDR, json={})
check("Missing name is rejected with 422", r.status_code == 422)

# The rejected updates must not have written anything.
r = client.get("/api/users/me", headers=A_HDR)
check("Rejected updates left the stored name unchanged",
      body_of(r)["name"] == new_name)

# There is no endpoint that takes a target user id, so one account cannot be
# written through another's identity.
r = client.put("/api/users/me", headers=A_HDR, json={"name": "hijack", "id": B_ID})
r = client.get("/api/users/me", headers=B_HDR)
check("User A's update cannot alter User B's account", body_of(r)["name"] == B_NAME)
check("User B's name is intact after A's update attempt",
      body_of(r)["email"] == B_EMAIL)


# --------------------------------------------------------------------- #
# 7. Cross-user isolation across all three surfaces
# --------------------------------------------------------------------- #
print("\n--- 7. Cross-user isolation ---")

r = client.get("/api/history", headers=A_HDR)
check("User A's history excludes User B's Biology session",
      all(s["subject"] != "Biology" for s in body_of(r)["sessions"]))
check("User A's history excludes User B's session id",
      b_sid not in [s["id"] for s in body_of(r)["sessions"]])

r = client.get("/api/history", headers=B_HDR)
check("User B's history excludes all of User A's sessions",
      all(s["subject"] not in a_subjects for s in body_of(r)["sessions"]))
check("User B's history excludes User A's session ids",
      not ({s[0] for s in a_sessions} & {s["id"] for s in body_of(r)["sessions"]}))

r = client.get(f"/api/calendar?month={today.month}&year={today.year}", headers=B_HDR)
b_days2 = {day["date"]: day for day in body_of(r)["days"]}
check("User B's calendar excludes A's subjects",
      not ({"Mathematics", "Physics", "Chemistry"}
           & {sub for day in b_days2.values() for sub in day["subjects"]}))

r = client.get("/api/users/me", headers=B_HDR)
check("User B's profile is their own", body_of(r)["name"] == B_NAME)
check("User B's profile email is their own", body_of(r)["email"] == B_EMAIL)
r = client.get("/api/users/me", headers=A_HDR)
# A's hijack probe already changed A's name to "hijack"; isolation means A
# cannot be mistaken for B: its profile is not B's, and its email is its own.
check("User A's profile is their own (not User B's)",
      body_of(r)["name"] != B_NAME and body_of(r)["email"] == A_EMAIL)
check("User A's profile email is their own", body_of(r)["email"] == A_EMAIL)


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

print("All Consolidated Task B tests passed!")