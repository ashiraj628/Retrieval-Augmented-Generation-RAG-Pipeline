from fastapi import Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.exceptions import InvalidTokenError
from app.core.security import decode_token
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.core.config import settings
bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    token=credentials.credentials
    payload = decode_token(token)
    if payload.type != "access":
        raise InvalidTokenError()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(payload.sub)
    if user is None:
        raise InvalidTokenError()

    return user

def get_auth_service(
    session: AsyncSession = Depends(get_db),
) -> AuthService:
    return AuthService(session)