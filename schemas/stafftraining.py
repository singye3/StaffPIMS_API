from pydantic import BaseModel


class StaffTrainingModel(BaseModel):
    staffid: int
    trainingid: int

    class Config:
        orm_mode = True