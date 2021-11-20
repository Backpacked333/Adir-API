from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssignmentBase(BaseModel):
    """ Build body of answer with Assignment details """
    ind_db: int
    student_id: int
    id: str
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
    html_url: Optional[str]
    quiz_id: Optional[str]
    locked: Optional[str]


class CourseBase(BaseModel):
    """ Build body of answer with Course details """
    id_db: int
    student_id: int
    id: str
    name: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    created_at: Optional[datetime]
    course_code: Optional[str]
    workflow_state: Optional[str]
    enrolled_as: Optional[str]


class QuestionsBase(BaseModel):
    assignment_id: int
    id: str
    student_id: int
    name: Optional[str]
    points: Optional[int]
    type: Optional[str]
    text: Optional[str]
    answer_0: Optional[str]
    answer_1: Optional[str]
    answer_2: Optional[str]
    answer_3: Optional[str]
