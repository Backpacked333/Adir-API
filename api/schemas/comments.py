from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class CommentCreate(BaseModel):
    assigment_answer_id: Optional[int] = None
    quiz_answer_id: Optional[int] = None
    content: str
    student_id: Optional[str] = None
