from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, Column, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship

from models.base import Base



class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    merchant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("merchants.id"), nullable=True)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)
    source_job_id: Mapped[Optional[int]] = mapped_column(ForeignKey("import_jobs.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(20))  # expense, income, transfer
    amount: Mapped[float] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3))
    transaction_date: Mapped[datetime] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(String(255),nullable=True)
    source_type: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="transactions")
    account: Mapped["Account"] = relationship(back_populates="transactions")
    merchant: Mapped["Merchant"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")
    source_job: Mapped["ImportJob"] = relationship(back_populates="transactions")
    receipt: Mapped["Receipt"] = relationship(back_populates="transaction")