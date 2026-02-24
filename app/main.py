from fastapi import FastAPI, Depends
from app.dependency.auth import router as auth_router
from app.dependency.auth import get_current_user
from app.services.users import router as regis_router
from app.dependency.database import engine, Base
from app.models.users import User  # สำคัญ! ต้อง import เพื่อ register model

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(regis_router)

@app.get("/")
def home():
    return {"message": "Main API is working"}

@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, this is your private data!"}