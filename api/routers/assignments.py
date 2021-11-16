from typing import List

from fastapi import APIRouter, HTTPException, Depends

from api.schemas import students, users, assignments
from api.utils import assignments as assignments_utils
from api.utils.dependencies import get_current_user

router = APIRouter(prefix="/assignments",)


@router.get("/", response_model=List[assignments.AssignmentBase])
async def get_assignments(user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_assignments_by_user(user=user)


@router.get("/{assignment_id}", response_model=assignments.AssignmentBase)
async def read_students_me(assignment_id: int, user: users.User = Depends(get_current_user)):
    return await assignments_utils.get_assignments_details(assignment_id=assignment_id)
