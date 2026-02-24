from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# เปลี่ยน username, password, host, db_name เป็นของคุณ
# รูปแบบ: postgresql://[user]:[password]@[host]:[port]/[db_name]
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:wave2547@127.0.0.1:5432/mobile_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Helper function สำหรับดึง Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()