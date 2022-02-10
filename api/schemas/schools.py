from pydantic import BaseModel, HttpUrl
from datetime import datetime


class SchoolIn(BaseModel):
    name: str
    login_form_url: HttpUrl
    logo_url: HttpUrl


class School(SchoolIn):
    id: int
    created_at: datetime
