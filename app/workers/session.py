from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

worker_engine = create_async_engine(
    settings.database_url,
    echo=False,
    poolclass=NullPool,
)

WorkerSessionLocal = async_sessionmaker(
    worker_engine,
    expire_on_commit=False,
)