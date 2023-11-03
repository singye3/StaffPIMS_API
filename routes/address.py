from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from models.models import Address
from config.db import SessionLocal
from schemas.address import AddressCreateSchema, AddressSchema

router = APIRouter()


@router.post('/addresses', response_model=AddressSchema)
def create_address(address_data: AddressCreateSchema):
    try:
        address = Address(**address_data.dict())
        db = SessionLocal()
        db.add(address)
        db.commit()
        db.refresh(address)
        return address
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get('/addresses', response_model=List[AddressSchema])
def get_all_addresses():
    try:
        db = SessionLocal()
        addresses = db.query(Address).all()
        return addresses
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get('/addresses/{address_id}', response_model=AddressSchema)
def get_address(address_id: int):
    try:
        db = SessionLocal()
        address = db.query(Address).get(address_id)

        if address:
            return address
        else:
            raise HTTPException(status_code=404, detail='Address not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.put('/addresses/{address_id}', response_model=AddressSchema)
def update_address(address_id: int, address_data: AddressCreateSchema):
    try:
        db = SessionLocal()
        address = db.query(Address).get(address_id)

        if address:
            for field, value in address_data.dict().items():
                setattr(address, field, value)

            db.commit()
            db.refresh(address)
            return address
        else:
            raise HTTPException(status_code=404, detail='Address not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.delete('/addresses/{address_id}', response_model=dict)
def delete_address(address_id: int):
    try:
        db = SessionLocal()
        address = db.query(Address).get(address_id)

        if address:
            db.delete(address)
            db.commit()
            return {'message': 'Address deleted'}
        else:
            raise HTTPException(status_code=404, detail='Address not found')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()