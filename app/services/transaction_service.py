import os
from dotenv import load_dotenv
import requests

load_dotenv()
TYPHOON_API = os.getenv("TYPHOON_API")


class TransactionService:
    @staticmethod
    def decision_transaction(account_id: int, prompt: str):
        pass
