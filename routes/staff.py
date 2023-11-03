from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from models.models import Institution, Staff, Qualification, Dependent,Directory
from config.db import SessionLocal
from schemas.staff import StaffBasicModel, StaffModel,StaffGridBasicModel
from config.db import get_db

router = APIRouter()

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter()


@router.get('/staff/{staff_id}/basic')
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).filter(Staff.staffid == staff_id).first()

        if staff:
            qualification = db.query(Qualification).filter(Qualification.staffid == staff_id).all()
            directory = db.query(Directory).filter(Directory.directoryid == staff.directoryid).first()
            qualification_names = [qual.name for qual in qualification]

            return {
                'name': staff.name,
                'gender': staff.gender,
                'email': staff.email,
                'phonenumber': staff.phonenumber,
                'staffstatus': staff.staffstatus,
                'qualification': qualification_names,
                'directory': directory.name if directory else None
            }
            
        else:
            raise HTTPException(status_code=404, detail='Staff not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/staff/{name}/basic', response_model=List[StaffGridBasicModel])
def get_staff_basic_by_name(name: str, db: Session = Depends(get_db)):
    try:
        staff = (
            db.query(Staff)
            .filter(Staff.name == name)
            .all()
        )

        if staff:
            staff_basic_list = []
            for staff_member in staff:
                staff_basic = StaffGridBasicModel(
                    staffid= staff_member.staffid,
                    name=staff_member.name,
                    email=staff_member.email,
                    phonenumber=staff_member.phonenumber,
                    staffstatus=staff_member.staffstatus,
                )
                staff_basic_list.append(staff_basic)

            return staff_basic_list
        else:
            raise HTTPException(status_code=404, detail='Staff not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get('/staff/basic', response_model=List[StaffGridBasicModel])
def get_staff_basic(db: Session = Depends(get_db)):
    try:
        staff = (
            db.query(Staff)
            .all()
        )

        if staff:
            staff_basic_list = []
            for staff_member in staff:
                
                staff_basic = StaffGridBasicModel(
                    staffid=staff_member.staffid,
                    name=staff_member.name,
                    email=staff_member.email,
                    phonenumber=staff_member.phonenumber,
                    staffstatus=staff_member.staffstatus,
                )
                staff_basic_list.append(staff_basic)

            return staff_basic_list
        else:
            raise HTTPException(status_code=404, detail='Staff not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint for creating staff 
@router.post('/staff', response_model=StaffModel)
def create_staff(staff_data: StaffModel, db: Session = Depends(get_db)):
    try:
        staff = Staff(**staff_data.dict())
        db.add(staff)
        db.commit()
        db.refresh(staff)
        return staff
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/staff')
def get_all_staff(db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).all()  # Assuming `Staff` is the SQLAlchemy model

        if not staff:
            raise HTTPException(status_code=404, detail="No staff data found")
        
        return staff
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/staff/{staff_id}', response_model=StaffModel)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).filter(Staff.staffid == staff_id).first()

        if staff:
            qualification = db.query(Qualification).filter(Qualification.staffid == staff_id)
            return staff
        else:
            raise HTTPException(status_code=404, detail='Staff not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/staff/{staff_id}', response_model=StaffModel)
def update_staff(staff_id: int, staff_data: StaffModel, db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).filter(Staff.staffid == staff_id).first()

        if staff:
            for field, value in staff_data.dict().items():
                setattr(staff, field, value)

            db.commit()
            db.refresh(staff)
            return staff
        else:
            raise HTTPException(status_code=404, detail='Staff not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/staff/{staff_id}', response_model=dict)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    try:    
        staff = db.query(Staff).filter(Staff.staffid == staff_id).first()

        if staff:
            db.delete(staff)
            db.commit()
            return {'message': 'Staff deleted'}
        else:
            raise HTTPException(status_code=404, detail='Staff not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dependents")
def get_staff_dependents(db: Session = Depends(get_db)):
    staffs = db.query(Staff).all()
    if not staffs:
        raise HTTPException(status_code=404, detail="Staff not found")

    result = []
    for staff in staffs:
        dependents = db.query(Dependent).filter(Dependent.staffid == staff.staffid).all()

        dependents_data = [
            {
                "name": dependent.name,
                "gender": dependent.gender,
                "bloodgroup": dependent.bloodgroup,
                "phonenumber": dependent.phonenumber,
                "type": dependent.relationtype,
            }
            for dependent in dependents
        ]

        staff_data = {
            "staffid": staff.staffid,
            "staff_name": staff.name,
            "dependents": dependents_data
        }

        result.append(staff_data)

    return result

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

@router.get("/qualifications")
def get_staff_qualifications(db: Session = Depends(get_db)):
    staffs = db.query(Staff).all()

    if not staffs:
        raise HTTPException(status_code=404, detail="Staff not found")

    # Create a mapping of institution IDs to institution names
    institution_mapping = {institution.id: institution.name for institution in db.query(Institution).all()}

    result = []
    for staff in staffs:
        qualifications = db.query(Qualification).filter(Qualification.staffid == staff.staffid) # Assuming you have defined a relationship between Staff and Qualification

        qualification_data = [
            {
                "name": qualification.name,
                "graduationdate": qualification.graduationdate,
                "majorfield": qualification.majorfield,
                "gpagrade": qualification.gpagrade,
                "honorsaward": qualification.honorsaward,
                "institution": institution_mapping.get(qualification.institutionid)
            }
            for qualification in qualifications
        ]

        staff_data = {
            "staffid": staff.staffid,
            "staff_name": staff.name,
            "qualifications": qualification_data
        }

        result.append(staff_data)

    return result


@router.get("/trainings")
def get_staff_trainings(db: Session = Depends(get_db)):
    staffs = db.query(Staff).all()

    if not staffs:
        raise HTTPException(status_code=404, detail="Staff not found")

    # Create a mapping of institution IDs to institution names
    institution_mapping = {institution.id: institution.name for institution in db.query(Institution).all()}

    result = []
    for staff in staffs:
        trainings = staff.Training
        training_data = [
            {
                "name": training.name,
                "institution_name": institution_mapping.get(training.institutionid),
                "instructorname": training.instructorname,
                "startingdate": training.startingdate,
                "endingdate": training.endingdate
            }
            for training in trainings
        ]

        staff_data = {
            "staffid": staff.staffid,
            "staff_name": staff.name,
            "trainings": training_data
        }

        result.append(staff_data)

    return result


# Define the route to get staff qualifications by staff_id
@router.get('/qualifications/{staff_id}')
def get_staff_qualifications(staff_id: str, db: Session = Depends(get_db)):
    qualifications = db.query(Qualification).filter(Qualification.staffid == staff_id).all()

    if not qualifications:
        return {"message": "Qualifications not found"}

    staff_qualifications = []
    for qualification in qualifications:
        staff_qualifications.append({
            'id': qualification.id,
            'institutionid': qualification.institutionid,
            'name': qualification.name,
            'graduationdate': qualification.graduationdate,
            'majorfield': qualification.majorfield,
            'gpagrade': qualification.gpagrade,
            'honorsaward': qualification.honorsaward,
            'staffid': qualification.staffid
        })

    return staff_qualifications

# Endpoint to fetch staff training details
@router.get('/staff/{staff_id}/training')
def get_staff_training(staff_id: str,db: Session = Depends(get_db)):


    try:
        staff = db.query(Staff).filter(Staff.staffid == staff_id).first()

        if staff is None:
            raise HTTPException(status_code=404, detail='Staff not found')

        training = staff.Training

        # Return the training details
        return {'staff_id': staff_id, 'training': [t.name for t in training]}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

    

