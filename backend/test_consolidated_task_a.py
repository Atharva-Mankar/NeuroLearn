"""Comprehensive verification for Consolidated Task A.

Standalone script -- run with `python test_consolidated_task_a.py` (not pytest).

Covers:
  1. Identity validation: missing / non-integer / unknown X-User-Id is rejected
  2. User A + User B data isolation (list, health, complete)
  3. Session creation writes exactly one row
  4. Completion UPDATEs that same row (no duplicate)
  5. Dashboard is derived from real rows, with honest unavailable states
  6. Real elapsed-duration tracking (server-side started_at -> ended_at)

Uses FastAPI's TestClient so the full HTTP path runs without a live server,
and cleans up only the rows it created so it is safe to re-run.
"""
import sys
import time

sys.path.insert(0, '.')

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import create_database, SessionLocal
from app.models import User, StudySession

create_database()

client = TestClient(app)
failures = []
created_user_ids = []
created_session_ids = []

# Each run creates its own freshly-named accounts. A fixed email would collide
# with a previous run's leftovers, which would make the exact-count assertions
# below depend on whether the script had been run before.
RUN_ID = f"{int(time.time())}"
A_EMAIL = f"taska_a_{RUN_ID}@test.com"
B_EMAIL = f"taska_b_{RUN_ID}@test.com"
A_NAME = "Test User A"
B_NAME = "Test User B"
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


# --------------------------------------------------------------------- #
# 1. Identity validation
# --------------------------------------------------------------------- #
print("\n--- 1. Identity validation ---")

r = client.get("/api/dashboard")
check("Dashboard without X-User-Id returns 400", r.status_code == 400)
check("Missing header gives a sensible message",
      "identity" in body_of(r).get("detail", "").lower())

r = client.get("/api/sessions")
check("Sessions without X-User-Id returns 400", r.status_code == 400)

r = client.get("/api/sessions/999/health")
check("Health without X-User-Id returns 400", r.status_code == 400)

r = client.post("/api/sessions")
check("Create-session without X-User-Id returns 400", r.status_code == 400)

r = client.post("/api/sessions/12345/complete")
check("Complete-session without X-User-Id returns 400", r.status_code == 400)

# Use a real route so the 400 comes from get_current_user, not a route miss.
r = client.get("/api/sessions/1/health", headers={"X-User-Id": "not-an-integer"})
check("X-User-Id that is not an integer returns 400", r.status_code == 400)

r = client.get("/api/sessions/1/health", headers={"X-User-Id": "99999999"})
check("X-User-Id that does not exist in the DB returns 404", r.status_code == 404)
check("Unknown-user 404 does not leak whether the session exists",
      body_of(r).get("detail") == "Unknown user.")


# --------------------------------------------------------------------- #
# 2. User A + User B isolation
# --------------------------------------------------------------------- #
print("\n--- 2. User isolation (User A / User B) ---")

user_a, a_created = ensure_user(A_NAME, A_EMAIL)
check("User A exists (signup or login)", user_a is not None)
user_b, b_created = ensure_user(B_NAME, B_EMAIL)
check("User B exists (signup or login)", user_b is not None)

A_ID = user_a["id"]
B_ID = user_b["id"]
# Only track rows we actually inserted so cleanup never touches pre-existing data
if a_created:
    created_user_ids.append(A_ID)
if b_created:
    created_user_ids.append(B_ID)

check("User A and User B have different IDs", A_ID != B_ID)
check("Database returned the real name for A", user_a["name"] == A_NAME)

# Header values must be strings on the wire, which is what the browser sends.
A_HDR = {"X-User-Id": str(A_ID)}
B_HDR = {"X-User-Id": str(B_ID)}


def start_session(headers, subject, topic, minutes):
    """POST /api/sessions and record the created row for cleanup."""
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
    if r.status_code == 200:
        created_session_ids.append(r.json()["id"])
    return r


r1 = start_session(A_HDR, "Mathematics", "Linear algebra", 60)
check("User A creates session A1 (200)", r1.status_code == 200)
A1 = r1.json()
check("A1 is a real DB record with an id", A1.get("id") is not None)
check("A1 echoes the real subject and planned duration",
      A1["subject"] == "Mathematics" and A1["planned_duration"] == 60)
check("A1 starts with no actual duration yet", A1["actual_duration"] is None)
check("A1 starts as active", A1["status"] == "active")

r2 = start_session(A_HDR, "Data Science", "Pandas", 45)
check("User A creates session A2 (200)", r2.status_code == 200)
A2 = r2.json()

r3 = start_session(B_HDR, "Computer Science", "Algorithms", 90)
check("User B creates session B1 (200)", r3.status_code == 200)
B1 = r3.json()

