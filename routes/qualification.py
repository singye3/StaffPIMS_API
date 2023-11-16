from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from models.models import Qualification
from schemas.qualification import QualificationModel
from config.db import get_db
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.get("/qualifications", response_model=List[QualificationModel])
def get_all_qualifications(db: Session = Depends(get_db)):
    try:
        qualifications = db.query(Qualification).all()
        return qualifications
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/qualifications/{qualification_id}", response_model=QualificationModel)
def get_qualification_by_id(qualification_id: int, db: Session = Depends(get_db)):
    try:
        qualification = db.query(Qualification).filter(Qualification.id == qualification_id).first()
        if qualification:
            return qualification
        else:
            raise HTTPException(status_code=404, detail="Qualification not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/qualifications", response_model=QualificationModel)
def create_qualification(qualification: QualificationModel, db: Session = Depends(get_db)):
    try:
        new_qualification = Qualification(**qualification.dict())
        db.add(new_qualification)
        db.commit()
        db.refresh(new_qualification)
        return new_qualification
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/qualifications/{qualification_id}", response_model=QualificationModel)
def update_qualification(qualification_id: int, qualification: QualificationModel, db: Session = Depends(get_db)):
    try:
        existing_qualification = db.query(Qualification).filter(Qualification.id == qualification_id).first()
        if existing_qualification:
            for key, value in qualification.dict().items():
                setattr(existing_qualification, key, value)
            db.commit()
            db.refresh(existing_qualification)
            return existing_qualification
        else:
            raise HTTPException(status_code=404, detail="Qualification not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/qualifications/{qualification_id}")
def delete_qualification(qualification_id: int, db: Session = Depends(get_db)):
    try:
        qualification = db.query(Qualification).filter(Qualification.id == qualification_id).first()
        if qualification:
            db.delete(qualification)
            db.commit()
            return {"message": "Qualification deleted"}
        else:
            raise HTTPException(status_code=404, detail="Qualification not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))