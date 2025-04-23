class UserAlreadyExists(Exception):
    """Se lanza cuando se intenta crear un usuario que ya existe"""
    pass


class DocumentNotFound(Exception):
    """Se lanza cuando no se encuentra un documento por ID."""
    pass


class FragmentNotFound(Exception):
    """Se lanza cuando no se encuentra un fragmento"""
    pass


class VectorIndexConflict(Exception):
    """Se lanza cuando el vector_id ya está en uso en FAISS."""
    pass


class VectorIndexNotFound(Exception):
    """Se lanza cuando no se encuentra un índice vector"""
    pass


class DocumentProcessingError(Exception):
    """Error general durante el procesamiento del documento"""
    pass


class PDFExtractionError(DocumentProcessingError):
    """Fallo al extraer texto del PDF"""
    pass


class FAISSLoadError(DocumentProcessingError):
    """Fallo al cargar o guardar el índice FAISS"""
    pass


class FragmentCreationError(DocumentProcessingError):
    """Fallo al guardar un fragmento"""
    pass


class VectorInsertionError(DocumentProcessingError):
    """Fallo al crear el vector en FAISS o en DB"""
    pass
