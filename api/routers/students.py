# import httpx as httpx
from fastapi import APIRouter, HTTPException, Depends

from app.api.schemas import students, users
from app.api.utils import users as users_utils, students as students_utils
from app.api.utils.dependencies import get_current_user

router = APIRouter(prefix="/students",)


@router.get("/me", response_model=students.StudentBase)
async def read_students_me(current_student: students.StudentBase = Depends(get_current_user)):
    return current_student
