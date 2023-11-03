from pydantic import BaseModel
from datetime import date
from enum import Enum


class HonorsAwardEnum(str, Enum):
    none = "none"
    cum_laude = "cum_laude"
    magna_cum_laude = "magna_cum_laude"
    summa_cum_laude = "summa_cum_laude"


class QualificationModel(BaseModel):
    id: int
    institutionid: int
    name: str
    graduationdate: date
    majorfield: str
    gpagrade: float
    honorsaward: HonorsAwardEnum
    staffid: int

    class Config:
        orm_mode = True