import os.path

import aiofiles
from api.models.assignments import assignments_table, questions_table, quizzes_table, quiz_answers_table
from api.models.databases import database
from api.models.students import students_table
from api.schemas import users as user_schema

from app import settings


async def get_assignments_by_user(user: user_schema.User):
    query = students_table.select().where(students_table.c.user_id == user.user_id)
    students = await database.fetch_all(query)
    students_ids = [student['id'] for student in students]
    query = assignments_table.select().where(assignments_table.c.student_id.in_(students_ids))
    return await database.fetch_all(query)


async def get_assignments_details(assignment_id: int):
    query = assignments_table.select().where(assignments_table.c.int_db == assignment_id)
    return await database.fetch_one(query)


async def get_quizzes_by_user(user: user_schema.User):
    query = students_table.select().where(students_table.c.user_id == user.user_id)
    students = await database.fetch_all(query)
    students_ids = [student['id'] for student in students]
    query = quizzes_table.select().where(assignments_table.c.student_id.in_(students_ids))
    return await database.fetch_all(query)


async def get_quizzes_details(quiz_id: int):
    query = quizzes_table.select().where(quizzes_table.c.int_db == quiz_id)
    return await database.fetch_one(query)


async def get_quizzes_questions(quiz_id: int):
    query = questions_table.select().where(questions_table.c.quiz_id == quiz_id).order_by('id')
    return await database.fetch_all(query)


async def create_quiz_answer(answer, quiz_id, question_id, student_id, file):
    file_path = await save_file(file)

    query = quiz_answers_table.insert().values(
        student_id=student_id,
        question_id=question_id,
        quiz_id=quiz_id,
        file_id=file_path,
        answer=answer
    )
    return await database.execute(query)


async def save_file(file):
    file_path = os.path.join(settings.FILE_ANSWERS_PATH, file.filename)
    os.makedirs(settings.FILE_ANSWERS_PATH, exist_ok=True)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    return file_path
