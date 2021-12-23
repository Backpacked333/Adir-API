from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas import users
from api.utils import users as users_utils
from api.utils.dependencies import get_current_user

from api.schemas.comments import CommentCreate
from api.utils.comments import create_comment, get_assignment_comments, get_quiz_question_comments
from api.utils.students import get_student
from api.schemas import comments

router = APIRouter(prefix="/comments",)


@router.post("/add")
async def add_comment(comment_data: CommentCreate,
                      user: users.User = Depends(get_current_user)):

    student = await get_student(user.user_id)
    result = await create_comment(comment_data, student['id'])
    return {"status": "ok", "comment_id": result}


@router.get("/get/assignment/{assignment_id}", response_model=List[comments.AssigmentComments])
async def get_comments(assignment_id: int, user: users.User = Depends(get_current_user)):
    return await get_assignment_comments(assignment_id)


@router.get("/get/quiz_question/{quiz_question_id}", response_model=List[comments.QuizComments])
async def get_comments(quiz_question_id: int, user: users.User = Depends(get_current_user)):
    return await get_quiz_question_comments(quiz_question_id)
