from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern="^(expense|income)$")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, pattern="^(expense|income)$")

class CategoryRead(BaseModel):
    id: int
    user_id: Optional[int]
    name: str
    type: str
    is_system: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryWithStats(CategoryRead):
    transaction_count: int = 0
    total_amount: float = 0.0
