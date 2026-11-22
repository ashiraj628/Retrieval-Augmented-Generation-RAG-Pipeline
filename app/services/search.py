from uuid import UUID
from app.services.embedding import EmbeddingService
from app.repositories.chunk_embedding import ChunkEmbeddingRepository,SimilarChunk

class SearchService:
    def __init__(
            self,
            embedding_service:EmbeddingService,
            chunk_embedding_repo:ChunkEmbeddingRepository
            ):
        self.embedding_service=embedding_service
        self.chunk_embedding_repo=chunk_embedding_repo
        
    async def search(self,query:str,conversation_id:UUID)->list[SimilarChunk]:
        query_embedding= self.embedding_service.generate(query)
        return await self.chunk_embedding_repo.search_similar(
                query_embedding=query_embedding,
                conversation_id=conversation_id
            )
        