# User A's list must contain ONLY A1 and A2
r = client.get("/api/sessions", headers=A_HDR)
check("User A GET /api/sessions returns 200", r.status_code == 200)
a_sessions = r.json()
ids_a = [s["id"] for s in a_sessions]
check("User A sees exactly 2 sessions", len(a_sessions) == 2)
check("User A's list is exactly {A1, A2}", sorted(ids_a) == sorted([A1["id"], A2["id"]]))
check("User A does NOT see B1", B1["id"] not in ids_a)

# User B's list must contain ONLY B1
r = client.get("/api/sessions", headers=B_HDR)
check("User B GET /api/sessions returns 200", r.status_code == 200)
b_sessions = r.json()
ids_b = [s["id"] for s in b_sessions]
check("User B sees exactly 1 session", len(b_sessions) == 1)
check("User B's list is exactly {B1}", ids_b == [B1["id"]])
check("User B does NOT see A1 or A2", A1["id"] not in ids_b and A2["id"] not in ids_b)

# --- Ownership enforcement: the DB query filters on user_id, not React ---
r = client.get(f"/api/sessions/{B1['id']}/health", headers=A_HDR)
check("User A GET User B's session health returns 404", r.status_code == 404)

r = client.post(f"/api/sessions/{B1['id']}/complete", headers=A_HDR)
check("User A POST User B's complete returns 404", r.status_code == 404)

r = client.get(f"/api/sessions/{A1['id']}/health", headers=B_HDR)
check("User B GET User A's session health returns 404", r.status_code == 404)

# The rejected completion must not have touched User B's row.
r = client.get(f"/api/sessions/{B1['id']}/health", headers=B_HDR)
check("User B's session is still active after User A's rejected completion",
      r.status_code == 200 and r.json()["is_active"] is True)

# Owner can still reach their own session
r = client.get(f"/api/sessions/{B1['id']}/health", headers=B_HDR)
check("User B can read their own session (200)", r.status_code == 200)
check("Owner's session reports itself active", r.json()["is_active"] is True)


# --------------------------------------------------------------------- #
# 3. Completion updates the SAME record
# --------------------------------------------------------------------- #
print("\n--- 3. Completion updates the same record ---")

db = SessionLocal()
# Scope the count to this run's own users so leftovers from other accounts
# (or an earlier aborted run) cannot influence the no-duplicates check.
own_rows = db.query(StudySession).filter(StudySession.user_id.in_([A_ID, B_ID]))
rows_before = own_rows.count()
check("This run created exactly 3 session rows so far", rows_before == 3)

r = client.post(f"/api/sessions/{A1['id']}/complete", headers=A_HDR)
check("Complete A1 returns 200", r.status_code == 200)
completed = r.json()
check("Completion returns the SAME id as creation", completed["id"] == A1["id"])
check("A1 status is now 'completed'", completed["status"] == "completed")
check("A1 now has a real actual_duration", completed["actual_duration"] is not None)

check("Complete A2 returns 200",
      client.post(f"/api/sessions/{A2['id']}/complete", headers=A_HDR).status_code == 200)
check("Complete B1 returns 200",
      client.post(f"/api/sessions/{B1['id']}/complete", headers=B_HDR).status_code == 200)

rows_after = own_rows.count()
check("No duplicate rows created by completion", rows_after == rows_before)

row_a1 = db.query(StudySession).filter(StudySession.id == A1["id"]).first()
check("A1 is stored as completed with user_id == A",
      row_a1.status == "completed" and row_a1.user_id == A_ID)
check("A1 has an ended_at timestamp", row_a1.ended_at is not None)

# A session can only be completed once
r = client.post(f"/api/sessions/{A1['id']}/complete", headers=A_HDR)
check("Completing an already-completed session is rejected with 400",
      r.status_code == 400)


# --------------------------------------------------------------------- #
# 4. Dashboard is derived from real rows
# --------------------------------------------------------------------- #
print("\n--- 4. Dashboard is derived from real DB data ---")

r = client.get("/api/dashboard", headers=A_HDR)
check("User A dashboard returns 200", r.status_code == 200)
a_dash = r.json()
check("Dashboard user.name is the real name", a_dash["user"]["name"] == A_NAME)
check("Dashboard user.email is the real email", a_dash["user"]["email"] == A_EMAIL)

# No weekly goal is stored, so no percentage may be invented.
check("No hardcoded percentage goal is shown",
      a_dash["study_progress"]["percentage"] is None)
check("Study progress reports real hours from the last 7 days",
      "hours completed in the last 7 days" in a_dash["study_progress"]["description"])
# Sessions ran for seconds, so the honest total is well under the 105 planned
# minutes. If planned duration were being passed off as actual this would read
# "1.8 hours".
check("Study progress does NOT count planned minutes as actual",
      "1.8 hours" not in a_dash["study_progress"]["description"])

check("Fatigue level is 'Unavailable', not a fake 'Medium'",
      a_dash["fatigue"]["level"] == "Unavailable")
check("Fatigue has no fabricated numeric score", a_dash["fatigue"]["value"] is None)
check("Fatigue explains why it is unavailable",
      "not implemented" in a_dash["fatigue"]["disclaimer"].lower())

