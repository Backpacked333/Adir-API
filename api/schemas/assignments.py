from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssignmentBase(BaseModel):
    """ Build body of answer with Assignment details """
    int_db: int
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
    due_date_required: Optional[str]
    workflow_state: Optional[str]
    html_url: Optional[str]
    quiz_id: Optional[str]
    locked: Optional[str]


class QuizzesBase(BaseModel):
    int_db: int
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
    due_date_required: Optional[str]
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
    quiz_id: int
    id: str
    student_id: int
    name: Optional[str]
    points: Optional[int]
    type: Optional[str]
    text: Optional[str]
    answers: Optional[str]


class GradesBase(BaseModel):
    id_db: int
    student_id: int
    course_id: str
    assignment_id: str
    name: Optional[str]
    link: Optional[str]
    status: Optional[str]
    score: Optional[datetime]
    grade: Optional[str]
    out_of: Optional[str]
    due: Optional[str]


class QuizAnswer(BaseModel):
    id: int
    question_id: str
    answer: str
    file_id: Optional[str]
    quiz_id: str
    student_id: int


class QuizAnswers(BaseModel):
    quiz_id: str
    answers: list


class QuizAnswerCreate(BaseModel):
    quiz_id: str
    question_id: str
    answer: str
    file_id: Optional[str]
