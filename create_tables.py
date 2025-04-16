from app.db.base import Base
from app.db.session import engine


def create_all():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas con éxito")


if __name__ == "__main__":
    create_all()
