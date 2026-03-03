from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from app.schemas.transaction import TransactionInput
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transaction", tags=["Transaction"])


@router.post("/chat")
def chat(payload: TransactionInput):
    return TransactionService.decision_transaction(payload.account_id, payload.prompt)


@router.post("/ocr")
async def ocr_transaction(account_id: int = Form(...), file: UploadFile = File(...)):
    return TransactionService.ocr_transaction(account_id, file)


@router.get("/account/{account_id}")
def get_transactions_by_account_id(account_id: int):
    return TransactionService.get_transactions_by_account_id(account_id)


@router.get("/user/{user_id}")
def get_all_transaction_by_user_id(user_id: int):
    return TransactionService.get_all_transaction_by_user_id(user_id)
