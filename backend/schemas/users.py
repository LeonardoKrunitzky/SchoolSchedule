from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    role: str
    registration: str
    name: str
    period: int
    workload: int
    status: str

class UserCreate(BaseModel):
    role_id: UUID
    registration: str
    name: str
    password: str
    period: Optional[str] = None
    workload: Optional[int] = None
    status: Optional[bool] = True

class UserResponse(BaseModel):
    id: UUID
    role_id: UUID
    registration: str
    name: str
    period: Optional[str] = None
    workload: Optional[int] = None
    status: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    registration: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    period: Optional[str] = None
    workload: Optional[int] = None
    status: Optional[bool] = None