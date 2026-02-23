from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from app import models, schemas
# 1. การตั้งค่าพื้นฐาน (ในสเกลใหญ่ควรอยู่ใน .env)
SECRET_KEY = "super-secret-key-for-mobile-app"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ใช้สำหรับ Hash รหัสผ่าน
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# บอก FastAPI ว่าจะไปหา Token ได้จาก URL ไหน
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Helper Functions ---

def create_access_token(data: dict):
    """ฟังก์ชันสำหรับสร้าง JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """ฟังก์ชันตรวจสอบว่า Token ที่ส่งมาถูกต้องหรือไม่"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username # ส่งชื่อ User กลับไป
    except JWTError:
        raise credentials_exception

# --- API Routes ---

@router.post("/login")
async def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # ดึง User จาก Database จริงๆ
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    
    # เช็คว่ามี User ไหม และรหัสผ่านที่ Hash ไว้ตรงกันไหม
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    
    # สร้าง Token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}