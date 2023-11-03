from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.dependent import DependentModel
from models.models import Dependent, Staff
from config.db import get_db

router = APIRouter()


@router.get("/dependents/{number}", response_model=DependentModel)
def get_dependent(number: int, db: Session = Depends(get_db)):
    dependent = db.query(Dependent).filter(Dependent.number == number).first()
    if not dependent:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Dependent not found")
    return dependent


@router.post("/dependents", response_model=DependentModel, status_code=status.HTTP_201_CREATED)
def create_dependent(dependent: DependentModel, db: Session = Depends(get_db)):
    db_dependent = Dependent(**dependent.dict())
    db.add(db_dependent)
    db.commit()
    db.refresh(db_dependent)
    return db_dependent


@router.put("/dependents/{number}", response_model=DependentModel)
def update_dependent(number: int, dependent: DependentModel, db: Session = Depends(get_db)):
    db_dependent = db.query(Dependent).filter(Dependent.number == number).first()
    if not db_dependent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dependent not found")

    for field, value in dependent.dict(exclude_unset=True).items():
        setattr(db_dependent, field, value)

    db.commit()
    db.refresh(db_dependent)
    return db_dependent


@router.delete("/dependents/{number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dependent(number: int, db: Session = Depends(get_db)):
    db_dependent = db.query(Dependent).filter(Dependent.number == number).first()
    if not db_dependent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dependent not found")

    db.delete(db_dependent)
    db.commit()
    return None

@router.get("/dependents")
def get_all_dependent_with_staff(db: Session = Depends(get_db)):
    dependents = db.query(Dependent).all()
    if not dependents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No dependents found")

    result = []
    for dependent in dependents:
        staff = db.query(Staff).filter(Staff.staffid == dependent.staffid).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

        dependent.staff_name = staff.name
        result.append(dependent)

    return result