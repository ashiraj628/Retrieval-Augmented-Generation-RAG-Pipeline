from dataclasses import dataclass
from uuid import UUID
@dataclass
class Source:
    document_id:UUID
    filename:str

@dataclass
class ChatContext:
    context:str
    sources:list[Source]

@dataclass
class ChatResponse:
    answer:str
    sources:list[Source]
    conversation_id:UUID