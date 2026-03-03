from sqlalchemy import text
from app.dependency.database import engine


class AccountRepository:
    @staticmethod
    def get_accounts_by_user_id(user_id: int):
        with engine.connect() as conn:
            query = text(
                "SELECT id, user_id, account_name, balance FROM accounts WHERE user_id = :user_id"
            )
            result = conn.execute(query, {"user_id": user_id}).fetchall()
            return [dict(row._mapping) for row in result]

    @staticmethod
    def create_account(user_id: int, account_name: str, balance: float = 0.0):
        with engine.begin() as conn:
            query = text(
                "INSERT INTO accounts (user_id, account_name, balance) VALUES (:user_id, :account_name, :balance) RETURNING id, user_id, account_name, balance"
            )
            result = conn.execute(
                query,
                {"user_id": user_id, "account_name": account_name, "balance": balance},
            )
            row = result.fetchone()
            return dict(row._mapping) if row else None

    @staticmethod
    def delete_account(account_id: int, user_id: int):
        with engine.begin() as conn:
            query = text(
                "DELETE FROM accounts WHERE id = :id AND user_id = :user_id RETURNING id"
            )
            result = conn.execute(query, {"id": account_id, "user_id": user_id})
            return result.fetchone() is not None

    @staticmethod
    def update_account_balance(account_id: int, amount_change: float):
        with engine.begin() as conn:
            query = text(
                "UPDATE accounts SET balance = balance + :amount_change WHERE id = :id"
            )
            conn.execute(query, {"amount_change": amount_change, "id": account_id})
