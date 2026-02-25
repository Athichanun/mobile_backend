from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserResponse
from app.services.users_service import UserService
from app.dependency.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.register_user(
        db,
        username=user.username,
        password=user.password,
        email=user.email,
        phone=user.phone,
        image=user.image
    )

@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(user_id)

@router.delete("/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return UserService.delete_user_by_id(user_id)