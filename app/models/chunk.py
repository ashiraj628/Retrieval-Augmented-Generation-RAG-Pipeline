from uuid import UUID,uuid4
from sqlalchemy.orm import Mapped , mapped_column,relationship
from sqlalchemy import ForeignKey,UniqueConstraint,Text
from app.database.base import Base


class Chunk(Base):
    __tablename__="chunks"
    __table_args__=(
        UniqueConstraint("document_id","chunk_index"),
    )
    document:Mapped["Document"]=relationship(
        'Document',
        back_populates='chunks'
    )
    embedding:Mapped["ChunkEmbedding"]=relationship(
        back_populates='chunk',
        cascade="all,delete-orphan"
    )
    id:Mapped[UUID]=mapped_column(
        primary_key=True,
        default=uuid4
    )
    document_id:Mapped[UUID]=mapped_column(
        ForeignKey('documents.id',ondelete="CASCADE"),
        nullable=False
    )
    chunk_index:Mapped[int]=mapped_column(
        nullable=False
    )
    text:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )