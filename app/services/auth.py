
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password,verify_password,create_access_token,create_refresh_token,decode_token
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest,AuthResponse,LoginRequest,AccessTokenResponse
from app.schemas.user import UserResponse
from app.core.exceptions import UserAlreadyExistsError,InvalidCredentialsError,InvalidTokenError
class AuthService:
    def __init__(self,session:AsyncSession):
        self.session=session
        self.user_repo=UserRepository(session)

    async def register(self,request:RegisterRequest)->AuthResponse:
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user  is not None:
            raise UserAlreadyExistsError()
        user=User(
            full_name=request.full_name,
            email=request.email,
            hashed_password=hash_password(request.password)
        )
        await self.user_repo.create(user)
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        await self.session.refresh(user)
        return   self._build_auth_response(user)
        
    async def login(self,request:LoginRequest)->AuthResponse:
        user= await self.user_repo.get_by_email(request.email)
        if user is None:
            raise InvalidCredentialsError()
        if not verify_password(request.password,user.hashed_password):
            raise InvalidCredentialsError()
        return self._build_auth_response(user)
    
    def _build_auth_response(self, user: User) -> AuthResponse:
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return AuthResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            refresh_token=refresh_token,
        )
    async def refresh(self,token:str)->AccessTokenResponse:
        payload=decode_token(token)
        if payload.type != "refresh":
            raise InvalidTokenError()
        user=await self.user_repo.get_by_id(payload.sub)
        if user is None:
            raise InvalidTokenError()
        
        access_token = create_access_token(user.id)

        return AccessTokenResponse(
            access_token=access_token
        )
