from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.jwt import get_current_user
from app.core.roles import require_admin
from app.db.dependencies import get_db
from app.db.schemas.vectorindexschema import VectorIndexCreate, VectorIndexOut
from app.db.crud.vectorindex_crud import (
    create_vector_index,
    get_vector_by_id,
    get_vector_by_vector_id,
    get_vectors_by_fragment_id,
    delete_vector_index
)
from app.core.exceptions import VectorIndexConflict, VectorIndexNotFound

router = APIRouter(prefix="/vector-index", tags=["Índice Vectorial"])


# ---------- Crear vector index ----------
@router.post("/", response_model=VectorIndexOut)
def create_vector_entry(
        vector: VectorIndexCreate,
        db: Session = Depends(get_db),
        current_user=Depends(require_admin)
):
    try:
        return create_vector_index(db, vector)
    except VectorIndexConflict as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el vector: {e}")


# ---------- Obtener vector index por ID ----------
@router.get("/{vector_id}", response_model=VectorIndexOut)
def get_vector_entry_by_id(
        vector_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    try:
        return get_vector_by_id(db, vector_id)
    except VectorIndexNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---------- Obtener vector index por vector_id (FAISS ID) ----------
@router.get("/faiss-id/{faiss_vector_id}", response_model=VectorIndexOut)
def get_vector_by_faiss_id(
        faiss_vector_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    try:
        return get_vector_by_vector_id(db, faiss_vector_id)
    except VectorIndexNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---------- Obtener todos los vectores de un fragmento ----------
@router.get("/fragment/{fragment_id}", response_model=list[VectorIndexOut])
def get_vectors_by_fragment(
        fragment_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    return get_vectors_by_fragment_id(db, fragment_id)


# ---------- Eliminar vector index ----------
@router.delete("/{vector_id}", response_model=VectorIndexOut)
def delete_vector_entry(
        vector_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_admin)
):
    try:
        return delete_vector_index(db, vector_id)
    except VectorIndexNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
