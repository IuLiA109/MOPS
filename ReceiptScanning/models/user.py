from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, validates,mapped_column
from models.base import Base
import re

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{4,}$")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(31),
        unique=True,
        nullable=False
    )

    @validates("username")
    def validate_username(self, key, value: str) -> str:
        if not USERNAME_RE.fullmatch(value or ""):
            raise ValueError("Invalid username (min 4 chars, letters/numbers/_)")
        return value

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )
