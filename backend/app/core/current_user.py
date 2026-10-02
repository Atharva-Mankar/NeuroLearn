"""Temporary current-user resolution for Phase 4.

SECURITY LIMITATION -- READ THIS BEFORE USING THIS MODULE
=========================================================

NeuroLearn does NOT yet have backend authentication. There is no JWT, no
session cookie, and no signed token. The frontend holds a logged-in user
object in localStorage and sends its numeric ``id`` with each request.

This module validates that id against the database (the user must actually
exist), which is enough for per-user data isolation to be enforced *in the
database query* rather than in React. It is NOT enough to stop a malicious
client from forging a different, existing user id.

Once real backend authentication lands, this dependency is the single place
that changes: swap the body of :func:`get_current_user` to read a verified
token/session and load the user from it. Every router already depends on this
one function, so no router code has to change. That is the entire point of
routing identity resolution through a dependency rather than reading
``user_id`` from request bodies in each handler.
"""

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import User

# Header used as a stand-in for a future Authorization header.
CURRENT_USER_HEADER = "X-User-Id"


def get_current_user(
    x_user_id: str | None = Header(
        default=None,
        alias=CURRENT_USER_HEADER,
        description=(
            "Temporary stand-in for an authenticated identity. This is the "
            "user's database id, supplied by the frontend. It is NOT a "
            "credential: see the module docstring."
        ),
    ),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the acting user for the current request.

    Validates that the supplied id belongs to a real, existing user row and
    returns that user. Raises 400 when the header is absent or malformed and
    404 when no such user exists, so a forged id never silently creates data.

    Args:
        x_user_id: The value of the ``X-User-Id`` header, if present.
        db: Database session dependency.

    Returns:
        The authenticated ``User`` row.

    Raises:
        HTTPException: 400 if the header is missing or not an integer,
            404 if no user with that id exists.
    """
    if x_user_id is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Missing identity header. Backend authentication is not "
                "implemented yet; the frontend must send X-User-Id."
            ),
        )

    try:
        user_id = int(x_user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=400, detail="X-User-Id must be an integer user id."
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Unknown user.")

    return user


__all__ = ["CURRENT_USER_HEADER", "get_current_user"]