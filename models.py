from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
 
class Usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str= Field(..., example='Carlos')
    email: EmailStr = Field(..., example='carlos.nunez@teamsoft.com.pe')
    edad: str = Field(..., example='2024-10-30T19:00:00Z')

class Proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str = Field(..., example='Proyecto p1')
    description: Optional[str] = Field(None, example='Descripcion Proyecto p1')
    id_usuario: Field(..., example='u1')
    fecha_creacion: str = Field(..., example='2024-10-30T19:00:00Z')
