from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.users_repository import UserRepository
from app.dependency.auth import pwd_context
import logging
logger = logging.getLogger(__name__)
class UserService:

    @staticmethod
    def register_user(db: Session, username: str, password: str , email: str, phone: str, image: str):

        # เช็คว่าซ้ำไหม
        existing_user = UserRepository.get_by_username(username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username นี้ถูกใช้งานไปแล้ว"
            )

        # hash password
        hashed_password = pwd_context.hash(password)
        # save
        logger.info(email)
        logger.info(phone)
        logger.info(image)
        logger.info(username)
        logger.info(hashed_password)
        return UserRepository.create_user(
            username=username,
            email=email,               # email จริง
            phone=phone,               # phone จริง
            image=image,               # Base64 image
            hashed_password=hashed_password,  # hash password
        )
    @staticmethod
    def get_user_by_id(user_id: int):
        return UserRepository.get_by_id(user_id)