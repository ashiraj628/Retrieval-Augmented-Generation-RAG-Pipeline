from uuid import UUID,uuid4
from datetime import datetime,UTC
from sqlalchemy.orm import relationship,Mapped,mapped_column
from sqlalchemy import String,DateTime,ForeignKey
from app.database.base import Base

class Conversation(Base):
    __tablename__="conversations"
    messages:Mapped[list["Message"]]=relationship(
        back_populates="conversation",
        cascade="all, delete-orphan"
    )
    documents: Mapped[list["Document"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )

    user: Mapped["User"] = relationship(
        back_populates="conversations"
    )

    id:Mapped[UUID]=mapped_column(
        default=uuid4,
        primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    title:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(UTC)
    )
    updated_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(UTC),
        onupdate=lambda:datetime.now(UTC)
    )