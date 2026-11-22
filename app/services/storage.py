import asyncio
from app.core.config import settings
import aiofiles
class StorageService:
    async def save(self,content:bytes,stored_filename:str)->None:
        settings.upload_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        file_path=settings.upload_dir / stored_filename

        async with aiofiles.open(file_path,'wb') as f:
            await f.write(content)


    async def get(self,stored_filename:str)->bytes:
        file_path=settings.upload_dir / stored_filename
        async with aiofiles.open(file_path,'rb') as f:
            return await f.read()

    async def delete(self, stored_filename: str) -> None:
        file_path = settings.upload_dir / stored_filename
        try:
            await asyncio.to_thread(file_path.unlink)
        except FileNotFoundError:
            pass