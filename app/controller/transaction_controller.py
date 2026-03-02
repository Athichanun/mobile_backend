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
