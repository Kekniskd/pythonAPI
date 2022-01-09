from fastapi import FastAPI
from app.database import engine
from . import models
from .routers import post, user, auth
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_password: str = 'localhost'
    database_username: str = 'postgres'
    secret_key: str = "afda3545321543"

settings = Settings()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello world"}