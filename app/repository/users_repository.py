from sqlalchemy import text
from app.dependency.database import engine

class UserRepository:

    @staticmethod
    def get_by_username(username: str):
        with engine.connect() as conn:
            query = text("SELECT id, username, hashed_password FROM users WHERE username = :username")
            result = conn.execute(query, {"username": username}).fetchone()
            if result:
                return dict(result._mapping)
            return None

    @staticmethod
    def get_by_id(user_id: int):
        with engine.connect() as conn:
            query = text("SELECT id, username, hashed_password FROM users WHERE id = :id")
            result = conn.execute(query, {"id": user_id}).fetchone()
            if result:
                return dict(result)
            return None

    @staticmethod
    def update_user(user_id: int, username: str, email: str, phone: str, image: str, hashed_password: str):
        with engine.begin() as conn:
            query = text(
                "UPDATE users SET username = :username, email = :email, phone = :phone, image = :image, hashed_password = :hashed_password WHERE id = :id RETURNING id, username"
            )
            result = conn.execute(query, {"username": username, "email": email, "phone": phone, "image": image, "hashed_password": hashed_password, "id": user_id})
            return dict(result.fetchone())

    @staticmethod
    def delete_user(user_id: int):
        with engine.begin() as conn:
            query = text("DELETE FROM users WHERE id = :id")
            conn.execute(query, {"id": user_id})
            return True

    @staticmethod
    def create_user(username: str, email: str, phone: str, image: str, hashed_password: str):
        with engine.begin() as conn: 
            query = text(
                "INSERT INTO users (username, email, phone, image, hashed_password) VALUES (:username, :email, :phone, :image, :hashed_password) RETURNING id, username"
            )
            result = conn.execute(query, {"username": username, "email": email, "phone": phone, "image": image, "hashed_password": hashed_password})
            row = result.fetchone()
            if row is None:
                return None
            return dict(row._mapping)