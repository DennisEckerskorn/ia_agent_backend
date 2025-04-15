from datetime import datetime
from pydantic import BaseModel


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
