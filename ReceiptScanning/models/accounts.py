from datetime import datetime, timedelta
from typing import List

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from models.base import Base
from models.transactions import Transaction



class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(50))
    currency: Mapped[str] = mapped_column(String(3))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="accounts")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="account")