import asyncio

from app.database.session import AsyncSessionLocal
from app.repositories.chunk_embedding import ChunkEmbeddingRepository
from app.services.embedding import EmbeddingService


async def main():
    query = "what is data preparation steps?"

    async with AsyncSessionLocal() as session:
        repo = ChunkEmbeddingRepository(session)
        embedding_service = EmbeddingService()

        query_embedding = embedding_service.generate(query)

        results = await repo.search_similar(query_embedding)

        for result in results:
            print("=" * 80)
            print("Score:", result.score)
            print("Document:", result.document.original_filename)
            print("Chunk Index:", result.chunk.chunk_index)
            print("Text:")
            print(result.chunk.text)
            print()


if __name__ == "__main__":
    asyncio.run(main())