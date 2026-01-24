from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from models.base import Base



class UserMerchantPreference(Base):
    __tablename__ = "user_merchant_preferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    merchant_id: Mapped[int] = mapped_column(ForeignKey("merchants.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    confidence: Mapped[float] = mapped_column(Numeric(3, 2))

    user: Mapped["User"] = relationship(back_populates="merchant_preferences")
    merchant: Mapped["Merchant"] = relationship(back_populates="user_preferences")
    category: Mapped["Category"] = relationship(back_populates="merchant_preferences")