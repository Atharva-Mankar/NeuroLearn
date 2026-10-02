"""Authentication API router.

Handles user signup and authentication endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import SignupRequest, SignupResponse
from app.database.connection import SessionLocal, get_db
from app.models import User
import hashlib
import secrets
import binascii
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])


def hash_password(password: str) -> str:
    """
    Securely hash a password using PBKDF2-HMAC-SHA256.

    Args:
        password: Plain text password

    Returns:
        Hex string of hash:salt
    """
    # Generate a random salt
    salt = secrets.token_bytes(32)

    # Hash the password with the salt
    # Using 100,000 iterations for security
    pwdhash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )

    # Return hash and salt as hex strings
    return f"{pwdhash.hex()}:{salt.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a stored hash.

    Args:
        password: Plain text password to verify
        hashed: Stored hash in format hash:salt

    Returns:
        True if password matches, False otherwise
    """
    try:
        hash_hex, salt_hex = hashed.split(':')
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        # Compute hash of provided password
        pwdhash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        # Compare hashes
        return secrets.compare_digest(pwdhash, expected_hash)
    except Exception:
        return False


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

@router.get("/health")
def auth_health():
    """Health check for auth routes."""
    return {"status": "ok"}

__all__ = ["router"]