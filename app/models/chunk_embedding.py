from uuid import UUID,uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from pgvector.sqlalchemy import Vector
from app.database.base import Base
class ChunkEmbedding(Base):
    __tablename__="chunk_embeddings"
    chunk:Mapped['Chunk']=relationship(
        back_populates='embedding'
    )
    id:Mapped[UUID]=mapped_column(
        primary_key=True,
        default=uuid4
    )
    chunk_id:Mapped[UUID]=mapped_column(
        ForeignKey('chunks.id',ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    model_name:Mapped[str]=mapped_column(
        nullable=False
    )
    embedding:Mapped[list[float]]=mapped_column(
        Vector(384),
        nullable=False
    )