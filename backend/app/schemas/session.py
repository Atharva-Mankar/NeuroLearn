"""
Pydantic schemas for the session API.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class CreateSessionRequest(BaseModel):
    """Request model for creating a new study session."""
    subject: str = Field(..., description="Subject of the study session")
    topic: str = Field(..., description="Specific topic being studied")
    duration_minutes: int = Field(
        ...,
        ge=5,
        le=180,
        description="Duration in minutes (5-180)"
    )
    webcam_enabled: bool = Field(
        False,
        description="Enable webcam monitoring for fatigue estimation"
    )

    @validator('subject')
    def subject_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Subject must not be empty')
        return v.strip()

    @validator('topic')
    def topic_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Topic must not be empty')
        return v.strip()


class CreateSessionResponse(BaseModel):
    """Response model for created session."""
    id: int
    subject: str
    topic: str
    planned_duration: int  # in minutes -- what the user asked for
    actual_duration: int | None = None  # in minutes -- real elapsed time, null while active
    status: str = "active"
    start_time: str  # ISO format timestamp string
    webcam_monitoring: bool


class SessionHealthResponse(BaseModel):
    """Simple session health check response."""
    is_active: bool
    # Seconds the session has been running. For an active session this is
    # measured live from started_at; for a finished one it is the stored total.
    elapsed_seconds: int