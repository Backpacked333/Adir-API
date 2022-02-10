import logging

from api.models.databases import database

from api.models.schools import school_table

from api.schemas import schools as schemas
from typing import List
from datetime import datetime


logger = logging.getLogger(__name__)


async def get_schools() -> List[schemas.School]:
    query = school_table.select()
    return await database.fetch_all(query)


async def create_school(school: schemas.SchoolIn) -> schemas.School:
    created_at = datetime.now()

    query = school_table.insert().values(
        name=school.name,
        login_form_url=school.login_form_url,
        logo_url=school.logo_url,
        created_at=created_at,
    )
    school_id = await database.execute(query)

    return schemas.School(id=school_id, created_at=created_at, **school.dict())
