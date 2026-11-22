from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message


class MessageRepository:
    def __init__(self,session: AsyncSession,):
        self.session = session

    async def create(self,message: Message,) -> None:
        self.session.add(message)

    async def get_by_id(self,message_id: UUID,) -> Message | None:
        stmt = select(Message).where(Message.id == message_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_conversation(self,conversation_id: UUID,) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_recent_messages(self,conversation_id: UUID,limit: int,) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)

        # Return oldest → newest
        return list(reversed(result.scalars().all()))

