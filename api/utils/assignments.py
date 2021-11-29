from api.models.assignments import assignments_table, questions_table, quizzes_table
from api.models.databases import database
from api.models.students import students_table
from api.schemas import users as user_schema


async def get_assignments_by_user(user: user_schema.User):
    query = students_table.select().where(students_table.c.user_id == user.user_id)
    students = await database.fetch_all(query)
    students_ids = [student['id'] for student in students]
    query = assignments_table.select().where(assignments_table.c.student_id.in_(students_ids))
    return await database.fetch_all(query)


async def get_assignments_details(assignment_id: int):
    query = assignments_table.select().where(assignments_table.c.ind_db == assignment_id)
    return await database.fetch_one(query)


async def get_assignments_questions(assignment_id: int):
    query = questions_table.select().where(questions_table.c.assignment_id == assignment_id).order_by('id')
    return await database.fetch_all(query)


async def get_quizzes_by_user(user: user_schema.User):
    query = students_table.select().where(students_table.c.user_id == user.user_id)
    students = await database.fetch_all(query)
    students_ids = [student['id'] for student in students]
    query = quizzes_table.select().where(assignments_table.c.student_id.in_(students_ids))
    return await database.fetch_all(query)


async def get_quizzes_details(assignment_id: int):
    query = quizzes_table.select().where(assignments_table.c.ind_db == assignment_id)
    return await database.fetch_one(query)


async def get_quizzes_questions(assignment_id: int):
    query = questions_table.select().where(questions_table.c.assignment_id == assignment_id).order_by('id')
    return await database.fetch_all(query)
