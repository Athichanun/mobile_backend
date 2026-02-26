from app.services.ai_service import LLM
from fastapi import APIRouter, Depends, status


router = APIRouter(prefix="/transaction", tags=["Transaction"])


@router.get("/test")
def call_llm():
    return LLM.call_llm()
