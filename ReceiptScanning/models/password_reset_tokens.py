from datetime import datetime, timedelta

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from models.base import Base
from models.users import User
import re

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'
    id: Mapped[int] = mapped_column(primary_key=True,nullable=False,autoincrement=True)
    user_id: Mapped["User"] = mapped_column(ForeignKey('users.id'),nullable=False)
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False,default=datetime.now())
    expires_at: Mapped[datetime] = mapped_column(nullable=False,default=datetime.now() + timedelta(hours=1))
    used_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="password_reset_tokens")