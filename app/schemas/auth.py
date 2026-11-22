from pydantic import BaseModel, EmailStr,ConfigDict,Field
from uuid import UUID
from typing import Literal
from app.schemas.user import UserResponse

class TokenPayload(BaseModel):
    model_config = ConfigDict(frozen=True)
    sub: UUID
    type: Literal["access", "refresh"]


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"


class AuthResponse(TokenResponse):
    user: UserResponse

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"