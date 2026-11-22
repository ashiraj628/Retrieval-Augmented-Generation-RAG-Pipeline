import asyncio
import dramatiq
from app.workers.session import WorkerSessionLocal
from app.repositories.chunk import ChunkRepository
from app.repositories.chunk_embedding import ChunkEmbeddingRepository
from app.repositories.document import DocumentRepository
from app.services.embedding import EmbeddingService
from app.services.embedding_processing import EmbeddingProcessingService

#TODO : add retry 

@dramatiq.actor
def generate_embeddings(document_id: str):
    asyncio.run(process_document(document_id))


async def process_document(document_id: str):
    async with WorkerSessionLocal() as session:
        service = EmbeddingProcessingService(
            session=session,
            chunk_repo=ChunkRepository(session),
            chunk_embedding_repo=ChunkEmbeddingRepository(session),
            document_repo=DocumentRepository(session),
            embedding_service=EmbeddingService(),
        )

        await service.process_document(document_id)