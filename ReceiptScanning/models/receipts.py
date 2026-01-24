from decimal import Decimal
from typing import List, Optional, Text

from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.products import Product


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    total_tax: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    raw_text: Mapped[Optional[str]] = mapped_column(String(15000))

    transaction: Mapped["Transaction"] = relationship(back_populates="receipt")
    products: Mapped[List["Product"]] = relationship(
        back_populates="receipt", cascade="all, delete-orphan"
    )