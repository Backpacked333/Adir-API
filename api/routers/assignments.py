from typing import List, Dict, Optional

from fastapi import APIRouter, Depends, File, UploadFile, Form

from api.schemas import students, users, assignments
from api.utils import assignments as assignments_utils
from api.utils.dependencies import get_current_user
from api.utils.students import get_student
from api.schemas.assignments import QuizAnswerCreate

from app import settings

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
    records = await assignments_utils.get_quizzes_questions(quiz_id=quiz_id)
    return {"total": len(records), "questions": records[skip:skip+limit]}


@router.post("/quizzes/answer")
async def submit_quiz_answer(answer: Optional[str] = Form(...),
                              quiz_id: str = Form(...),
                              question_id: str = Form(...),
                              file: Optional[UploadFile] = File(None),
                              user: users.User = Depends(get_current_user)):
    student = await get_student(user.user_id)
    return await assignments_utils.create_quiz_answer(student_id=student['id'],
                                                      answer=answer,
                                                      quiz_id=quiz_id,
                                                      question_id=question_id,
                                                      file=file)


@router.post("/answer")
async def submit_assignment_answer(answer: Optional[str] = Form(...),
                                   assignment_id: str = Form(...),
                                   file: Optional[UploadFile] = File(None),
                                   user: users.User = Depends(get_current_user)):
    student = await get_student(user.user_id)
    return await assignments_utils.create_assignment_answer(student_id=student['id'],
                                                            answer=answer,
                                                            assignment_id=assignment_id,
                                                            file=file)


@router.get("/quizzes/{quiz_id}", response_model=assignments.QuizzesBase)
async def get_quizzes_details(quiz_id: int, user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_quizzes_details(quiz_id=quiz_id)


@router.get("/{assignment_id}", response_model=assignments.AssignmentBase)
async def assignments_details(assignment_id: int, user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_assignments_details(assignment_id=assignment_id)
