from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth, database
from app.database import get_db
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. ตรวจสอบว่ามี Username นี้หรือยัง
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username นี้ถูกใช้งานไปแล้ว"
        )
    
    # 2. เข้ารหัสผ่านก่อนบันทึก
    hashed_password = auth.pwd_context.hash(user.password)
    
    # 3. สร้างก้อนข้อมูลใหม่
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    
    # 4. บันทึกลง Database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user