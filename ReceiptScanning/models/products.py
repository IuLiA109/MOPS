from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    price: Mapped[float] = mapped_column(nullable=False,default=0)
    quantity: Mapped[float] = mapped_column(nullable=False,default=0.0)
    unit: Mapped[str] = mapped_column(String(10),nullable=False)
    sale: Mapped[float] = mapped_column(nullable=False,default=0.0)
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))
    receipt: Mapped["Receipt"] = relationship(back_populates="products")