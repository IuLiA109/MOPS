from pydantic import BaseModel, EmailStr
from typing import Optional




class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

