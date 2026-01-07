import re
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain at least 8 characters, one uppercase character, "
                "one lowercase character, one number, and one special character."
            )
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r".+@.+\..+"
        if not re.match(pattern, v):
            raise ValueError(
                "Email is invalid."
            )
        return v

class UserLogin(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_exclusive_auth_method(self):
        if self.email and self.username:
            raise ValueError("Provide either email or username, not both.")
        if not self.email and not self.username:
            raise ValueError("Provide either email or username.")
        return self

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r".+@.+\..+"
        if not re.match(pattern, v):
            raise ValueError(
                "Email is invalid."
            )
        return v

class UserRead(BaseModel):
    id: int
    username: str
