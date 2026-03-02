from pydantic import BaseModel


class TransactionBase(BaseModel):
    account_id: int
    name: str
    transaction_type: str
    amount: float
    price: float
    date: str


class TransactionInput(BaseModel):
    account_id: int
    prompt: str
