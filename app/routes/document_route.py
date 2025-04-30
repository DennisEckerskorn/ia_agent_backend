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
from app.services.document_processing import process_document, delete_document_processing
from app.core.exceptions import (
    PDFExtractionError, FAISSLoadError,
    FragmentCreationError, VectorInsertionError,
    DocumentProcessingError
)

router = APIRouter(prefix="/documents", tags=["Documentos"])

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- SUBIR DOCUMENTO (archivo real + procesamiento automático) ----------
@router.post("/upload", response_model=DocumentOut)
def upload_document(
        name: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user=Depends(require_admin)
):
    filepath = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(filepath, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    try:
        doc = DocumentCreate(name=name)
        new_doc = create_document(db, doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar el documento: {e}")

    try:
        process_document(new_doc.id, filepath, db)
    except PDFExtractionError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except (FAISSLoadError, FragmentCreationError, VectorInsertionError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DocumentProcessingError as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

    return new_doc


# ---------- CREAR DOCUMENTO MANUAL (sin archivo) ----------
@router.post("/", response_model=DocumentOut)
def create_new_document(
        doc: DocumentCreate,
        db: Session = Depends(get_db),
        current_user=Depends(require_admin)
):
    try:
        return create_document(db, doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el documento: {e}")


# ---------- OBTENER DOCUMENTO POR ID ----------
@router.get("/{doc_id}", response_model=DocumentOut)
def get_document_by_id_route(
        doc_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    doc = get_document_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc


# ---------- LISTAR TODOS LOS DOCUMENTOS ----------
@router.get("/", response_model=list[DocumentOut])
def list_documents(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    return get_all_documents(db)


# ---------- ELIMINAR DOCUMENTO ----------
@router.delete("/{doc_id}", response_model=DocumentOut)
def delete_document_by_id(
        doc_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_admin)
):
    doc = get_document_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    delete_document_processing(doc.id, doc.name, db)

    return delete_document(db, doc_id)
