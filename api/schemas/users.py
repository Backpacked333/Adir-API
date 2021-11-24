from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    """ Check sign-up request """
    full_name: str
    email: EmailStr
    password: str
    external_login: str
    external_password: str


class UserBase(BaseModel):
    """ Build body of answer with User details """
    user_id: int
    email: EmailStr
    full_name: str
    last_login: datetime = None


class UserID(BaseModel):
    id: int


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        """ Convert UUID в hex string """
        return value.hex


class User(UserBase):
    """ Build body of answer with User details and token """
    token: TokenBase = {}
