from fastapi import FastAPI
import psycopg2
from app.database import engine
from psycopg2.extras import RealDictCursor
import time
from . import models
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='12345678',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to database")
        break
    except Exception as e:
        print(e)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello world"}