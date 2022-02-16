from fastapi import APIRouter, Response
from api.schemas import schools as schemas
from api.utils import schools as utils


router = APIRouter(prefix="/schools",)

@router.get("/")
async def get_schools():
    return await utils.get_schools()


@router.post("/")
async def create_school(school: schemas.SchoolIn):
    return await utils.create_school(school=school)


@router.post("/login")
async def school_login(login: schemas.SchoolLogin):
    is_logined = await utils.login_to_school(login=login)
    return Response(status_code=200) if is_logined else Response(status_code=400)
