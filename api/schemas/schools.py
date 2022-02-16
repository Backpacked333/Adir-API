from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class SchoolIn(BaseModel):
    name: Optional[str]
    login_form_url: Optional[HttpUrl]
    logo_url: Optional[HttpUrl] = "https://qwertycoding.com/Group%208427.png"
    username: Optional[str]
    password: Optional[str]


class School(SchoolIn):
    id: int
    created_at: Optional[datetime]


class SchoolLogin(BaseModel):
    url: str
    username: str
    password: str
