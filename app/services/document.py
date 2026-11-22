from uuid import uuid4,UUID
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from app.models.document import Document,DocumentStatus
from app.models.chunk import Chunk
from app.services.storage import StorageService
from app.services.pdf import PDFService
from app.services.chunk import ChunkingService
from app.repositories.document import DocumentRepository
from app.repositories.chunk import ChunkRepository
from app.workers.embedding import generate_embeddings
from app.repositories.conversation import ConversationRepository
from app.core.exceptions import ConversationNotFoundError
class DocumentService:
    def __init__(
                self,
                session:AsyncSession,
                storage_service:StorageService,
                document_repo:DocumentRepository,
                chunk_repo:ChunkRepository,
                pdf_service:PDFService,
                chunk_service:ChunkingService,
                conversation_repo:ConversationRepository

            ):
        self.session=session
        self.storage_service=storage_service
        self.document_repo=document_repo
        self.chunk_repo=chunk_repo
        self.pdf_service=pdf_service
        self.chunk_service=chunk_service
        self.conversation_repo=conversation_repo

    async def upload(self,conversation_id:UUID,user_id:UUID,file:UploadFile)->Document:
        conversation = await self.conversation_repo.get_by_id_for_user(conversation_id,user_id)
        if conversation is None:
            raise ConversationNotFoundError()
        
        content=await file.read()
        document_id=uuid4()
        extension=Path(file.filename).suffix
        stored_filename=f"{document_id}{extension}"
        try:
            await self.storage_service.save(content,stored_filename)
            page_count=self.pdf_service.get_page_count(content)
            text=self.pdf_service.extract_text(content)
            chunk_texts=self.chunk_service.split(text)
            document=Document(
                id=document_id,
                conversation_id=conversation_id,
                original_filename=file.filename,
                stored_filename=stored_filename,
                pages=page_count,
                file_size=file.size,
                status=DocumentStatus.PROCESSING
            )
            
            chunk_models=[]
            for index,chunk_text in enumerate(chunk_texts):
                chunk_models.append(
                    Chunk(
                        document_id=document_id,
                        chunk_index=index,
                        text=chunk_text
                    )
                )
            await self.document_repo.create(document)
            await self.chunk_repo.create_many(chunk_models)
            await self.session.commit()
            await self.session.refresh(document)

            #TODO:add worker
            generate_embeddings.send(str(document.id))
            return document
        except Exception:
            await self.session.rollback()
            try:
                await self.storage_service.delete(stored_filename)
            except Exception:
                pass
            raise 
