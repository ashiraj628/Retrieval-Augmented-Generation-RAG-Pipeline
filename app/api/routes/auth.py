from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from app.api.auth_dependencies import get_auth_service
from app.api.auth_dependencies import bearer_scheme
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    AccessTokenResponse,
)
from app.services.auth import AuthService
from app.schemas.user import UserResponse
from app.api.auth_dependencies import get_current_user
from app.models.user import User
router = APIRouter()

@router.post("/register",response_model=AuthResponse,status_code=status.HTTP_201_CREATED,)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(request)


@router.post("/login",response_model=AuthResponse,status_code=status.HTTP_200_OK,)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(request)

@router.post("/refresh",response_model=AccessTokenResponse,status_code=status.HTTP_200_OK,)
async def refresh(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh(credentials.credentials)


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user