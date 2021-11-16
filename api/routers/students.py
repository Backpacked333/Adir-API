from fastapi import APIRouter, Depends

from api.schemas import students, users
from api.utils.dependencies import get_current_user

router = APIRouter(prefix="/students",)


@router.get("/me", response_model=students.StudentBase)
async def read_students_me(current_student: students.StudentBase = Depends(get_current_user)):
    return current_student
