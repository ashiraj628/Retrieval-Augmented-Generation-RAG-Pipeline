from uuid import UUID
from sqlalchemy import select,delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chunk import Chunk
class ChunkRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def create_many(self,chunks:list[Chunk])->None:
        self.session.add_all(chunks)

    async def get_by_document_id(self,document_id:UUID)->list[Chunk]:
        stmt=select(Chunk).where(Chunk.document_id==document_id).order_by(Chunk.chunk_index)
        result=await self.session.execute(stmt)
        return result.scalars().all()
    
    async def delete_by_document_id(self,document_id:UUID)->int:
        stmt=delete(Chunk).where(Chunk.document_id==document_id)
        result=await self.session.execute(stmt)
        return result.rowcount
    
    async def get_chunks_in_range(
            self,
            document_id: UUID,
            start_index: int,
            end_index: int,
        ) -> list[Chunk]:
        stmt=select(Chunk).where(
            Chunk.document_id==document_id,
            Chunk.chunk_index>=start_index,
            Chunk.chunk_index<=end_index,
            ).order_by(Chunk.chunk_index)
        result = await self.session.execute(stmt)

        return result.scalars().all()