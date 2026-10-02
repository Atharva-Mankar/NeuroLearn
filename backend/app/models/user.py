"""User database model.

Defines the SQLAlchemy ``User`` table. This is the persistence layer only:
the model describes how user records are stored. Authentication (signup,
login, password hashing, tokens) is implemented in later phases.
"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class User(Base):
    """A NeuroLearn user account.

    Attributes:
        id: Unique, auto-incrementing primary key.
        name: Display name. Required.
        email: Login identifier. Required and unique.
        password_hash: Hashed password. Required.
            Only the hash is ever stored; plaintext passwords are never
            persisted. Hashing itself is implemented in a later phase.
        created_at: Timestamp set automatically when the record is created.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
