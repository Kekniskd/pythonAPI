from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext


pwd_contect = CryptContext(schemes=["bcrypt"], deprecated="auto")
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


@app.get("/")
def root():
    return {"message": "Hello world"}


# Get all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


# Get post by ID
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return post


# Delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    postQuery.update(updatedPost.dict(), synchronize_session=False)
    db.commit()
    return postQuery.first()


# Create user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashedPass = pwd_contect.hash(user.password)
    user.password = hashedPass
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser