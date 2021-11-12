from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssignmentBase(BaseModel):
    """ Build body of answer with Assignment details """
    id: int
    student_id: int
    assigment_ident: str
    description: Optional[str]
    due_at: Optional[datetime]
    points_possible: Optional[str]
    grading_type: Optional[str]
    allowed_attempts: Optional[str]
    course_id: Optional[int]
    name: Optional[str]
    submission_types: Optional[str]
    has_submitted_submissions: Optional[str]
    due_date_required: Optional[datetime]
    workflow_state: Optional[str]
    quiz_ident: Optional[str]


class CourseBase(BaseModel):
    """ Build body of answer with Course details """
    id: int
    student_id: int
    course_ident: str
    name: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    created_at: Optional[datetime]
    course_code: Optional[str]
    workflow_state: Optional[str]
    enrolled_as: Optional[str]
