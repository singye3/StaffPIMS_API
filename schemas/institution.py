from pydantic import BaseModel


class InstitutionModel(BaseModel):
    name: str
    location: str

    class Config:
        orm_mode = True