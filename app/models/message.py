from uuid import UUID,uuid4
from datetime import datetime,UTC
from enum import StrEnum
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Enum as SQLEnum,DateTime ,ForeignKey,Text
from sqlalchemy.dialects.postgresql import JSONB
from app.database.base import Base

class MessageRole(StrEnum):
    USER="user"
    ASSISTANT="assistant"

class Message(Base):
    __tablename__="messages"

    conversation:Mapped["Conversation"]=relationship(
        back_populates="messages"
    )

    id:Mapped[UUID]=mapped_column(
        default=uuid4,
        primary_key=True
    )
    conversation_id: Mapped[UUID] = mapped_column(
    ForeignKey("conversations.id",ondelete="CASCADE"),
    nullable=False,
)
    role:Mapped[MessageRole]=mapped_column(
        SQLEnum(MessageRole, name="message_role",),
        nullable=False
    )
    content:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )
    sources: Mapped[list[dict] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(UTC)
    )