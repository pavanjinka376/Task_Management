from pydantic import BaseModel, EmailStr
from typing import Optional

# ---------- USER SCHEMAS ----------

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role_id: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[str] = None


class UserOut(BaseModel):
    id: str
    email: EmailStr
    role_id: str

    class Config:
        from_attributes = True


# ---------- TASK SCHEMAS ----------

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class TaskOut(TaskCreate):
    id: str
    owner_id: str

    class Config:
        from_attributes = True
