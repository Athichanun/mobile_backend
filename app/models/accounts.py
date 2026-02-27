from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.dependency.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_name = Column(String, index=True)
    balance = Column(Float, default=0.0)

    # Optional: relationship back to User
    user = relationship("User", back_populates="accounts")

# Add relationship to User model as well
# Note: I will modify users.py in the next step to add back_populates
