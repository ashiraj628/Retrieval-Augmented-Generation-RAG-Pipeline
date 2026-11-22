from uuid import UUID
from collections import defaultdict
from app.models.chunk import Chunk
from app.models.message import Message
from app.services.search import SearchService
from app.services.llm import LLMService
from app.repositories.chunk import ChunkRepository
from app.repositories.chunk_embedding import SimilarChunk
from app.services.dtos import Source,ChatContext,ChatResponse
from app.services.conversation import ConversationService

class ChatService:
    def __init__(
            self,
            llm:LLMService,
            search_service:SearchService,
            conversation_service:ConversationService,
            chunk_repo:ChunkRepository
            ):
        self.search_service=search_service
        self.llm=llm
        self.conversation_service=conversation_service
        self.chunk_repo=chunk_repo
    
    async def chat(self,user_id: UUID,question:str,conversation_id:UUID|None=None)->ChatResponse:
        if conversation_id is not None:
            conversation=await self.conversation_service.get_conversation(conversation_id,user_id)

        if conversation.title=="New chat":
            conversation.title=question

        history = await self.conversation_service.get_recent_history(
            conversation.id,
            limit=10,
        )
        # save user message
        await self.conversation_service.add_user_message(
            conversation.id,
            question,
        )

        similar_chunks=await self.search_service.search(question,conversation.id)
        if not similar_chunks:
            answer = (
                "I couldn't find any relevant information in the uploaded documents."
                )

            await self.conversation_service.add_assistant_message(
                conversation.id,
                answer,
                [],
            )

            return ChatResponse(
                answer=answer,
                sources=[],
                conversation_id=conversation.id,
            )
        
        grouped_chunks=await self._collect_context(similar_chunks)
        chat_context=self._build_context(grouped_chunks)
        history_text=self._format_history(history)
        prompt=self._build_prompt(chat_context.context,question,history_text)
        answer= await self.llm.generate(prompt)
        #save assistant message
        await self.conversation_service.add_assistant_message(
            conversation.id,
            answer,
            chat_context.sources,
        )
        return ChatResponse(
            answer=answer,
            sources=chat_context.sources,
            conversation_id=conversation.id
        )
        
        
    async def _collect_context(
    self,
    similar_chunks: list[SimilarChunk],
    ) -> dict[UUID, dict[int, Chunk]]:
        grouped_chunks:dict[UUID,dict[int,Chunk]]=defaultdict(dict)
        for similar in similar_chunks: 
            expanded=await self._expand_context(
                similar.chunk.chunk_index,
                similar.document.id
                )
            for chunk in expanded:
                grouped_chunks[chunk.document_id][chunk.chunk_index]=chunk
        return grouped_chunks


    async def _expand_context(self,chunk_index:int,document_id:UUID)->list[Chunk]:
        radius = 1
        start_index = max(0, chunk_index - radius)
        end_index = chunk_index + radius
        return await self.chunk_repo.get_chunks_in_range(document_id,start_index,end_index)

    def _build_context(self,grouped_chunks:dict[UUID,dict[int,Chunk]])->ChatContext:
        context=[]
        sources=[]
        for chunk_map in grouped_chunks.values():
            ordered_chunks=sorted(
                chunk_map.values(),
                key= lambda chunk:chunk.chunk_index
            )
            if not ordered_chunks:
                continue
            first_chunk = ordered_chunks[0]
            sources.append(
                Source(
                    document_id=first_chunk.document_id,
                    filename=first_chunk.document.original_filename
                )
            )
            doc_text = [
                f"Source: {first_chunk.document.original_filename}",
                "",
            ]
            doc_text.extend(chunk.text for chunk in ordered_chunks)
            context.append("\n".join(doc_text))
        return ChatContext(
            context="\n\n".join(context),
            sources=sources
        ) 

    def _build_prompt(self,context:str,question:str,history_text:str)->str:
        return (
            "You are a helpful AI assistant.\n\n"
            "Answer the question using ONLY the provided context.\n\n"
            "If the answer cannot be found in the context, say you don't know.\n\n"
            f"Conversation History:\n{history_text}\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )
    def _format_history(self, history: list[Message]) -> str:
        if not history:
            return ""
        formatted_history = []
        for message in history:
            formatted_history.append(
                f"{message.role.capitalize()}:\n{message.content}"
            )
        return "\n\n".join(formatted_history)