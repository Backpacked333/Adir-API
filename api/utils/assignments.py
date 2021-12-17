import os.path

import aiofiles
from api.models.assignments import assignments_table, questions_table, quizzes_table, quiz_answers_table, \
    quizzes_status_table, assignments_status_table, assignment_answers_table
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
    student = await database.fetch_one(query)
    query = quizzes_table.select().where(quizzes_table.c.student_id == student['id'])
    return await database.fetch_all(query)


async def get_quizzes_details(quiz_id: int):
    query = quizzes_table.select().where(quizzes_table.c.int_db == quiz_id)
    return await database.fetch_one(query)


async def get_quizzes_questions(quiz_id: int, student_id: int):
    query = questions_table.select().where(questions_table.c.quiz_id == quiz_id,
                                           questions_table.c.student_id == student_id).order_by('id')
    return await database.fetch_all(query)


async def create_quiz_answers(answers, quiz_id, student_id, file):
    quiz_status_query = quizzes_status_table.select().where(quizzes_status_table.c.quiz_id == quiz_id)
    quiz_status = await database.fetch_one(quiz_status_query)
    if quiz_status and quiz_status['status'] > 10:
        return {'status': 'error', 'message': 'answer was added to server'}

    if file:
        answer = await save_file(file)

    result = await create_update_quiz_answers(answers, quiz_id, student_id)
    if result:
        if not quiz_status:
            await set_status_quiz(quiz_id, student_id)
        return {'status': 'ok'}
    return {'status': 'error', 'message': result}


async def create_update_quiz_answers(answers, question_id, quiz_id, student_id):
    quiz_answer_query = quiz_answers_table.select().where(quiz_answers_table.c.student_id == student_id,
                                                          quiz_answers_table.c.question_id == question_id,
                                                          quiz_answers_table.c.quiz_id == quiz_id)
    quiz_answer = await database.fetch_one(quiz_answer_query)

    if not quiz_answer:
        query = quiz_answers_table.insert().values(
            student_id=student_id,
            question_id=question_id,
            quiz_id=quiz_id,
            answer=answer
        )
        return await database.execute(query)
    else:
        query = quiz_answers_table.update().values(
            answer=answer
        ).where(quiz_answers_table.c.id == quiz_answer['id']).returning(quiz_answers_table.c.id)
        return await database.execute(query)


async def set_status_quiz(quiz_id, student_id, status=10):
    query = quizzes_status_table.insert().values(
        student_id=student_id,
        status=status,
        quiz_id=quiz_id
    )
    await database.execute(query)


async def save_file(file):
    file_path = os.path.join(settings.FILE_ANSWERS_PATH, file.filename)
    os.makedirs(settings.FILE_ANSWERS_PATH, exist_ok=True)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    return file_path


async def create_assignment_answer(assignment_id, student_id, file):
    assignment_status_query = assignments_status_table.select() \
                                    .where(assignments_status_table.c.assignment_id == assignment_id)
    assignment_status = await database.fetch_one(assignment_status_query)
    if assignment_status and assignment_status['status'] > 10:
        return {'status': 'error', 'message': 'answer was added to server'}

    file_path = await save_file(file)

    result = await create_update_assignments_answer(file_path, assignment_id, student_id)
    if result:
        if not assignment_status:
            await set_status_assignment(assignment_id, student_id)
        return {'status': 'ok'}
    return {'status': 'error', 'message': result}


async def set_status_assignment(assignment_id, student_id, status=10):
    query = assignments_status_table.insert().values(
        student_id=student_id,
        status=status,
        assignment_id=assignment_id
    )
    await database.execute(query)


async def create_update_assignments_answer(file_path, assignment_id, student_id):
    assignment_answer_query = assignment_answers_table.select() \
                                                      .where(assignment_answers_table.c.student_id == student_id,
                                                             assignment_answers_table.c.assignment_id == assignment_id)
    assignment_answer = await database.fetch_one(assignment_answer_query)

    if not assignment_answer:
        query = assignment_answers_table.insert().values(
            student_id=student_id,
            assignment_id=assignment_id,
            answer=file_path
        )
        return await database.execute(query)
    else:
        query = assignment_answers_table.update().values(
            answer=file_path
        ).where(assignment_answers_table.c.id == assignment_answer['id']).returning(assignment_answers_table.c.id)
        return await database.execute(query)
