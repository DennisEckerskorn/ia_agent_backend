import os
import fitz
import faiss
import numpy as np
from sqlalchemy.orm import Session

from app.db.crud.fragment_crud import create_fragment, get_fragments_by_document_id
from app.db.crud.vectorindex_crud import create_vector_index, get_vectors_by_fragment_id
from app.db.schemas.fragmentschema import FragmentCreate
from app.db.schemas.vectorindexschema import VectorIndexCreate

from app.core.exceptions import (
    PDFExtractionError, FAISSLoadError,
    FragmentCreationError, VectorInsertionError
)

FAISS_INDEX_PATH = "faiss_indexes/vector.index"
EMBEDDING_DIM = 384  # Simulado, normalmente sería 1536 con OpenAI


def extract_text_from_pdf(filepath: str) -> str:
    try:
        doc = fitz.open(filepath)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text
    except Exception as e:
        raise PDFExtractionError(f"Error extrayendo texto del PDF: {e}")


def split_text_into_chunks(text: str, max_chars: int = 500) -> list[str]:
    paragraphs = text.split("\n")
    chunks, current = [], ""

    for p in paragraphs:
        if len(current) + len(p) <= max_chars:
            current += p + " "
        else:
            chunks.append(current.strip())
            current = p + " "
    if current:
        chunks.append(current.strip())

    return chunks


def mock_generate_embedding(text: str) -> list[float]:
    np.random.seed(abs(hash(text)) % (2 ** 32))
    return list(np.random.rand(EMBEDDING_DIM))


def load_or_create_faiss_index(d: int) -> faiss.IndexFlatL2:
    try:
        if os.path.exists(FAISS_INDEX_PATH):
            print("Cargando índice FAISS desde disco...")
            return faiss.read_index(FAISS_INDEX_PATH)
        else:
            print("Creando un nuevo índice FAISS...")
            return faiss.IndexFlatL2(d)
    except Exception as e:
        raise FAISSLoadError(f"Error al cargar o crear el índice FAISS: {e}")


def save_faiss_index(index: faiss.IndexFlatL2):
    try:
        os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
        faiss.write_index(index, FAISS_INDEX_PATH)
    except Exception as e:
        raise FAISSLoadError(f"Error al guardar el índice FAISS: {e}")


def process_document(document_id: int, filepath: str, db: Session):
    print(f"📄 Procesando documento {filepath} ...")

    text = extract_text_from_pdf(filepath)
    chunks = split_text_into_chunks(text)

    index = load_or_create_faiss_index(EMBEDDING_DIM)
    next_vector_id = index.ntotal

    for chunk in chunks:
        try:
            # 1. Guardar fragmento en base de datos
            fragment = FragmentCreate(text=chunk, document_id=document_id)
            new_frag = create_fragment(db, fragment)
        except Exception as e:
            raise FragmentCreationError(f"No se pudo guardar el fragmento: {e}")

        try:
            # 2. Generar vector y guardar en FAISS
            vector = mock_generate_embedding(chunk)
            np_vector = np.array([vector], dtype=np.float32)
            index.add(np_vector)
        except Exception as e:
            raise VectorInsertionError(f"Error al añadir vector a FAISS: {e}")

        try:
            # 3. Guardar en tabla vector_index
            vector_record = VectorIndexCreate(
                fragment_id=new_frag.id,
                vector_id=next_vector_id
            )
            create_vector_index(db, vector_record)
            next_vector_id += 1
        except Exception as e:
            raise VectorInsertionError(f"Error guardando en la base de datos el vector: {e}")

    save_faiss_index(index)
    print("Documento procesado y persistido con éxito")


def delete_document_processing(document_id: int, document_name: str, db: Session):
    #1. Eliminar archivo del disco.
    filepath = os.path.join("uploaded_docs", f"{document_name}.pdf")
    if os.path.exists(filepath):
        os.remove(filepath)

    #2. Eliminar vectores de FAISS
    if os.path.exists(FAISS_INDEX_PATH):
        try:
            index = faiss.read_index(FAISS_INDEX_PATH)

            fragments = get_fragments_by_document_id(db, document_id)
            faiss_ids = []
            for frag in fragments:
                vectors = get_vectors_by_fragment_id(db, frag.id)
                faiss_ids.extend([vec.vector_id for vec in vectors])

            if faiss_ids:
                selector = faiss.IDSelectorBatch(np.array(faiss_ids, dtype='int64'))
                index.remove_ids(selector)
                faiss.write_index(index, FAISS_INDEX_PATH)

        except Exception as e:
            raise FAISSLoadError(f"Error al limpiar FAISS: {e}")
