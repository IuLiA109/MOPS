from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from models.base import Base



class CategorizationRule(Base):
    __tablename__ = "categorization_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    priority: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    category: Mapped["Category"] = relationship(back_populates="rules")