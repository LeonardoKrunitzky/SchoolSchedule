from pydantic import BaseModel

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