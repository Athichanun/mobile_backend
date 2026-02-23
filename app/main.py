from fastapi import FastAPI
from app.auth import router as auth_router
from app.auth import get_current_user
from app.register import router as regis_router
from fastapi import Depends
from app.database import engine
from app import models
import logging
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router)
app.include_router(regis_router)
@app.get("/")


def home():
    return {"message": "Main API is working"}

@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, this is your private data!"}
