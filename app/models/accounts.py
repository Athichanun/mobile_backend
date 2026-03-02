from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.dependency.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    account_name = Column(String, index=True, nullable=False)
    balance = Column(Float, default=0.0)

    # Many Accounts → 1 User
    user = relationship("User", back_populates="accounts")

    # 1 Account → Many Transactions
    transactions = relationship(
        "Transaction", back_populates="account", cascade="all, delete-orphan"
    )
