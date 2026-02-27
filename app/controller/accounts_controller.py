from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.accounts import AccountCreate, AccountResponse
from app.services.accounts_service import AccountService
from app.dependency.database import get_db
from app.dependency.auth import get_current_user

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/", response_model=List[AccountResponse])
def get_user_accounts(current_user: tuple = Depends(get_current_user)):
    # get_current_user returns (username, user_id)
    username, user_id = current_user
    return AccountService.get_user_accounts(user_id)

@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: AccountCreate, current_user: tuple = Depends(get_current_user)):
    # Overwrite user_id from token to ensure security
    username, user_id = current_user
    return AccountService.create_account(
        user_id=user_id,
        account_name=account.account_name,
        balance=account.balance
    )

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, current_user: tuple = Depends(get_current_user)):
    username, user_id = current_user
    success = AccountService.delete_account(account_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found or you don't have permission to delete it"
        )
    return None
