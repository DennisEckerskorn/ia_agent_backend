from datetime import datetime
from pydantic import BaseModel


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
