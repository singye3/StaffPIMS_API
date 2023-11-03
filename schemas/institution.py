from pydantic import BaseModel


class InstitutionModel(BaseModel):
    id: int
    name: str
    location: str
    director: str

    class Config:
        orm_mode = True