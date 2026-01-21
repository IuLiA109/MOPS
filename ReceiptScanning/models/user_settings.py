from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from models.base import Base
import re

# from models.users import User


class UserSetting(Base):
    __tablename__ = 'user_settings'
    id: Mapped[int] = mapped_column(primary_key=True,nullable=False,autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    preferred_currency: Mapped[str] = mapped_column(nullable=False)
    weekly_report_enabled: Mapped[bool] = mapped_column(default=False,nullable=False)
    monthly_report_enabled: Mapped[bool] = mapped_column(default=False,nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(),nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.now())
    user: Mapped["User"] = relationship(back_populates="settings")