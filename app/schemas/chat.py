from uuid import UUID
from pydantic import BaseModel,Field
from datetime import datetime
from app.models.message import MessageRole
class SourceResponse(BaseModel):
    document_id: UUID
    filename: str

class ChatRequest(BaseModel):
    query:str = Field(min_length=1)
    conversation_id: UUID | None = None  

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    conversation_id:UUID

class ListConversation(BaseModel):
    id:UUID
    title:str
    time:datetime

class Message(BaseModel):
    id:UUID
    role:MessageRole
    content:str
    created_at:datetime
    sources:list[SourceResponse]

class ConversationMessages(BaseModel):
    conversation:ListConversation
    messages:list[Message]