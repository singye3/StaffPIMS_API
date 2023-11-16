from pydantic import BaseModel
from datetime import date


class CreateTrainingModel(BaseModel):
    institutionid: int
    name: str
    startingdate: date
    endingdate: date

    class Config:
        orm_mode = True

class TrainingModel(BaseModel):
    trainingid: int
    institutionid: int
    name: str
    startingdate: date
    endingdate: date

    class Config:
        orm_mode = True
