from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.jwt import get_current_user
from app.core.roles import require_admin
from app.db.dependencies import get_db
from app.db.schemas.fragmentschema import FragmentCreate, FragmentOut
from app.db.crud.fragment_crud import (
    create_fragment,
    get_fragment_by_id,
    get_all_fragments,
    delete_fragment,
    get_fragments_by_document_id
)
from app.core.exceptions import FragmentNotFound

router = APIRouter(prefix="/fragments", tags=["Fragmentos"])


# ---------- Crear fragmento ----------
@router.post("/", response_model=FragmentOut)
def create_new_fragment(
        fragment: FragmentCreate,
        db: Session = Depends(get_db),
        current_user=Depends(require_admin)
):
    try:
        return create_fragment(db, fragment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el fragmento: {e}")


# ---------- Obtener fragmento por ID ----------
@router.get("/{fragment_id}", response_model=FragmentOut)
def get_fragment(
        fragment_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    try:
        return get_fragment_by_id(db, fragment_id)
    except FragmentNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---------- Listar todos los fragmentos ----------
@router.get("/", response_model=list[FragmentOut])
def list_all_fragments(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    return get_all_fragments(db)


# ---------- Eliminar fragmento ----------
@router.delete("/{fragment_id}", response_model=FragmentOut)
def delete_fragment_by_id(
        fragment_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_admin)
):
    try:
        return delete_fragment(db, fragment_id)
    except FragmentNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---------- Listar fragmentos por documento ----------
@router.get("/by-document/{doc_id}", response_model=list[FragmentOut])
def get_fragments_by_document(
        doc_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    return get_fragments_by_document_id(db, doc_id)
