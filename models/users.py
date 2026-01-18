import re
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character."
    )
    nickname: str = Field(
        min_length=1,
        max_length=10,
        description="Nickname must be between 1 and 10 characters and contain only English, Korean, and numbers."
    )
    profileImageUrl: Optional[str] = None

    @validator('nickname')
    def nickname_constraints(cls, v):
        if not re.match(r'^[a-zA-Z0-9가-힣]*$', v):
            raise ValueError('Nickname can only contain English, Korean, and numbers.')
        return v

    @validator('password')
    def password_complexity(cls, v):
        if ' ' in v:
            raise ValueError('Password cannot contain spaces.')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number.')
        if not re.search(r'[\W_]', v):
            raise ValueError('Password must contain at least one special character.')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    nickname: str
    profileImageUrl: Optional[str] = None
    createdAt: datetime

class User(BaseModel):
    id: int
    email: str
    hashed_password: str
    nickname: str
    profileImageUrl: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)