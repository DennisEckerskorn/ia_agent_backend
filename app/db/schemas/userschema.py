from datetime import datetime
from pydantic import BaseModel


# ----------- USERS -------------
class UserCreate(BaseModel):
    """
    Esquema de entrada para crear un nuevo usuario.

    Se usa en peticiones POST.
    """
    username: str
    password: str
    role: str


class UserOut(BaseModel):
    """
    Esquema de salida para representar un usuario en la API.

    Evita exponer la contraseña. Se usa al devolver un usuario.
    """
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True
