from enum import StrEnum
from datetime import datetime,UTC
from uuid import UUID,uuid4

from sqlalchemy import Enum as SQLEnum,DateTime,ForeignKey
from sqlalchemy.orm import Mapped , mapped_column,relationship

from app.database.base import Base

class DocumentStatus(StrEnum):
    PROCESSING = "PROCESSING"
    EMBEDDING = "EMBEDDING"
    READY = "READY"
    FAILED = "FAILED"

class Document(Base):
    __tablename__="documents"

    chunks:Mapped[list["Chunk"]]=relationship(
        'Chunk',
        back_populates='document',
        cascade="all, delete-orphan",
    )
    conversation: Mapped["Conversation"] = relationship(
        back_populates="documents"
    )
    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    id:Mapped[UUID]=mapped_column(
        primary_key=True,
        default=uuid4
    )
    original_filename:Mapped[str]=mapped_column(
        nullable=False
    )
    stored_filename:Mapped[str]
    pages:Mapped[int]
    file_size:Mapped[int]
    status: Mapped[DocumentStatus] = mapped_column(
        SQLEnum(DocumentStatus),
        default=DocumentStatus.PROCESSING,
    )
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(UTC)
    )