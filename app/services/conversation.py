from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.models.user import User
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository
from app.repositories.document import DocumentRepository
from app.services.dtos import Source
from app.core.exceptions import ConversationNotFoundError
from app.services.storage import StorageService
class ConversationService:
    def __init__(
        self,
        session:AsyncSession,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository,
        document_repo:DocumentRepository,
        storage_service:StorageService
    ):
        self.session=session
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.document_repo=document_repo
        self.storage_service=storage_service

    async def create_conversation(self,user_id:UUID,title: str | None = None,) -> Conversation:
        conversation = Conversation(
            title=title,
            user_id=user_id
        )
        await self.conversation_repo.create(conversation)
        await self.session.flush()
        return conversation

    async def get_conversation(self,conversation_id: UUID,user_id:UUID) -> Conversation:
        conversation= await self.conversation_repo.get_by_id_for_user(
            conversation_id=conversation_id,
            user_id=user_id
        )
        if conversation is None:
            raise ConversationNotFoundError()
        return conversation

    async def list_conversations(self,user_id:UUID) -> list[Conversation]:
        return await self.conversation_repo.list_for_user(user_id)

    async def delete_conversation(self,conversation_id: UUID,user_id:UUID) -> None:
        documents = await self.document_repo.list_by_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )
        for document in documents:
            await self.storage_service.delete(document.stored_filename)

        deleted = await self.conversation_repo.delete_for_user(
            conversation_id= conversation_id,
            user_id=user_id
        )
        if deleted == 0:
            raise ConversationNotFoundError()

    async def add_user_message(self,conversation_id: UUID,content: str,) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=content,
            sources=None,
        )
        await self.message_repo.create(message)
        return message

    async def add_assistant_message(self,conversation_id: UUID,content: str,sources:list[Source],) -> Message:
        sources_json = [
            {
                "document_id": str(source.document_id),
                "filename": source.filename,
            }
            for source in sources
        ]

        message = Message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=content,
            sources=sources_json,
        )

        await self.message_repo.create(message)
        return message

    async def get_recent_history(self,conversation_id: UUID,limit: int,) -> list[Message]:
        return await self.message_repo.get_recent_messages(
            conversation_id,
            limit,
        )
    async def get_messages(self,conversation_id:UUID)->list[Message]:
        return await self.message_repo.list_by_conversation(conversation_id)