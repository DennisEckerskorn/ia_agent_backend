from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime


class Fragment(Base):
    __tablename__ = "fragments"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", backref="fragments")
