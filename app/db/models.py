from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow())


class Fragment(Base):
    __tablename__ = "fragments"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", backref="fragments")


class VectorIndex(Base):
    __tablename__ = "vector_index"
    id = Column(Integer, primary_key=True)
    fragment_id = Column(Integer, ForeignKey("fragments.id"))
    vector_id = Column(Integer, unique=True)
    fragment = relationship("Fragment", backref="vector")
