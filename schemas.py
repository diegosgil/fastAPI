from pydantic import BaseModel
from typing import Optional

class LibroBase(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]

class LibroCreate(LibroBase):
    pass

class LibroOut(LibroBase):
    id: int

    class Config:
        orm_mode = True
