from pydantic import BaseModel

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