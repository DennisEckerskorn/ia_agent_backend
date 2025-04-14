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
        orm_mode = True


# ----------- DOCUMENTS ---------
class DocumentCreate(BaseModel):
    """
    Esquema de entrada para registrar un documento en la base de datos.

    El administrador lo usará al subir un nuevo documento.
    """
    name: str


class DocumentOut(BaseModel):
    """
    Esquema de salida para representar un documento ya guardado.

    Incluye fecha de carga para auditoría o filtros.

    """
    id: str
    name: str
    uploaded_at: datetime

    class Config:
        orm_mode = True


# --------- FRAGMENTS ------------
class FragmentCreate(BaseModel):
    """
    Esquema para crear un nuevo fragmento de texto.

    Se usa despues de dividir el documento en trozos.
    """
    text: str
    document_id: int


class FragmentOut(BaseModel):
    """
    Esquema de salida para un fragmento, útil para devolver resultados al usuario.
    """
    id: int
    text: str
    document_id: int

    class Config:
        orm_mode = True


# --------- VECTOR INDEX ---------
class VectorIndexCreate(BaseModel):
    """
    Esquema para registrar la relación entre un fragmento de texto y su vector en FAISS.
    """
    fragment_id: int
    vector_id: int


class VectorIndexOut(BaseModel):
    """
    Esquema de salida para mostrar datos del índice vectorial.
    """
    id: int
    fragment_id: int
    vector_id: int

    class Config:
        orm_mode: True
