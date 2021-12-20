from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class CommentCreate(BaseModel):
    assigment_id: Optional[int] = None
    quiz_question_id: Optional[int] = None
    content: str
