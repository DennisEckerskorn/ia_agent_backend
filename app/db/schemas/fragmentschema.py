from datetime import datetime
from pydantic import BaseModel


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
        from_attributes = True
