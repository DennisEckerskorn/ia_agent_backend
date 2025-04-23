from sqlalchemy.orm import Session
from app.db.models.vectorindex import VectorIndex
from app.db.schemas.vectorindexschema import VectorIndexCreate
from app.core.exceptions import VectorIndexConflict, VectorIndexNotFound


def create_vector_index(db: Session, vector: VectorIndexCreate):
    existing = db.query(VectorIndex).filter(VectorIndex.vector_id == vector.vector_id).first()
    if existing:
        raise VectorIndexConflict(f"El vector_id: {vector.vector_id} ya existe.")

    new_vector = VectorIndex(
        fragment_id=vector.fragment_id,
        vector_id=vector.vector_id
    )
    db.add(new_vector)
    db.commit()
    db.refresh(new_vector)
    return new_vector


def get_vector_by_id(db: Session, vector_id: int):
    vector = db.query(VectorIndex).filter(VectorIndex.id == vector_id).first()
    if not vector:
        raise VectorIndexNotFound(f"Índice vectorial con ID: '{vector_id}' no encontrado.")
    return vector


def get_vector_by_vector_id(db: Session, faiss_vector_id: int):
    vector = db.query(VectorIndex).filter(VectorIndex.vector_id == faiss_vector_id).first()
    if not vector:
        raise VectorIndexNotFound(f"Índice vectorial con vector_id: '{faiss_vector_id}' no encontrado.")
    return vector


def get_vectors_by_fragment_id(db: Session, fragment_id: int):
    return db.query(VectorIndex).filter(VectorIndex.fragment_id == fragment_id).all()


def delete_vector_index(db: Session, vector_index_id: int):
    vi = get_vector_by_id(db, vector_index_id)
    db.delete(vi)
    db.commit()
    return vi
