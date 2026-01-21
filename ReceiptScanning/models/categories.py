from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from models.base import Base
import re

from models.categorization_rules import CategorizationRule
from models.merchants import Merchant
from models.transactions import Transaction
from models.user_merchant_preferences import UserMerchantPreference



class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(20))
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="categories")


    transactions: Mapped[List["Transaction"]] = relationship(back_populates="category")
    rules: Mapped[List["CategorizationRule"]] = relationship(back_populates="category")
    merchants: Mapped[List["Merchant"]] = relationship(back_populates="default_category")
    merchant_preferences: Mapped[List["UserMerchantPreference"]] = relationship(back_populates="category")