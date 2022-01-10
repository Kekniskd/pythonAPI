from fastapi import status, HTTPException, Depends, APIRouter, status
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# Create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    present_user = db.query(models.User).filter(models.User.email == user.email).first()
    if present_user:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"{user.email} already exists!!")
    else:
        hashedPass = utils.hash(user.password)
        user.password = hashedPass
        newUser = models.User(**user.dict())
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser


# Get user by ID
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    return user