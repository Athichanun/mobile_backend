from sqlalchemy import text
from app.dependency.database import engine
from app.repository.accounts_repository import AccountRepository


class TransactionRepository:
    @staticmethod
    def create_transaction(
        account_id: int,
        name: str,
        transaction_type: str,
        amount: float,
        price: float,
        date: str,
    ):
        with engine.begin() as conn:
            query = text(
                "INSERT INTO transactions (account_id, name, transaction_type, amount, price, date) VALUES (:account_id, :name, :transaction_type, :amount, :price, :date) RETURNING id, name, transaction_type, amount, price, date"
            )
            result = conn.execute(
                query,
                {
                    "account_id": account_id,
                    "name": name,
                    "transaction_type": transaction_type,
                    "amount": amount,
                    "price": price,
                    "date": date,
                },
            )
            row = result.fetchone()
            if row is None:
                return None

            # Update account balance
            total_price = float(amount) * float(price)
            balance_change = (
                total_price if transaction_type == "income" else -total_price
            )
            AccountRepository.update_account_balance(account_id, balance_change)

            return dict(row._mapping)

    @staticmethod
    def execute_read_query(sql_query: str):
        # Basic safety check to ensure it's a SELECT query
        if not sql_query.strip().upper().startswith("SELECT"):
            return {"error": "Only SELECT queries are allowed for AI-generated SQL"}

        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            return [dict(row._mapping) for row in result.fetchall()]
