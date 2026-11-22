import asyncio
from sqlalchemy import text
from app.database.session import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as session:
       result =await session.execute(text("SELECT 1"))
       print(result.scalar())



if __name__=="__main__":
    asyncio.run(main())