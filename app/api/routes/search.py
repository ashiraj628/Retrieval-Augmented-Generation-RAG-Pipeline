from fastapi import APIRouter,Depends
from app.api.dependencies import get_search_service
from app.services.search import SearchService
from app.schemas.search import SearchRequest,SearchResponse
router=APIRouter()

@router.post('/search')
async def search_similar(
    request:SearchRequest,
    service: SearchService = Depends(get_search_service),
    ):
    results= await service.search(request.query)
    return [
        SearchResponse(
            document_id=str(similar.document.id),
            chunk_index=similar.chunk.chunk_index,
            chunk_text=similar.chunk.text,
            file_name=similar.document.original_filename,
            score=similar.score,
        )
        for similar in results
    ]