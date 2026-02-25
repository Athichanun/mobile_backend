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
            query = text("SELECT id, username, email, phone, image FROM users WHERE id = :id")
            result = conn.execute(query, {"id": user_id}).fetchone()
            print("RAW RESULT:", result)
            if result:
                return dict(result._mapping)   # 👈 สำคัญมาก
            return None

    @staticmethod
    def update_user(user_id: int, **fields):
        with engine.begin() as conn:
            set_clauses = []
            values = {"id": user_id}

            for key, value in fields.items():
                if value is not None:
                    set_clauses.append(f"{key} = :{key}")
                    values[key] = value

            if not set_clauses:
                return None  # ไม่มีอะไรให้ update

            query = text(
                f"""
                UPDATE users
                SET {", ".join(set_clauses)}
                WHERE id = :id
                RETURNING id, username
                """
            )

            result = conn.execute(query, values)
            row = result.fetchone()
            return dict(row._mapping) if row else None

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