from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document,DocumentStatus
from app.models.conversation import Conversation

class DocumentRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def create(self,document:Document)->None:
        self.session.add(document)
    
    async def get_by_id(self,document_id:UUID)->Document|None:
        stmt=select(Document).where(Document.id==document_id)
        result=await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list_by_conversation(self,conversation_id: UUID,user_id: UUID,) -> list[Document]:
        stmt = (
            select(Document)
            .join(Conversation)
            .where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def update_status(self,document_id:UUID,status:DocumentStatus)->bool:
        document= await self.get_by_id(document_id)
        if document is None:
            return False
        else:
            document.status=status
        return True
    
    async def delete_by_id(self,document_id:UUID)->bool:
        document= await self.get_by_id(document_id)
        if document is None:
            return False
        else:
            await self.session.delete(document)
        return True