# Timeline must use real stored timestamps.
check("Timeline only contains today's real sessions",
      all(item["subject"] in ("Mathematics", "Data Science")
          for item in a_dash["today_timeline"]))
for item in a_dash["today_timeline"]:
    check(f"Timeline time {item['time']!r} is not a fabricated 6/8 PM slot",
          item["time"] not in ("6:00 PM", "8:00 PM"))

recent = a_dash["recent_sessions"]
check("Recent sessions contains only A1 and A2",
      len(recent) == 2 and sorted(s["id"] for s in recent) == sorted([A1["id"], A2["id"]]))
for s in recent:
    check("Recent session fatigue states real availability",
          s["fatigue"] == "Unavailable")
    check("Recent session duration is the measured one, not the planned one",
          s["duration"] != "60 min" and s["duration"] != "45 min")

for s in a_dash["adaptive_suggestions"]:
    check("No fabricated 'best focus window' suggestion",
          "best focus" not in (s["title"] + s["description"]).lower())
    check("No fabricated weekly-goal percentage suggestion",
          "%" not in s["title"] and "%" not in s["description"])

check("Calendar preview has 7 entries", len(a_dash["calendar_preview"]) == 7)
today_local = time.strftime("%Y-%m-%d")
check("Calendar counts only the 2 real completed sessions today",
      sum(day["sessions"] for day in a_dash["calendar_preview"]) == 2)


# --------------------------------------------------------------------- #
# 5. User B's dashboard is separate
# --------------------------------------------------------------------- #
print("\n--- 5. User B dashboard is separate ---")

r = client.get("/api/dashboard", headers=B_HDR)
check("User B dashboard returns 200", r.status_code == 200)
b_dash = r.json()
check("User B dashboard shows their own name", b_dash["user"]["name"] == B_NAME)
check("User B dashboard shows their own email", b_dash["user"]["email"] == B_EMAIL)
check("User B's timeline only contains their own subject",
      all(item["subject"] == "Computer Science" for item in b_dash["today_timeline"]))
check("User B's recent sessions contain only B1",
      [s["id"] for s in b_dash["recent_sessions"]] == [B1["id"]])
check("User B's calendar counts only their 1 session",
      sum(day["sessions"] for day in b_dash["calendar_preview"]) == 1)


# --------------------------------------------------------------------- #
# 6. Real elapsed-duration tracking
# --------------------------------------------------------------------- #
print("\n--- 6. Elapsed duration tracking ---")

r = start_session(A_HDR, "Physics", "Mechanics", 50)
check("New session created for the elapsed test", r.status_code == 200)
elapsed_session_id = r.json()["id"]

# A second, untouched session proves elapsed time is measured, not client-supplied.
r = start_session(A_HDR, "Chemistry", "Stoichiometry", 90)
check("Second session created for the elapsed test", r.status_code == 200)
untouched_session_id = r.json()["id"]

time.sleep(2)

r = client.post(f"/api/sessions/{elapsed_session_id}/complete", headers=A_HDR)
check("Completed the elapsed-duration session", r.status_code == 200)
resp = r.json()
check("Response actual_duration is the real elapsed minutes (~0), not the 50 planned",
      resp["actual_duration"] == 0)

row = db.query(StudySession).filter(StudySession.id == elapsed_session_id).first()
check("Session record stores elapsed_seconds", row.elapsed_seconds is not None)
check("Elapsed seconds reflect the ~2s real wait (>1)", row.elapsed_seconds > 1)
check("Elapsed seconds are nowhere near the 50 planned minutes (<=5)",
      row.elapsed_seconds <= 5)

untouched = db.query(StudySession).filter(StudySession.id == untouched_session_id).first()
check("An unfinished session has no elapsed_seconds yet",
      untouched.elapsed_seconds is None)

# While active, health measures live from started_at.
r = client.get(f"/api/sessions/{untouched_session_id}/health", headers=A_HDR)
check("Health endpoint measures live elapsed time for an active session",
      r.status_code == 200 and r.json()["elapsed_seconds"] > 1)

# Once complete, health returns the stored total.
r = client.get(f"/api/sessions/{elapsed_session_id}/health", headers=A_HDR)
check("Health endpoint returns the stored total for a completed session",
      r.json()["elapsed_seconds"] == row.elapsed_seconds)

# History shows planned and actual side by side, never conflated.
r = client.get("/api/sessions", headers=A_HDR)
by_id = {s["id"]: s for s in r.json()}
check("History keeps planned_duration as what the user asked for",
      by_id[elapsed_session_id]["planned_duration"] == 50)
check("History reports actual_duration separately and truthfully",
      by_id[elapsed_session_id]["actual_duration"] == 0)


# --------------------------------------------------------------------- #
# Cleanup -- only rows this run created
# --------------------------------------------------------------------- #
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

print("All Consolidated Task A tests passed!")
