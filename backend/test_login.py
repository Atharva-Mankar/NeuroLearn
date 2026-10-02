"""Focused, repeatable verification for the real login endpoint.

Uses FastAPI's TestClient so the full HTTP path (validation, routing, error
handling) is exercised without needing a running server. Cleans up the users it
creates, so it can be re-run safely.
"""

import sys
sys.path.insert(0, '.')

from fastapi.testclient import TestClient

print("Testing imports...")
try:
    from app.main import app
    from app.database.connection import create_database, SessionLocal
    from app.models import User
    from app.routers.auth import verify_password
    print("All imports successful")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Emails used by this script. Both are exact-match cleanup targets.
TEST_EMAIL = "logintest@example.com"
MIXED_CASE_EMAIL = "MixedCaseLogin@Example.COM"
TEST_PASSWORD = "logintestpass123"
WRONG_PASSWORD = "totallywrongpass123"

create_database()

# Remove leftovers from any previous run so this test is repeatable
db = SessionLocal()
db.query(User).filter(User.email == TEST_EMAIL).delete()
db.query(User).filter(User.email == MIXED_CASE_EMAIL.lower()).delete()
db.commit()
db.close()
print(f"\nCleared leftover test users ({TEST_EMAIL}, {MIXED_CASE_EMAIL.lower()})")

client = TestClient(app)
failures = []


def check(label, condition):
    """Record a check result and print it."""
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}")
    if not condition:
        failures.append(label)


print("\n--- A/B: signup then login with correct credentials ---")
r = client.post("/api/auth/signup", json={
    "name": "Login Test User",
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD,
})
check("Signup returns 200", r.status_code == 200)

r = client.post("/api/auth/login", json={
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD,
})
check("Valid login returns 200", r.status_code == 200)
body = r.json()
check("Response contains id", "id" in body)
check("Response contains name", "name" in body)
check("Response contains email", "email" in body)
check("Response does NOT contain password", "password" not in body)
check("Response does NOT contain password_hash", "password_hash" not in body)
check("Response email matches", body.get("email") == TEST_EMAIL)

print("\n--- B: wrong password ---")
r = client.post("/api/auth/login", json={
    "email": TEST_EMAIL,
    "password": WRONG_PASSWORD,
})
check("Wrong password returns 401", r.status_code == 401)
check("Wrong password returns generic message",
      r.json().get("detail") == "Invalid email or password.")

print("\n--- C: unknown email ---")
r = client.post("/api/auth/login", json={
    "email": "nosuchuser@example.com",
    "password": TEST_PASSWORD,
})
check("Unknown email returns 401", r.status_code == 401)
unknown_body = r.json()
check("Unknown email returns generic message",
      unknown_body.get("detail") == "Invalid email or password.")

# The two failure paths must be indistinguishable to the caller
wrong_pw_body = {"detail": "Invalid email or password."}
check("Unknown email and wrong password responses are identical",
      unknown_body == wrong_pw_body)

print("\n--- D: email case normalization ---")
# Sign up with a mixed-case email
r = client.post("/api/auth/signup", json={
    "name": "Mixed Case User",
    "email": MIXED_CASE_EMAIL,
    "password": TEST_PASSWORD,
})
check("Mixed-case signup returns 200", r.status_code == 200)

# Log in with a different case than it was registered with
r = client.post("/api/auth/login", json={
    "email": "mixedcaselogin@EXAMPLE.com",
    "password": TEST_PASSWORD,
})
check("Mixed-case login returns 200", r.status_code == 200)
check("Mixed-case login returns normalized email",
      r.json().get("email") == MIXED_CASE_EMAIL.lower())

# Whitespace around the email should also be tolerated
r = client.post("/api/auth/login", json={
    "email": f"  {TEST_EMAIL.upper()}  ",
    "password": TEST_PASSWORD,
})
check("Login tolerates surrounding whitespace and uppercase", r.status_code == 200)

print("\n--- E: password stored only as Argon2id hash ---")
db = SessionLocal()
stored = db.query(User).filter(User.email == TEST_EMAIL).first()
check("User exists in database", stored is not None)
if stored:
    check("Stored hash is not the plaintext password",
          stored.password_hash != TEST_PASSWORD)
    check("Stored hash uses Argon2 prefix",
          stored.password_hash.startswith("$argon2"))
    check("Correct password verifies against stored hash",
          verify_password(TEST_PASSWORD, stored.password_hash))
    check("Incorrect password fails against stored hash",
          not verify_password(WRONG_PASSWORD, stored.password_hash))
db.close()

print("\n--- F: login input validation ---")
r = client.post("/api/auth/login", json={"email": "not-an-email", "password": "x"})
check("Invalid email format returns 422", r.status_code == 422)

r = client.post("/api/auth/login", json={"email": TEST_EMAIL})
check("Missing password returns 422", r.status_code == 422)

print("\n--- Cleanup ---")
db = SessionLocal()
db.query(User).filter(User.email == TEST_EMAIL).delete()
db.query(User).filter(User.email == MIXED_CASE_EMAIL.lower()).delete()
db.commit()
remaining = db.query(User).filter(
    (User.email == TEST_EMAIL) | (User.email == MIXED_CASE_EMAIL.lower())
).count()
check("Test users removed from database", remaining == 0)
db.close()

print("")
if failures:
    print(f"{len(failures)} CHECK(S) FAILED:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("All login tests passed!")