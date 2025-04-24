from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Fragment(Base):
    __tablename__ = "fragments"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))

    document = relationship("Document", back_populates="fragments")

    vectors = relationship(
        "VectorIndex",
        back_populates="fragment",
        cascade="all, delete-orphan"
    )
