from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from app.dependency.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )

    name = Column(String, index=True)
    transaction_type = Column(String, index=True)  # income / expense
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(Date)

    # Many Transactions → 1 Account
    account = relationship("Account", back_populates="transactions")
