from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional



class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    others = "others"


class BloodGroupEnum(str, Enum):
    a_positive = "a+"
    a_negative = "a-"
    b_positive = "b+"
    b_negative = "b-"
    ab_positive = "ab+"
    ab_negative = "ab-"
    o_positive = "o+"
    o_negative = "o-"


class StaffStatusEnum(str, Enum):
    active = "active"
    study_leave = "study_leave"
    resignation = "resignation"
    suspended = "suspended"
    deceased = "deceased"
    retired = "retired"
    maternity_paternity_leave = "maternity_paternity_leave"
    medical_leave = "medical_leave"
    on_leave = "on_leave"
    probationary = "probationary"


class StaffType(str, Enum):
    academic = "academic"
    non_academic = "non_academic"

class StaffGridBasicModel(BaseModel):
    staffid: str
    name : str
    email : str
    phonenumber: str
    staffstatus: StaffStatusEnum


class StaffBasicModel(BaseModel):
    name: str
    gender: str
    email: str
    phonenumber: str
    staffstatus: StaffStatusEnum
    qualification: str
    directory: str


class StaffModel(BaseModel):
    staffid: str
    cid: str
    name: str
    gender: GenderEnum
    nationality: str
    phonenumber: str
    email: str
    bloodgroup: BloodGroupEnum
    dateofbirth: date
    permanentaddress: int
    temporaryaddress: int
    salary: float
    joiningdate: date
    staffstatus: StaffStatusEnum
    positionlevel: int
    positiontitle: str
    stafftype: StaffType
    directoryid: int

    class Config:
        orm_mode = True