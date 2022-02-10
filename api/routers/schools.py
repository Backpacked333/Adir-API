from fastapi import APIRouter
from api.schemas import schools as schemas
from api.utils import schools as utils


router = APIRouter(prefix="/schools",)

@router.get("/")
async def get_schools():
    return await utils.get_schools()


@router.post("/")
async def create_school(school: schemas.SchoolIn):
    return await utils.create_school(school=school)
