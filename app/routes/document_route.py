from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import os

from app.core.jwt import get_current_user
from app.core.roles import require_admin
from app.db.dependencies import get_db
from app.db.crud.document_crud import (
    create_document, get_document_by_id,
    get_all_documents, delete_document
)
from app.db.schemas.documentschema import DocumentCreate, DocumentOut

router = APIRouter(prefix="/documents", tags=["Documentos"])

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- SUBIR DOCUMENTO (ARCHIVO REAL) ----------
@router.post("/upload", response_model=DocumentOut)
def upload_document(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    # Guardar el archivo en disco
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())

    # Guardar en la base de datos
    doc = DocumentCreate(name=name)
    return create_document(db, doc)


# ---------- CREAR DOCUMENTO MANUAL (sin archivo) ----------
@router.post("/", response_model=DocumentOut)
def create_new_document(
    doc: DocumentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return create_document(db, doc)


# ---------- OBTENER DOCUMENTO POR ID ----------
@router.get("/{doc_id}", response_model=DocumentOut)
def get_document_by_id_route(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    document = get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return document


# ---------- LISTAR TODOS LOS DOCUMENTOS ----------
@router.get("/", response_model=list[DocumentOut])
def list_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_all_documents(db)


# ---------- ELIMINAR DOCUMENTO ----------
@router.delete("/{doc_id}", response_model=DocumentOut)
def delete_document_by_id(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    document = delete_document(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return document
