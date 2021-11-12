from app.models.databases import database
from app.models.students import students_table
from app.models.users import tokens_table, users_table
from app.schemas import students as student_schema
from app.schemas import users as user_schema


async def create_student(student: student_schema.StudentCreate, user: user_schema.User):
    """ Creates a new student in the database """
    query = students_table.insert().values(
        user_id=user['id'],
        external_login=student.login, external_password=student.password, url=student.url
    )
    last_record_id = await database.execute(query)
    return {**student.dict(), "id": last_record_id, "user_id": user['id']}

