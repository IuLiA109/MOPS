from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.products import Product

class Receipt(Base):
    __tablename__ = 'receipts'

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey('transactions.id'))
    total: Mapped[float] = mapped_column(nullable=False,default=0.0)
    products: Mapped[List["Product"]] = relationship(
        back_populates='receipt',
        cascade='all, delete, delete-orphan'
    )
    transaction: Mapped["Transaction"] = relationship(back_populates="receipt")