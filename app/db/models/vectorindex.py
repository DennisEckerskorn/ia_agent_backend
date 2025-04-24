from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class VectorIndex(Base):
    __tablename__ = "vector_index"
    id = Column(Integer, primary_key=True)
    fragment_id = Column(Integer, ForeignKey("fragments.id", ondelete="CASCADE"))
    vector_id = Column(Integer, unique=True)

    fragment = relationship("Fragment", back_populates="vectors")
