from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    admin = 'admin'
    staff = 'staff'
    student = 'student'

class UserBase(BaseModel):
    username: str
    password: str
    role: UserRole
    
    class Config:
        orm_mode = True

class UpdateCredential(BaseModel):
    username: str
    password: str


   
