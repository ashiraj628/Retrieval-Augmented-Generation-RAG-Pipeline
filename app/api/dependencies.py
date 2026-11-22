from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.document import DocumentService
from app.services.storage import StorageService
from app.services.pdf import PDFService
from app.services.chunk import ChunkingService
from app.services.embedding import EmbeddingService
from app.services.search import SearchService
from app.services.embedding_processing import EmbeddingProcessingService
from app.services.llm import LLMService
from app.services.chat import ChatService
from app.services.conversation import ConversationService
from app.repositories.document import DocumentRepository
from app.repositories.chunk import ChunkRepository
from app.repositories.chunk_embedding import ChunkEmbeddingRepository
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository

def get_pdf_service()->PDFService:
    return PDFService()
def get_storage_service()->StorageService:
    return StorageService()
def get_chunk_service()->ChunkingService:
    return ChunkingService()

def get_embedding_service()->EmbeddingService:
    return EmbeddingService()

def get_document_repository(session:AsyncSession=Depends(get_db))->DocumentRepository:
    return DocumentRepository(session)
def get_chunk_repository(session:AsyncSession=Depends(get_db))->ChunkRepository:
    return ChunkRepository(session)

def get_chunk_embedding_repo(session:AsyncSession=Depends(get_db))->ChunkEmbeddingRepository:
    return ChunkEmbeddingRepository(session)

def get_message_repo(session:AsyncSession=Depends(get_db))->MessageRepository:
    return MessageRepository(session)

def get_conversation_repo(session:AsyncSession=Depends(get_db))->ConversationRepository:
    return ConversationRepository(session)

def get_search_service(
        embedding_service:EmbeddingService=Depends(get_embedding_service),
        chunk_embedding_repo:ChunkEmbeddingRepository=Depends(get_chunk_embedding_repo)
        ):
    return SearchService(
        embedding_service,
        chunk_embedding_repo
    )

def get_llm_service()->LLMService:
    return LLMService()

def get_embedding_processing_service(
    session: AsyncSession = Depends(get_db),
    chunk_repo: ChunkRepository = Depends(get_chunk_repository),
    chunk_embedding_repo: ChunkEmbeddingRepository = Depends(get_chunk_embedding_repo),
    document_repo: DocumentRepository = Depends(get_document_repository),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> EmbeddingProcessingService:
    return EmbeddingProcessingService(
        session=session,
        chunk_repo=chunk_repo,
        chunk_embedding_repo=chunk_embedding_repo,
        embedding_service=embedding_service,
        document_repo=document_repo,
    )


def get_document_service(
    session: AsyncSession = Depends(get_db),
    storage_service: StorageService = Depends(get_storage_service),
    document_repo: DocumentRepository = Depends(get_document_repository),
    chunk_repo:ChunkRepository=Depends(get_chunk_repository),
    pdf_service:PDFService=Depends(get_pdf_service),
    chunk_service:ChunkingService=Depends(get_chunk_service),
    conversation_repo:ConversationRepository=Depends(get_conversation_repo),
) -> DocumentService:
    return DocumentService(
        session=session,
        storage_service=storage_service,
        document_repo=document_repo,
        chunk_repo=chunk_repo,
        pdf_service=pdf_service,
        chunk_service=chunk_service,
        conversation_repo=conversation_repo,
    )


def get_conversation_service(
        session:AsyncSession=Depends(get_db),
        conversation_repo:ConversationRepository=Depends(get_conversation_repo),
        message_repo:MessageRepository=Depends(get_message_repo),
        document_repo:DocumentRepository=Depends(get_document_repository),
        storage_service:StorageService=Depends(get_storage_service)
)->ConversationService:
    return ConversationService(
        session=session,
        conversation_repo=conversation_repo,
        message_repo=message_repo,
        document_repo=document_repo,
        storage_service=storage_service
    )

def get_chat_service(
        llm:LLMService=Depends(get_llm_service),
        search_service:SearchService=Depends(get_search_service),
        chunk_repo:ChunkRepository=Depends(get_chunk_repository),
        conversation_service:ConversationService=Depends(get_conversation_service)
)->ChatService:
    return ChatService(
        llm=llm,
        search_service=search_service,
        chunk_repo=chunk_repo,
        conversation_service=conversation_service
    )