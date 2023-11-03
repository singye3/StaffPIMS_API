from pydantic import BaseModel

class DirectoryModel(BaseModel):
    directoryid: int
    name: str
    hod: str

    class Config:
        orm_mode = True