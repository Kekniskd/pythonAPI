from fastapi import Response, status, HTTPException, Depends, APIRouter, Depends
from starlette.status import HTTP_403_FORBIDDEN
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# Get all posts
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_post(db: Session = Depends(get_db), limit: int=10, skip: int=0, search: Optional[str]=""):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # Query (SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.user_id AS posts_user_id, count(votes.post_id) AS votesFROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id)
    return results


# Create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    newPost = models.Post(user_id=current_user.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


# Get post by ID
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return post


# Delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    postQuery.update(updatedPost.dict(), synchronize_session=False)
    db.commit()
    return postQuery.first()