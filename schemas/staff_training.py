from pydantic import BaseModel

class StaffTrainingUpdate(BaseModel):
    trainingid: int

class StaffTrainingCreate(BaseModel):
    staffid: str
    trainingid: int