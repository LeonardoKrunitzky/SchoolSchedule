from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    role: str
    registration: str
    name: str
    period: int
    workload: int
    status: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    registration: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    period: Optional[str] = None
    workload: Optional[int] = None
    status: Optional[str] = None