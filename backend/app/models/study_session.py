"""Study session database model.

Defines the SQLAlchemy ``StudySession`` table. Each session belongs to a user
and tracks study subject, topic, duration, and timing information.
"""

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.models.user import User


class StudySession(Base):
    """A study session record belonging to a user.

    Attributes:
        id: Unique, auto-incrementing primary key.
        user_id: Foreign key referencing the user who owns this session.
        user: Relationship to the User model.
        subject: Subject of the study session (e.g., "Mathematics").
        topic: Specific topic being studied (e.g., "Linear algebra").
        duration_minutes: Planned duration in minutes. This is what the user
            asked for when starting, NOT a measurement of how long they actually
            studied. The real figure is ``elapsed_seconds``.
        elapsed_seconds: Actual seconds between ``started_at`` and ``ended_at``,
            filled in when the session is completed. Null while active.
        status: Current status ("active", "completed", "paused", etc.).
        started_at: Timestamp when the session began.
        ended_at: Timestamp when the session ended (nullable for active sessions).
        created_at: Timestamp set automatically when the record is created.
    """

    __tablename__ = "study_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped[User] = relationship("User", lazy="joined")

    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    topic: Mapped[str] = mapped_column(String(200), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    elapsed_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    started_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<StudySession id={self.id} user_id={self.user_id} subject={self.subject!r}>"