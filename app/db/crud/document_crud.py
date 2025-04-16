from sqlalchemy.orm import Session
from app.db.models.document import Document
from app.db.schemas.documentschema import DocumentCreate
from app.core.exceptions import DocumentNotFound


def get_document_by_id(db: Session, doc_id: int):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise DocumentNotFound(f"Documento con ID: '{doc_id}' no encontrado.")
    return doc


def get_all_documents(db: Session):
    return db.query(Document).all()


def create_document(db: Session, doc: DocumentCreate):
    new_doc = Document(name=doc.name)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def delete_document(db: Session, doc_id: int):
    doc = get_document_by_id(db, doc_id)
    db.delete(doc)
    db.commit()
    return doc
