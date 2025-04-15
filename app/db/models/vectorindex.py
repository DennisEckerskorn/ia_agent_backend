from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime


class VectorIndex(Base):
    __tablename__ = "vector_index"
    id = Column(Integer, primary_key=True)
    fragment_id = Column(Integer, ForeignKey("fragments.id"))
    vector_id = Column(Integer, unique=True)
    fragment = relationship("Fragment", backref="vector")
