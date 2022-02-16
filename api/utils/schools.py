import logging

from api.models.databases import database

from api.models.schools import school_table

from api.schemas import schools as schemas
from typing import List
from datetime import datetime
import httpx as httpx
from lxml import html


logger = logging.getLogger(__name__)


async def get_schools() -> List[schemas.School]:
    query = school_table.select()
    return await database.fetch_all(query)


async def create_school(school: schemas.SchoolIn) -> schemas.School:
    def is_valid_for_scraping_url(url: str) -> bool:
        is_valid_for_scraping_url = (
            True
            if len(url.replace('https://', '').replace('http://', '').split('/')) == 1
            else False
        )

        return is_valid_for_scraping_url

    created_at = datetime.now()

    # if not is_valid_for_scraping_url(url=school.login_form_url):
    #     raise HTTPException(
    #         status_code=422,
    #         detail="login_form_url isn't valid for scraping url. Example: https://canvas.harvard.edu",
    #     )

    query = school_table.insert().values(
        name=school.name,
        login_form_url=school.login_form_url,
        logo_url=school.logo_url,
        created_at=created_at,
    )
    school_id = await database.execute(query)

    return schemas.School(id=school_id, created_at=created_at, **school.dict())


async def login_to_school(login: schemas.SchoolLogin) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.get(login.url)

        tree = html.fromstring(resp.text)
        token = tree.xpath("//*[@id='login_form']/input[2]")[0]
        payload = {
            'pseudonym_session[unique_id]': login.username,
            'pseudonym_session[password]': login.password,
            'pseudonym_session[remember_me]': 1,
            'authenticity_token': token.value
        }
        login_res = await client.post(login.url, data=payload)
        return True if login_res.status_code == 302 else False