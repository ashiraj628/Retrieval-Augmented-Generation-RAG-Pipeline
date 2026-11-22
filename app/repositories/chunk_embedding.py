from uuid import UUID
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete
from sqlalchemy.orm import joinedload
from app.models.chunk_embedding import ChunkEmbedding
from app.models.chunk import Chunk
from app.models.document import Document

@dataclass
class SimilarChunk:
    chunk:Chunk
    document:Document
    score:float



class ChunkEmbeddingRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def create(self,chunk_embedding:ChunkEmbedding)->None:
        self.session.add(chunk_embedding)
    
    async def create_many(self,chunks_embedding:list[ChunkEmbedding])->None:
        self.session.add_all(chunks_embedding)

    async def get_by_chunk_id(self,chunk_id:UUID)-> None|ChunkEmbedding:
        stmt=select(ChunkEmbedding).where(ChunkEmbedding.chunk_id==chunk_id)
        result=await self.session.execute(stmt)
        return result.scalar_one_or_none()
    async def delete_by_chunk_id(self,chunk_id:UUID)->int:
        stmt= delete(ChunkEmbedding).where(ChunkEmbedding.chunk_id==chunk_id)
        result=await self.session.execute(stmt)
        return result.rowcount
    
    async def search_similar(self,query_embedding:list[float],conversation_id:UUID,limit:int=5)->list[SimilarChunk]:
        distance=ChunkEmbedding.embedding.cosine_distance(query_embedding)
        stmt = (
        select(
            ChunkEmbedding,
            distance.label("score"),
        )
        .join(ChunkEmbedding.chunk)
        .join(Chunk.document)
        .where(Document.conversation_id == conversation_id)
        .options(
            joinedload(ChunkEmbedding.chunk)
            .joinedload(Chunk.document)
        )
        .order_by(distance)
        .limit(limit)
    )

        result =await self.session.execute(stmt)

        rows = result.all()
        return [
            SimilarChunk(
                chunk=embedding.chunk,
                document=embedding.chunk.document,
                score=score,
            )
            for embedding, score in rows
        ]


