"""Database models.

Importing this package registers all SQLAlchemy models with the shared
``Base`` metadata so that ``Base.metadata.create_all()`` can create their
tables.
"""

from app.models.user import User

__all__ = ["User"]