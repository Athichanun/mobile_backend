from sqlalchemy import Column, Integer, String, Text
from app.dependency.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    image = Column(Text)  # <-- เปลี่ยนจาก String เป็น Text
    hashed_password = Column(String)