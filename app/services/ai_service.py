import requests
import os
from dotenv import load_dotenv

load_dotenv()
TYPHOON_API = os.getenv("TYPHOON_API")


class LLM:
    @staticmethod
    def call_llm():
        return TYPHOON_API
