import httpx as httpx
from lxml import html

from api.models.databases import database
from api.models.students import students_table
from api.schemas import students as student_schema


STUDENT_DOMAIN = 'https://canvas.instructure.com'
STUDENT_LOGIN_URL = f'{STUDENT_DOMAIN}/login/canvas'


async def create_student(student: student_schema.StudentCreate, user_id: int):
    """ Creates a new student in the database """
    query = students_table.insert().values(
        user_id=user_id,
        login=student.login, password=student.password, domain=STUDENT_DOMAIN
    )
    return await database.execute(query)


async def check_student(student: student_schema.StudentCreate):
    return await login_account(student.login, student.password)


async def get_student(user_id: int):
    query = students_table.select().where(students_table.c.user_id == user_id)
    return await database.fetch_one(query)


async def login_account(login: str, password: str):

    async with httpx.AsyncClient() as client:
        resp = await client.get(STUDENT_LOGIN_URL)

        tree = html.fromstring(resp.text)
        token = tree.xpath("//*[@id='login_form']/input[2]")[0]
        payload = {
            'pseudonym_session[unique_id]': login,
            'pseudonym_session[password]': password,
            'pseudonym_session[remember_me]': 1,
            'authenticity_token': token.value
        }
        login_res = await client.post(STUDENT_LOGIN_URL, data=payload)
        return True if login_res.status_code == 302 else False
