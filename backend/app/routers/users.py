"""Profile API router.

Endpoints for reading and editing the signed-in user's own profile.

The user is resolved by the shared :func:`get_current_user` dependency and the
update is applied to that row only -- there is no ``user_id`` in the request
body for a caller to point at someone else's account, so cross-user writes are
not expressible.

SECURITY LIMITATION: see ``app/core/current_user.py``. The ``X-User-Id``
header is a development-only stand-in for a real credential, not an
authenticating token.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.database.connection import get_db
from app.models import User
from app.schemas.auth import ProfileResponse, UpdateProfileRequest

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    """Return the signed-in user's profile straight from the database.

    The Settings page reads this rather than trusting the localStorage copy
    kept by the frontend, so a name changed in another tab (or by an earlier
    request) is reflected immediately.
    """
    return ProfileResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        created_at=current_user.created_at.isoformat(),
    )


@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    """Update the signed-in user's display name.

    The write targets ``current_user``, which the dependency resolved from the
    request identity -- never a user id supplied in the body.
    """
    current_user.name = request.name
    db.commit()
    db.refresh(current_user)

    return ProfileResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        created_at=current_user.created_at.isoformat(),
    )


__all__ = ["router"]