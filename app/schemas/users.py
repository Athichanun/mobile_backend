from pydantic import BaseModel
from typing import Optional
# สำหรับรับข้อมูลตอนสมัคร
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    image: str

# สำหรับรับข้อมูลตอนล็อกอิน
class UserLogin(BaseModel):
    username: str
    password: str

# สำหรับส่งข้อมูลกลับ (ไม่ส่งรหัสผ่านออกไป)
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    image: Optional[str] = None
    hashed_password: Optional[str] = None