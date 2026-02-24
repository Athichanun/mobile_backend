from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate, UserResponse
from app.dependency.auth import pwd_context
from app.dependency.database import get_db
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. ตรวจสอบว่ามี Username นี้หรือยัง
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username นี้ถูกใช้งานไปแล้ว"
        )
    
    # 2. เข้ารหัสผ่านก่อนบันทึก
    hashed_password = pwd_context.hash(user.password)
    
    # 3. สร้างก้อนข้อมูลใหม่
    new_user = User(username=user.username, hashed_password=hashed_password)
    
    # 4. บันทึกลง Database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user