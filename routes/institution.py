from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from models.models import Institution
from schemas.institution import InstitutionModel
from config.db import get_db
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.get("/institutions", response_model=List[InstitutionModel])
def get_all_institutions(db: Session = Depends(get_db)):
    try:
        institutions = db.query(Institution).all()
        return institutions
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/institutions/{institution_id}", response_model=InstitutionModel)
def get_institution_by_id(institution_id: int, db: Session = Depends(get_db)):
    try:
        institution = db.query(Institution).filter(Institution.id == institution_id).first()
        if institution:
            return institution
        else:
            raise HTTPException(status_code=404, detail="Institution not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/institutions/name/{name}")
def get_institution_by_name(name: str, db: Session = Depends(get_db)):
    try:
        institutions = db.query(Institution).filter(Institution.name == name).all()
        if institutions:
            return institutions
        else:
            raise HTTPException(status_code=404, detail="Institution not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/institutions", response_model=InstitutionModel)
def create_institution(institution: InstitutionModel, db: Session = Depends(get_db)):
    try:
        new_institution = Institution(**institution.dict())
        db.add(new_institution)
        db.commit()
        db.refresh(new_institution)
        return new_institution
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/institutions/{institution_id}", response_model=InstitutionModel)
def update_institution(institution_id: int, institution: InstitutionModel, db: Session = Depends(get_db)):
    try:
        existing_institution = db.query(Institution).filter(Institution.id == institution_id).first()
        if existing_institution:
            for key, value in institution.dict().items():
                setattr(existing_institution, key, value)
            db.commit()
            db.refresh(existing_institution)
            return existing_institution
        else:
            raise HTTPException(status_code=404, detail="Institution not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/institutions/{institution_id}")
def delete_institution(institution_id: int, db: Session = Depends(get_db)):
    try:
        institution = db.query(Institution).filter(Institution.id == institution_id).first()
        if institution:
            db.delete(institution)
            db.commit()
            return {"message": "Institution deleted"}
        else:
            raise HTTPException(status_code=404, detail="Institution not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))