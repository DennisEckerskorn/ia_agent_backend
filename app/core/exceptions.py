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
