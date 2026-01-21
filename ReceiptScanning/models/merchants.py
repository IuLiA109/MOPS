from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from models.base import Base
from models.transactions import Transaction
from models.user_merchant_preferences import UserMerchantPreference


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(primary_key=True)
    normalized_name: Mapped[str] = mapped_column(String(255), unique=True)
    display_name: Mapped[str] = mapped_column(String(255))
    default_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    default_category: Mapped["Category"] = relationship(back_populates="merchants")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="merchant")
    user_preferences: Mapped[List["UserMerchantPreference"]] = relationship(back_populates="merchant")