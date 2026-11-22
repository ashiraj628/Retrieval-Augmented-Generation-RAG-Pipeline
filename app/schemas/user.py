from uuid import UUID
from pydantic import BaseModel, EmailStr,ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    full_name: str
    email: EmailStr
