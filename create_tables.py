# create_tables.py
from app.db.base import Base
from app.db.session import engine

from app.db.models.user import User
from app.db.models.document import Document
from app.db.models.fragment import Fragment
from app.db.models.vectorindex import VectorIndex

def create_all():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas con éxito")

if __name__ == "__main__":
    create_all()
