import httpx as httpx

from app.api.models.databases import database
from app.api.models.students import students_table
from app.api.schemas import students as student_schema
from app.api.schemas import users as user_schema


async def create_student(student: student_schema.StudentCreate, user: user_schema.User):
    """ Creates a new student in the database """
    query = students_table.insert().values(
        user_id=user.id,
        login=student.login, password=student.password, domain=student.domain
    )
    last_record_id = await database.execute(query)
    return {**student.dict(), "id": last_record_id, "user_id": user.id}


async def check_student(login: str, password: str):
    res = await login_account(login, password)
    return ''


async def login_account(login: str, password: str):
    url = 'https://canvas.instructure.com/login/canvas'

    async with httpx.AsyncClient() as client:
        resp = client.get(url)

        tree = html.fromstring(r.text)
        token = tree.xpath("//*[@id='login_form']/input[2]")[0]
        payload = {
            'pseudonym_session[unique_id]': login,
            'pseudonym_session[password]': password,
            'pseudonym_session[remember_me]': 1,
            'authenticity_token': token.value
        }
        login_res = client.post(url, data=payload)
        return login_res
    return None
