from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, Field
from decimal import Decimal

class TransactionBase(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="Transaction amount")
    transaction_date: datetime
    description: Optional[str] = Field(None, max_length=255)
    merchant_name: Optional[str] = Field(None, max_length=255, description="Name of merchant/store")

class TransactionCreate(TransactionBase):
    account_id: int
    type: str = Field(..., pattern="^(expense|income|transfer)$")
    currency: str = Field(default="RON", max_length=3)
    
    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    transaction_date: Optional[datetime] = None
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None
    merchant_name: Optional[str] = Field(None, max_length=255)

class TransactionRead(BaseModel):
    id: int
    user_id: int
    account_id: int
    merchant_id: Optional[int]
    category_id: Optional[int]
    type: str
    amount: Decimal
    currency: str
    transaction_date: datetime
    description: Optional[str]
    source_type: str
    created_at: datetime
    
    merchant_name: Optional[str] = None
    category_name: Optional[str] = None
    account_name: Optional[str] = None

    class Config:
        from_attributes = True
