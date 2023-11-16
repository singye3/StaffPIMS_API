from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from models.models import StaffTraining
from config.db import SessionLocal, get_db
from schemas.staff_training import StaffTrainingCreate, StaffTrainingUpdate

router = APIRouter()


@router.post("/stafftraining", status_code=201)
def create_staff_training(staff_training: StaffTrainingCreate, db: Session = Depends(get_db)):
    try:
        new_staff_training = StaffTraining(staffid=staff_training.staffid, trainingid=staff_training.trainingid)
        db.add(new_staff_training)
        db.commit()
        db.refresh(new_staff_training)
        return new_staff_training
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/stafftraining/{staffid}/{trainingid}")
def get_staff_training(staffid: str, trainingid: int, db: Session = Depends(get_db)):
    try:
        staff_training = db.query(StaffTraining).filter_by(staffid=staffid, trainingid=trainingid).first()
        if not staff_training:
            return {}
        return staff_training
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.put("/stafftraining/{staffid}/{trainingid}")
def update_staff_training(staffid: str, trainingid: int, staff_training_update: StaffTrainingUpdate, db: Session = Depends(get_db)):
    try:
        staff_training = db.query(StaffTraining).filter_by(staffid=staffid, trainingid=trainingid).first()
        if not staff_training:
            return {}
        staff_training.trainingid = staff_training_update.trainingid
        db.commit()
        return staff_training
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.delete("/stafftraining/{staffid}/{trainingid}", status_code=204)
def delete_staff_training(staffid: str, trainingid: int, db: Session = Depends(get_db)):
    try:
        staff_training = db.query(StaffTraining).filter_by(staffid=staffid, trainingid=trainingid).first()
        if not staff_training:
            return []
        db.delete(staff_training)
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")