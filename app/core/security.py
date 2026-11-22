from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import UUID

import jwt
from jwt import InvalidTokenError as JWTInvalidTokenError
from pydantic import ValidationError
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.exceptions import InvalidTokenError
from app.schemas.auth import TokenPayload


password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)

def _create_token(
    user_id: UUID,
    expires_delta: timedelta,
    token_type: Literal["access", "refresh"],
) -> str:
    now = datetime.now(UTC)

    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_access_token(user_id: UUID) -> str:
    return _create_token(
        user_id=user_id,
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes
        ),
        token_type="access",
    )


def create_refresh_token(user_id: UUID) -> str:
    return _create_token(
        user_id=user_id,
        expires_delta=timedelta(
            days=settings.refresh_token_expire_days
        ),
        token_type="refresh",
    )


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        return TokenPayload.model_validate(payload)
    except (JWTInvalidTokenError, ValidationError) as e:
        raise InvalidTokenError("Invalid or expired token.") from e