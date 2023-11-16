from pydantic import BaseModel
from datetime import date
from enum import Enum


class HonorsAwardEnum(str, Enum):
    none = "none"
    cum_laude = "cum_laude"
    magna_cum_laude = "magna_cum_laude"
    summa_cum_laude = "summa_cum_laude"


class QualificationModel(BaseModel):
    institutionid: int
    name: str
    graduationdate: date
    majorfield: str
    gpagrade: str
    honorsaward: HonorsAwardEnum
    staffid: str

    class Config:
        orm_mode = True