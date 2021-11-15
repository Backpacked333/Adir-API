from typing import Optional

from pydantic import BaseModel


class StudentCreate(BaseModel):
    """ Check existing student account """
    login: str
    password: str
    domain: str = 'https://canvas.instructure.com'


class StudentBase(BaseModel):
    """ Build body of answer with Students details """
    id: int
    user_id: int
    login: str
    password: str
    bearer_token: Optional[str]
    domain: str
    local_id: Optional[str]
