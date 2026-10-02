"""Authentication API router.

Handles user signup and authentication endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
)
from app.database.connection import SessionLocal, get_db
from app.models import User
from pwdlib import PasswordHash

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Initialize the password hasher with Argon2id
pwd_hasher = PasswordHash.recommended()

# A precomputed hash of an unguessable value. Verifying against this when the
# supplied email is unknown keeps the response time of "unknown email" and
# "wrong password" indistinguishable, so login cannot be used to enumerate
# which addresses have accounts.
_DUMMY_HASH = pwd_hasher.hash("neurolearn-timing-equalizer-not-a-real-credential")


def hash_password(password: str) -> str:
    """
    Securely hash a password using Argon2 via pwdlib.

    Args:
        password: Plain text password

    Returns:
        String containing the Argon2 hash (includes algorithm, parameters, salt, and hash)
    """
    return pwd_hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a stored Argon2 hash.

    Args:
        password: Plain text password to verify
        hashed: Stored hash from pwdlib (includes algorithm, parameters, salt, and hash)

    Returns:
        True if password matches, False otherwise
    """
    return pwd_hasher.verify(hashed, password)


@router.post("/signup", response_model=SignupResponse)
def signup_endpoint(
    request: SignupRequest,
    db: SessionLocal = Depends(get_db)
):
    """
    Create a new user account.

    Args:
        request: User signup data with name, email, and password
        db: Database session dependency

    Returns:
        SignupResponse: Success message and user info (without password)

    Raises:
        HTTPException: 400 for validation errors, 409 for duplicate emails
    """
    # Normalize email
    email = request.email.lower().strip()
    name = request.name.strip()
    password = request.password.strip()

    # Check for empty values
    if not name:
        raise HTTPException(status_code=400, detail="Name must not be empty")

    # Check for duplicate email
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    # Hash password securely
    try:
        password_hash = hash_password(password)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Password hashing failed")

    # Create new user
    new_user = User(
        name=name,
        email=email,
        password_hash=password_hash,
    )

    # Add and commit to database
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")

    # Return success response (without password or password_hash)
    return SignupResponse(
        message="Account created successfully",
        user={
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    )


@router.post("/login", response_model=LoginResponse)
def login_endpoint(
    request: LoginRequest,
    db: SessionLocal = Depends(get_db)
):
    """
    Authenticate a user against the stored Argon2 password hash.

    Deliberately returns the same 401 for an unknown email and for a wrong
    password, so the endpoint cannot be used to discover which addresses have
    accounts.

    Args:
        request: Login credentials (email and password)
        db: Database session dependency

    Returns:
        LoginResponse: Safe user information only (never password/password_hash)

    Raises:
        HTTPException: 401 for invalid credentials
    """
    # Normalize email exactly as signup does
    email = request.email.lower().strip()
    password = request.password

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        # Burn an equivalent amount of CPU hashing so timing does not leak
        # whether this address exists.
        verify_password(password, _DUMMY_HASH)
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Verify the submitted password against the stored hash. The plain text
    # password is only ever passed to Argon2, never compared to a stored value.
    try:
        is_valid = verify_password(password, user.password_hash)
    except Exception:
        raise HTTPException(status_code=500, detail="Password verification failed")

    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Return safe user information only
    return LoginResponse(
        id=user.id,
        name=user.name,
        email=user.email,
    )


@router.get("/health")
def auth_health():
    """Health check for auth routes."""
    return {"status": "ok"}


__all__ = ["router"]