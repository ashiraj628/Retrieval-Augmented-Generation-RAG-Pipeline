from uuid import UUID
from pydantic import BaseModel,Field

class SearchRequest(BaseModel):
    query:str = Field(min_length=1)

class SearchResponse(BaseModel):
    document_id:UUID
    chunk_index:int
    chunk_text:str
    file_name:str
    score:float
