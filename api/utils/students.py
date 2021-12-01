import httpx as httpx
from lxml import html

from api.models.databases import database
from api.models.students import students_table
from api.schemas import students as student_schema


STUDENT_DOMAIN = 'https://unlv.instructure.com/login/canvas'


async def create_student(student: student_schema.StudentCreate, user_id: int):
    """ Creates a new student in the database """
    query = students_table.insert().values(
        user_id=user_id,
        login=student.login, password=student.password, domain=STUDENT_DOMAIN
    )
    return await database.execute(query)


async def check_student(student: student_schema.StudentCreate):
    return await login_account(student.login, student.password)


async def login_account(login: str, password: str):

    async with httpx.AsyncClient() as client:
        resp = await client.get(STUDENT_DOMAIN)

        tree = html.fromstring(resp.text)
        token = tree.xpath("//*[@id='login_form']/input[2]")[0]
        payload = {
            'pseudonym_session[unique_id]': login,
            'pseudonym_session[password]': password,
            'pseudonym_session[remember_me]': 1,
            'authenticity_token': token.value
        }
        login_res = await client.post(STUDENT_DOMAIN, data=payload)
        return True if login_res.status_code == 302 else False
