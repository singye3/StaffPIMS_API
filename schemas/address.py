from enum import Enum
from pydantic import BaseModel

class DzongkhagEnum(str, Enum):
    THIMPHU = "Thimphu"
    PARO = "Paro"
    PUNAKHA = "Punakha"
    WANGDUE_PHODRANG = "Wangdue Phodrang"
    CHHUKHA = "Chhukha"
    TRASHIGANG = "Trashigang"
    BUMTHANG = "Bumthang"
    TRONGSA = "Trongsa"
    MONGAR = "Mongar"
    GASA = "Gasa"
    HAA = "Haa"
    SAMDRUP_JONGKHAR = "Samdrup Jongkhar"
    TSIRANG = "Tsirang"
    DAGANA = "Dagana"
    ZHEMGANG = "Zhemgang"
    PEMA_GATSHEL = "Pema Gatshel"
    LHUNTSE = "Lhuentse"
    SARPANG = "Sarpang"
    TRASHI_YANGTSE = "Trashiyangtse"
    SAMTSE = "Samtse"


class AddressCreateSchema(BaseModel):
    villagename: str
    gewog: str
    dzongkhag: DzongkhagEnum


class AddressSchema(BaseModel):
    addressid: int
    villagename: str
    gewog: str
    dzongkhag: DzongkhagEnum

    class Config:
        orm_mode = True