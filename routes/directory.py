from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from config.db import get_db
from schemas.directory import DirectoryModel
from models.models import Directory, Staff

router = APIRouter()


@router.get("/directories", response_model=List[DirectoryModel])
def get_all_directories(db: Session = Depends(get_db)):
    directories = db.query(Directory).all()
    return directories


@router.get("/directories/{directory_id}", response_model=DirectoryModel)
def get_directory_by_id(directory_id: int, db: Session = Depends(get_db)):
    directory = db.query(Directory).get(directory_id)
    return directory

@router.get("/directories/name/{name}")
def get_directory_id(name: str, db: Session = Depends(get_db)):
    directory = db.query(Directory).filter(Directory.name == name).first()
    if directory:
        return directory.directoryid
    else:
        return {"error": "Directory not found"}


@router.post("/directories", response_model=DirectoryModel)
def create_directory(directory: DirectoryModel, db: Session = Depends(get_db)):
    new_directory = Directory(name=directory.name, hod=directory.hod)
    db.add(new_directory)
    db.commit()
    db.refresh(new_directory)
    return new_directory


@router.put("/directories/{directory_id}", response_model=DirectoryModel)
def update_directory(directory_id: int, directory: DirectoryModel, db: Session = Depends(get_db)):
    existing_directory = db.query(Directory).get(directory_id)
    existing_directory.name = directory.name
    existing_directory.hod = directory.hod
    db.commit()
    db.refresh(existing_directory)
    return existing_directory


@router.delete("/directories/{directory_id}")
def delete_directory(directory_id: int, db: Session = Depends(get_db)):
    directory = db.query(Directory).get(directory_id)
    db.delete(directory)
    db.commit()
    return {"message": "Directory deleted successfully"}


@router.get("/directories/{name}/staff")
def get_staff_members(directory_name: str, db: Session = Depends(get_db)):
    directory = db.query(Directory).filter(Directory.name == directory_name.upper()).first()
    if directory:
        staff_members = db.query(Staff).filter(Staff.directoryid == directory.directoryid).all()
        staff_names = [staff.name for staff in staff_members]
        return {"directory_name": directory_name, "staff_members": staff_names}
    else:
        return {"directory_name": directory_name, "message": "Directory not found"}

