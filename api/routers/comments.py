from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas import users
from api.utils import users as users_utils
from api.utils.dependencies import get_current_user

from app.api.schemas.comments import CommentCreate
from app.api.utils.comments import create_comment
from app.api.utils.students import get_student

router = APIRouter(prefix="/comments",)


@router.post("/add")
async def add_comment(comment_data: CommentCreate,
                      user: users.User = Depends(get_current_user)):

    student = await get_student(user.user_id)
    comment_data.student_id = student['id']
    result = await create_comment(comment_data)
    return {"status": "ok", "comment_id": result}
