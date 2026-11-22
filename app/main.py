from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.search import router as search_router
from app.api.routes.conversation import router as conversation_router
from app.api.routes.auth  import router as auth_router
from app.core.exception_handler import app_exception_handler
from app.core.exceptions import AppException

app=FastAPI(
    title=settings.app_name,
    version="0.1.0"
    )

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.include_router(
    health_router,
    prefix=f"{settings.api_v1_str}/health",
    tags=["Health"],
)
app.include_router(
    search_router,
    prefix=settings.api_v1_str,
    tags=["search"],
)
app.include_router(
    conversation_router,
    prefix=settings.api_v1_str,
    tags=["chat"]
)
app.include_router(
    auth_router,
    prefix=f"{settings.api_v1_str}/auth",
    tags=["Authentication"],
)