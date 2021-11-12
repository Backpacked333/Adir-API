import httpx as httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import students, users
from app.utils import users as users_utils, students as students_utils
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/students",)


@router.post("/check-account", response_model=students.StudentBase)
async def check_account(student: students.StudentCreate, user: users.User = Depends(get_current_user)):
    # async with httpx.AsyncClient() as client:
    #     resp = httpx.post(url=student.url, )
    return await students_utils.create_student(student=student, user=user)


@router.get("/me", response_model=students.StudentBase)
async def read_students_me(current_student: students.StudentBase = Depends(get_current_user)):
    return current_student
