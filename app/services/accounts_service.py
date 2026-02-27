from app.repository.accounts_repository import AccountRepository

class AccountService:

    @staticmethod
    def get_user_accounts(user_id: int):
        return AccountRepository.get_accounts_by_user_id(user_id)

    @staticmethod
    def create_account(user_id: int, account_name: str, balance: float = 0.0):
        return AccountRepository.create_account(user_id, account_name, balance)

    @staticmethod
    def delete_account(account_id: int, user_id: int):
        return AccountRepository.delete_account(account_id, user_id)
