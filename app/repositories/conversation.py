from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,update
from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(
            self,
            session:AsyncSession
            ):
        self.session=session

    async def create(self,conversation:Conversation)->None:
        self.session.add(conversation)

    async def get_by_id_for_user(self,conversation_id:UUID,user_id:UUID)->Conversation |None:
        stmt=select(Conversation).where(
            Conversation.id==conversation_id,
            Conversation.user_id==user_id
            )
        result=await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list_for_user(self,user_id:UUID)->list[Conversation]:
        stmt=select(Conversation).where(Conversation.user_id==user_id).order_by(Conversation.updated_at.desc())
        result= await self.session.execute(stmt)
        return result.scalars().all()
    
    async def delete_for_user(self,conversation_id:UUID,user_id:UUID)->int:
        stmt=delete(Conversation).where(Conversation.id == conversation_id, Conversation.user_id==user_id)
        result = await self.session.execute(stmt)
        return result.rowcount
    
    async def update_title_for_user(self,conversation_id:UUID,title:str,user_id:UUID)->bool:
        stmt = (
            update(Conversation)
            .where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .values(title=title)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0
