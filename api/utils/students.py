import httpx as httpx
from lxml import html

from api.models.databases import database
from api.models.students import students_table
from api.schemas import students as student_schema


async def create_student(student: student_schema.StudentCreate, user_id: int):
    """ Creates a new student in the database """
    query = students_table.insert().values(
        user_id=user_id,
        login=student.login, password=student.password, domain=student.domain
    )
    return await database.execute(query)


async def check_student(student: student_schema.StudentCreate):
    return await login_account(student.login, student.password)


async def login_account(login: str, password: str):
    url = 'https://canvas.instructure.com/login/canvas'

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

        tree = html.fromstring(resp.text)
        token = tree.xpath("//*[@id='login_form']/input[2]")[0]
        payload = {
            'pseudonym_session[unique_id]': login,
            'pseudonym_session[password]': password,
            'pseudonym_session[remember_me]': 1,
            'authenticity_token': token.value
        }
        login_res = await client.post(url, data=payload)
        return True if login_res.status_code == 302 else False

    raise HTTPException(status_code=400, detail="Can't check")

