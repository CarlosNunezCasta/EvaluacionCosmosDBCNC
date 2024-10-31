from pydantic import BaseModel,Field

class Usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str = Field(..., example='Carlos')
    email: str = Field(..., example='carlos.nunez@example.com')
    edad: int = Field(..., ge =1, example=31)

class Proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str = Field(..., example='Proyecto p1')
    description: str = Field(None, example='Descripcion Proyecto p1')
    id_usuario: str = Field(..., example='u1')
 