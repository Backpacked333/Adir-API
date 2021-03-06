from typing import List, Dict, Optional

from fastapi import APIRouter, Depends, File, UploadFile, Form

from api.schemas import students, users, assignments
from api.utils import assignments as assignments_utils
from api.utils.dependencies import get_current_user
from api.utils.students import get_student
from api.schemas.assignments import QuizAnswerCreate

from app import settings
from app.api.schemas.assignments import QuizAnswers

router = APIRouter(prefix="/assignments",)


@router.get("/", response_model=List[assignments.AssignmentBase])
async def get_assignments(user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_assignments_by_user(user=user)


@router.get("/quizzes", response_model=List[assignments.QuizzesBase])
async def get_quizzes(user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_quizzes_by_user(user=user)


@router.get("/quizzes/{quiz_id}/questions")
async def quizzes_questions(quiz_id: str, skip: int = 0, limit: int = settings.QUESTION_PAGINATION_SIZE,
                            user: users.User = Depends(get_current_user)):
    student = await get_student(user.user_id)
    if not student:
        return {"status": "error", "message": "Student didn't find"}
    records = await assignments_utils.get_quizzes_questions(quiz_id=quiz_id, student_id=student['id'])
    return {"total": len(records), "questions": records[skip:skip+limit]}


@router.post("/quizzes/answer")
async def submit_quiz_answer(quiz_answers: QuizAnswers,
                             user: users.User = Depends(get_current_user)):
    student = await get_student(user.user_id)
    return await assignments_utils.create_quiz_answers(student_id=student['id'],
                                                       quiz_answers=quiz_answers)


@router.post("/answer")
async def submit_assignment_answer(assignment_id: str = Form(...),
                                   file: Optional[UploadFile] = File(...),
                                   user: users.User = Depends(get_current_user)):
    student = await get_student(user.user_id)
    return await assignments_utils.create_assignment_answer(student_id=student['id'],
                                                            assignment_id=assignment_id,
                                                            file=file)


@router.get("/quizzes/{quiz_id}", response_model=assignments.QuizzesBase)
async def get_quizzes_details(quiz_id: int, user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_quizzes_details(quiz_id=quiz_id)


@router.get("/{assignment_id}", response_model=assignments.AssignmentBase)
async def assignments_details(assignment_id: int, user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_assignments_details(assignment_id=assignment_id)
