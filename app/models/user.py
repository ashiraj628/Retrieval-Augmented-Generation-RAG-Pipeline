from uuid import UUID,uuid4
from datetime import datetime,UTC
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import DateTime
from app.database.base import Base

class User(Base):
    __tablename__="users"

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    id:Mapped[UUID]=mapped_column(
        default=uuid4,
        primary_key=True
    )
    full_name:Mapped[str]=mapped_column(
        nullable=False
    )
    email:Mapped[str]=mapped_column(
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password:Mapped[str]=mapped_column(
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
