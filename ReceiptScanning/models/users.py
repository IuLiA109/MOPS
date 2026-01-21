from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship

from models.accounts import Account
from models.base import Base
import re

from models.categories import Category
from models.email_reports import EmailReport
from models.import_jobs import ImportJob
from models.password_reset_tokens import PasswordResetToken
from models.transactions import Transaction
from models.user_merchant_preferences import UserMerchantPreference
from models.user_settings import UserSetting

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
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
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
        default=datetime.now(),
        nullable=False,
        index=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )

    settings: Mapped["UserSetting"] = relationship(back_populates="user", uselist=False)
    password_reset_tokens: Mapped[List["PasswordResetToken"]] = relationship(back_populates="user")
    accounts: Mapped[List["Account"]] = relationship(back_populates="user")
    import_jobs: Mapped[List["ImportJob"]] = relationship(back_populates="user")
    categories: Mapped[List["Category"]] = relationship(back_populates="user")
    email_reports: Mapped[List["EmailReport"]] = relationship(back_populates="user")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")
    merchant_preferences: Mapped[List["UserMerchantPreference"]] = relationship(back_populates="user")
