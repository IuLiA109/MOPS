from typing import List
from pydantic import BaseModel, Field, ConfigDict


class ProductBaseModel(BaseModel):
    name: str
    price: float = 0.0
    quantity: float = 0.0
    unit: str
    sale: float = 0.0


class ReceiptBaseModel(BaseModel):
    total: float = 0.0
    raw_text: str | None = None
    product: List[ProductBaseModel] = Field(default_factory=list)