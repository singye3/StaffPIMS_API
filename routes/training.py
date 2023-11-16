from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from models.models import Training
from config.db import SessionLocal
from schemas.training import TrainingModel,CreateTrainingModel
from config.db import get_db

router = APIRouter()

@router.post('/trainings', response_model=TrainingModel)
def create_training(training_data: CreateTrainingModel, db: Session = Depends(get_db)):
    try:
        training = Training(**training_data.dict())
        db.add(training)
        db.commit()
        db.refresh(training)
        return training
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define the route to get all trainings
@router.get('/trainings')
def get_all_trainings(db: Session = Depends(get_db)):
    trainings = db.query(Training).all()

    if not trainings:
        return []

    training_details = []
    for training in trainings:
        training_details.append({
            'trainingid': training.trainingid,
            'name': training.name,
            'institution_name': training.Institution.name, # Access the name attribute of the associated Institution object
            'startingdate': training.startingdate,
            'endingdate': training.endingdate,
        })

    return training_details

@router.get('/trainings/{training_id}', response_model=TrainingModel)
def get_training(training_id: int, db: Session = Depends(get_db)):
    try:
        training = db.query(Training).filter(Training.trainingid == training_id).first()

        if training:
            return training
        else:
            raise HTTPException(status_code=404, detail='Training not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/trainings/name/{name}')
def get_training_by_name(name: str, db: Session = Depends(get_db)):
    try:
        training = db.query(Training).filter(Training.name == name).all()

        if training:
            return training
        else:
            return []
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/trainings/{training_id}', response_model=TrainingModel)
def update_training(training_id: int, training_data: CreateTrainingModel, db: Session = Depends(get_db)):
    try:
        training = db.query(Training).filter(Training.trainingid == training_id).first()

        if training:
            for field, value in training_data.dict().items():
                setattr(training, field, value)

            db.commit()
            db.refresh(training)
            return training
        else:
            raise HTTPException(status_code=404, detail='Training not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/trainings/{training_id}', response_model=dict)
def delete_training(training_id: int, db: Session = Depends(get_db)):
    try:
        training = db.query(Training).filter(Training.trainingid == training_id).first()

        if training:
            db.delete(training)
            db.commit()
            return {'message': 'Training deleted'}
        else:
            raise HTTPException(status_code=404, detail='Training not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))