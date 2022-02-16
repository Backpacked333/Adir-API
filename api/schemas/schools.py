from pydantic import BaseModel, HttpUrl
from datetime import datetime


class SchoolIn(BaseModel):
    name: str
    login_form_url: HttpUrl
    logo_url: HttpUrl = "https://qwertycoding.com/Group%208427.png"


class School(SchoolIn):
    id: int
    created_at: datetime


class SchoolLogin(BaseModel):
    url: str
    username: str
    password: str
