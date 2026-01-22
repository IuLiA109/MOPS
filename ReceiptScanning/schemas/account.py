from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern="^(cash|bank|card|other)$")
    currency: str = Field(default="RON", max_length=3)

class AccountCreate(AccountBase):
    is_default: bool = Field(default=False)

class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, pattern="^(cash|bank|card|other)$")
    currency: Optional[str] = Field(None, max_length=3)
    is_default: Optional[bool] = None

class AccountRead(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    currency: str
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AccountWithBalance(AccountRead):
    balance: float = 0.0
    transaction_count: int = 0
