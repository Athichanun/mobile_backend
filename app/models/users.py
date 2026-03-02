from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.dependency.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True)
    image = Column(Text)
    hashed_password = Column(String, nullable=False)

    # 1 User → Many Accounts
    accounts = relationship(
        "Account", back_populates="user", cascade="all, delete-orphan"
    )
