from pydantic import BaseModel
from typing import Optional

# ข้อมูลพื้นฐานสำหรับ Account
class AccountBase(BaseModel):
    account_name: str
    balance: float = 0.0

# สำหรับรับข้อมูลตอนสร้างบัญชีใหม่
class AccountCreate(AccountBase):
    user_id: int

# สำหรับส่งข้อมูลกลับไปยัง Frontend
class AccountResponse(AccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
