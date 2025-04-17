from app.db.session import SessionLocal
from app.db.schemas.userschema import UserCreate
from app.db.schemas.documentschema import DocumentCreate
from app.db.schemas.fragmentschema import FragmentCreate
from app.db.schemas.vectorindexschema import VectorIndexCreate

from app.db.crud.user_crud import create_user, get_user_by_username
from app.db.crud.document_crud import create_document, get_all_documents
from app.db.crud.fragment_crud import create_fragment, get_fragments_by_document_id
from app.db.crud.vectorindex_crud import create_vector_index, get_vector_by_vector_id


def test_create_user():
    print("🧪 Test: Crear usuario")
    db = SessionLocal()
    user_data = UserCreate(username="admin", password="123456", role="admin")
    try:
        user = create_user(db, user_data)
        print(f"✅ Usuario creado: {user.username}")
    except Exception as e:
        print(f"⚠️ {e}")
    finally:
        db.close()


def test_create_document():
    print("\n🧪 Test: Crear documento")
    db = SessionLocal()
    try:
        doc = create_document(db, DocumentCreate(name="Manual de pruebas"))
        print(f"✅ Documento creado: {doc.name}")
    except Exception as e:
        print(f"⚠️ {e}")
    finally:
        db.close()


def test_create_fragment():
    print("\n🧪 Test: Crear fragmento")
    db = SessionLocal()
    try:
        documents = get_all_documents(db)
        if not documents:
            print("⚠️ No hay documentos creados aún.")
            return

        doc_id = documents[0].id
        frag = create_fragment(db, FragmentCreate(
            text="Este es un fragmento de prueba.",
            document_id=doc_id
        ))
        print(f"✅ Fragmento creado para documento {doc_id}")
    except Exception as e:
        print(f"⚠️ {e}")
    finally:
        db.close()


def test_create_vector_index():
    print("\n🧪 Test: Crear vector index")
    db = SessionLocal()
    try:
        fragments = get_fragments_by_document_id(db, 1)
        if not fragments:
            print("⚠️ No hay fragmentos disponibles.")
            return

        frag_id = fragments[0].id
        vector = create_vector_index(db, VectorIndexCreate(
            fragment_id=frag_id,
            vector_id=999  # Usa un número único
        ))
        print(f"✅ Vector creado con ID: {vector.vector_id}")
    except Exception as e:
        print(f"⚠️ {e}")
    finally:
        db.close()


if __name__ == "__main__":
    test_create_user()
    test_create_document()
    test_create_fragment()
    test_create_vector_index()
