from pydantic import BaseModel
from datetime import date




class TrainingModel(BaseModel):
    trainingid: int
    institutionid: int
    name: str
    instructorname: str
    startingdate: date
    endingdate: date

    class Config:
        orm_mode = True

class InstituteWithTrainingModel(BaseModel):
    trainingid: int
    name: str
    # institute_name: str