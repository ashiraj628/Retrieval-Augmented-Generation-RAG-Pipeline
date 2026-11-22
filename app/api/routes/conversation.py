from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,Depends,Response,UploadFile,File
from app.api.dependencies import get_chat_service
from app.api.dependencies import get_conversation_service
from app.api.dependencies import get_db
from app.api.dependencies import get_document_service
from app.services.chat import ChatService
from app.services.document import DocumentService
from app.services.conversation import ConversationService
from app.schemas.chat import ChatResponse,SourceResponse,ChatRequest,ListConversation,Message,ConversationMessages
from app.api.auth_dependencies import get_current_user
from app.models.user import User


router=APIRouter()



@router.post("/conversations")
async def create_conversation(
    conversation_service: ConversationService = Depends(get_conversation_service),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    conversation = await conversation_service.create_conversation(
        user_id=current_user.id,
        title="New chat",
    )
    await session.commit()

    return {
        "id": conversation.id,
        "title": conversation.title,
    }

@router.post("/conversations/{conversation_id}/documents")
async def upload_file(
    conversation_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):
    return await service.upload(
        conversation_id=conversation_id,
        user_id=current_user.id,
        file=file,
    )

@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        result = await chat_service.chat(
            user_id=current_user.id,
            question=request.query,
            conversation_id=request.conversation_id,
        )

        await session.commit()

        return ChatResponse(
            answer=result.answer,
            sources=[
                SourceResponse(
                    document_id=source.document_id,
                    filename=source.filename,
                )
                for source in result.sources
            ],
            conversation_id=result.conversation_id,
        )

    except Exception:
        await session.rollback()
        raise

@router.get("/conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user),
    conversation_service: ConversationService = Depends(get_conversation_service),
):
    result = await conversation_service.list_conversations(
        current_user.id,
    )

    return [
        ListConversation(
            id=convo.id,
            title=convo.title,
            time=convo.updated_at,
        )
        for convo in result
    ]

@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    conversation_service: ConversationService = Depends(get_conversation_service),
):
    conversation = await conversation_service.get_conversation(
        conversation_id,
        current_user.id,
    )
    messages = await conversation_service.get_messages(conversation_id)
    return ConversationMessages(
        conversation=ListConversation(
            id=conversation.id,
            title=conversation.title,
            time=conversation.updated_at,
        ),
        messages=[
            Message(
                id=message.id,
                role=message.role,
                content=message.content,
                created_at=message.created_at,
                sources=[
                    SourceResponse(
                        document_id=UUID(source["document_id"]),
                        filename=source["filename"],
                    )
                    for source in (message.sources or [])
                ]
            )
            for message in messages
        ]
    )

@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    conversation_service: ConversationService = Depends(get_conversation_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await conversation_service.delete_conversation(
            conversation_id,
            current_user.id,
        )

        await session.commit()

        return Response(status_code=204)

    except Exception:
        await session.rollback()
        raise