from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from config.db import SessionLocal
from config.db import get_db
from models.models import User
from schemas.user import UpdateCredential, UserBase

router = APIRouter()

@router.post("/users/", response_model=UserBase)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(**user.dict())  # Use the User model from models.models
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get a specific user by username
@router.get("/users/{username}")
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()  # Use the User model from models.models
    if db_user is None:
        return {}
    return db_user

# Update a specific user by username
@router.put("/users/{username}", response_model=UserBase)
def update_user_credential(username: str, user: UpdateCredential, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()  # Use the User model from models.models
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a specific user by username
@router.delete("/users/{username}", response_model=UserBase)
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()  # Use the User model from models.models
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user
