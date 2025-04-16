from sqlalchemy.orm import Session
from app.db.models.fragment import Fragment
from app.db.schemas.fragmentschema import FragmentCreate
from app.core.exceptions import FragmentNotFound


def get_fragment_by_id(db: Session, fragment_id: int):
    frag = db.query(Fragment).filter(Fragment.id == fragment_id).first()
    if not frag:
        raise FragmentNotFound(f"Fragmento con ID: '{fragment_id}' no encontrado")
    return frag


def get_all_fragments(db: Session):
    return db.query(Fragment).all()


def get_fragments_by_document_id(db: Session, doc_id: int):
    return db.query(Fragment).filter(Fragment.document_id == doc_id).all()


def create_fragment(db: Session, fragment: FragmentCreate):
    new_fragment = Fragment(
        text=fragment.text,
        document_id=fragment.document_id
    )
    db.add(new_fragment)
    db.commit()
    db.refresh(new_fragment)
    return new_fragment


def delete_fragment(db: Session, fragment_id: int):
    frag = get_fragment_by_id(db, fragment_id)
    db.delete(frag)
    db.commit()
    return frag
