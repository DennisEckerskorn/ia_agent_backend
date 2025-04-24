from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import faiss
import numpy as np
import os

from app.core.jwt import get_current_user
from app.db.dependencies import get_db
from app.services.document_processing import (
    mock_generate_embedding, FAISS_INDEX_PATH, EMBEDDING_DIM
)
from app.db.crud.vectorindex_crud import get_vector_by_vector_id
from app.db.crud.fragment_crud import get_fragment_by_id
from app.core.exceptions import VectorIndexNotFound, FragmentNotFound

router = APIRouter(tags=["IA"])


class AskQuery(BaseModel):
    query: str
    top_k: int = 3


@router.post("/ask")
def ask_question(
    req: AskQuery,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Verificar existencia del índice
    if not os.path.exists(FAISS_INDEX_PATH):
        raise HTTPException(status_code=500, detail="Índice FAISS no inicializado")

    # 1. Generar vector de la consulta
    try:
        query_vector = np.array([mock_generate_embedding(req.query)], dtype=np.float32)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando vector de consulta: {e}")

    # 2. Cargar índice FAISS y buscar
    try:
        index = faiss.read_index(FAISS_INDEX_PATH)
        if index.ntotal == 0:
            raise HTTPException(status_code=500, detail="El índice FAISS está vacío")
        distances, indices = index.search(query_vector, req.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando FAISS: {e}")

    # 3. Recuperar fragmentos desde la base de datos
    resultados = []
    for faiss_id in indices[0]:
        try:
            faiss_id = int(faiss_id)
            vec = get_vector_by_vector_id(db, faiss_id)
            frag = get_fragment_by_id(db, vec.fragment_id)
            resultados.append(frag.text)
        except (VectorIndexNotFound, FragmentNotFound):
            continue
        except Exception as e:
            print(f"Error recuperando fragmento FAISS ID {faiss_id}: {e}")

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron fragmentos relevantes.")

    return {
        "query": req.query,
        "contexto": resultados
    }
