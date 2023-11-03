from pydantic import BaseModel
from datetime import date
from enum import Enum


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


class RelationTypeEnum(str, Enum):
    spouse = "spouse"
    child = "child"
    parent = "parent"
    sibling = "sibling"
    other = "other"


class DependentModel(BaseModel):
    number: int
    cid: str
    name: str
    gender: GenderEnum
    phonenumber: str
    bloodgroup: BloodGroupEnum
    dateofbirth: date
    relationtype: RelationTypeEnum
    permanentaddress: int
    temporaryaddress: int
    staffid: int

    class Config:
        orm_mode = True