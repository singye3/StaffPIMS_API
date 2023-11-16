from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from models.models import Address, Institution, Staff, Qualification, Dependent,Directory
from config.db import SessionLocal
from schemas.staff import StaffModel,StaffGridBasicModel
from config.db import get_db

router = APIRouter()

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter()


@router.get('/staff/check/{staff_id}')
def is_staff_exists(staff_id: str, db: Session = Depends(get_db)):
    try:
        staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
        if staff:
            return True
        else:
            return False
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get('/staff/{staff_id}/basic')
def get_staff(staff_id: str, db: Session = Depends(get_db)):
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
                'positiontitle': staff.positiontitle,
                'phonenumber': staff.phonenumber,
                'staffstatus': staff.staffstatus,
                'qualification': qualification_names,
                'directory': directory.name 
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


@router.put('/staff/{staff_id}', response_model=StaffModel)
def update_staff(staff_id: str, staff_data: StaffModel, db: Session = Depends(get_db)):
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
def delete_staff(staff_id: str, db: Session = Depends(get_db)):
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
@router.get("/dependents/{staff_id}")
def get_staff_dependents(staff_id: str ,db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    dependents = db.query(Dependent).filter(Dependent.staffid == staff.staffid).all()

    return [
        {
            "name": dependent.name,
            "gender": dependent.gender,
            "bloodgroup": dependent.bloodgroup,
            "phonenumber": dependent.phonenumber,
            "type": dependent.relationtype,
        }
        for dependent in dependents
    ]




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
        return []

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

    staff = db.query(Staff).filter(Staff.staffid == staff_id).first()

    if not staff:
        return []

    institution_mapping = {institution.id: institution.name for institution in db.query(Institution).all()}

    
    trainings = staff.Training
    return [
        {
            "name": training.name,
            "institution_name": institution_mapping.get(training.institutionid),
            "startingdate": training.startingdate,
            "endingdate": training.endingdate
        }
        for training in trainings
    ]


@router.get("/staff/{staff_id}")
def get_staff_details(staff_id:str,db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    # Create a mapping of institution IDs to institution names
    institution_mapping = {institution.id: (institution.name, institution.location) for institution in db.query(Institution).all()}
    permanentaddress = db.query(Address).filter(Address.addressid == staff.permanentaddress).first()
    temporaryaddress = db.query(Address).filter(Address.addressid == staff.temporaryaddress).first()
    dependents = db.query(Dependent).filter(Dependent.staffid == staff.staffid).all()
    qualifications = db.query(Qualification).filter(Qualification.staffid == staff_id).all()
    directory = db.query(Directory).filter(staff.directoryid == Directory.directoryid).first()
    address = db.query(Address).all()

    address_data = {
        address.addressid: {
            "villagename": address.villagename,
            "gewog": address.gewog,
            "dzongkhag": address.dzongkhag
        }
    for address in address
    }

    permaddress ={
        "villagename": permanentaddress.villagename,
        "gewog" : permanentaddress.gewog,
        "dzongkhag" : permanentaddress.dzongkhag
    }
    tempaddress ={
        "villagename": temporaryaddress.villagename,
        "gewog" : temporaryaddress.gewog,
        "dzongkhag" : temporaryaddress.dzongkhag
    }

    trainings = staff.Training

    biodata = {
        "staffid": staff.staffid,
        "cid": staff.cid,
        "name": staff.name,
        "gender": staff.gender,
        "phonenumber": staff.phonenumber,
        "email": staff.email,
        "dateofbirth": staff.dateofbirth,
        "bloodgroup": staff.bloodgroup,
        "nationality": staff.nationality,
        "joiningdate": staff.joiningdate,
        "staffstatus": staff.staffstatus,
        "positionlevel": staff.positionlevel,
        "positiontitle": staff.positiontitle,
        "stafftype": staff.stafftype,
        "permanentaddress": permaddress,
        "temporaryaddress": tempaddress,
        "directory": directory.name,

    }
    dependent_data = [
        {
            "name": dependent.name,
            "cid": dependent.cid,
            "gender": dependent.gender,
            "bloodgroup": dependent.bloodgroup,
            "dateofbirth": dependent.dateofbirth,
            "phonenumber": dependent.phonenumber,
            "type": dependent.relationtype,
            "permanentaddress": address_data.get(dependent.permanentaddress),
            "temporaryaddress": address_data.get(dependent.temporaryaddress),
        }
        for dependent in dependents
    ]

    qualification_data = [
        {
            'institution_name': institution_mapping.get(qualification.institutionid)[0],
            'location': institution_mapping.get(qualification.institutionid)[1],
            'name': qualification.name,
            'graduationdate': qualification.graduationdate,
            'majorfield': qualification.majorfield,
            'gpagrade': qualification.gpagrade,
            'honorsaward': qualification.honorsaward,
        }
        for qualification in qualifications
    ]
  
    training_data = [
        {
            "name": training.name,
            'institution_name': institution_mapping.get(training.institutionid)[0],
            'location': institution_mapping.get(training.institutionid)[1],
            "startingdate": training.startingdate,
            "endingdate": training.endingdate
        }
        for training in trainings
    ]
    staff_data = {
        "biodata": biodata,
        "qualifications" : qualification_data,
        "dependents" : dependent_data,
        "trainings": training_data
    }


    return staff_data    



    

