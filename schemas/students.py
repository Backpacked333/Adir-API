from typing import Optional

from pydantic import BaseModel


class StudentCreate(BaseModel):
    """ Check existing student account """
    login: str
    password: str
    url: str


class StudentBase(BaseModel):
    """ Build body of answer with Students details """
    id: int
    user_id: int
    url: str
    external_id: Optional[str]
    login: str
    password: str
    token: Optional[str]
