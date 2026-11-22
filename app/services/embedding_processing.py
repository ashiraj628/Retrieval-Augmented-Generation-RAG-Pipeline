from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chunk_embedding import ChunkEmbedding
from app.repositories.chunk import ChunkRepository
from app.repositories.chunk_embedding import ChunkEmbeddingRepository
from app.repositories.document import DocumentRepository
from app.services.embedding import EmbeddingService
from app.models.document import DocumentStatus




class EmbeddingProcessingService:
    def __init__(self,session:AsyncSession,chunk_repo:ChunkRepository,chunk_embedding_repo:ChunkEmbeddingRepository,embedding_service:EmbeddingService,
                 document_repo:DocumentRepository):
        self.session=session
        self.chunk_repo=chunk_repo
        self.chunk_embedding_repo=chunk_embedding_repo
        self.embedding_service=embedding_service
        self.document_repo=document_repo
    
    async def process_document(self,document_id:UUID):
        try:
            document=await self.document_repo.get_by_id(document_id)
            if document is None:
                raise ValueError(f"Document {document_id} not found")
            
            chunks= await self.chunk_repo.get_by_document_id(document_id)
            if not chunks:
                raise ValueError(f"No chunks found for document {document_id}")
            chunk_texts = [chunk.text for chunk in chunks]

            vectors=self.embedding_service.generate_many(chunk_texts)

            chunk_embedding_models=[]
            for chunk, vector in zip(chunks, vectors):
                chunk_embedding_models.append(
                    ChunkEmbedding(
                        chunk_id=chunk.id,
                        model_name=self.embedding_service.model_name,
                        embedding=vector,
                    )
                )

            await self.chunk_embedding_repo.create_many(chunk_embedding_models)
            document.status=DocumentStatus.READY
            await self.session.commit()
        except Exception:
            await self.session.rollback()

            document = await self.document_repo.get_by_id(document_id)
            if document is not None:
                document.status = DocumentStatus.FAILED
                await self.session.commit()

            raise