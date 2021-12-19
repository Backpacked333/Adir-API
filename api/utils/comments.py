from api.models.comments import comments_table
from api.models.databases import database

from api.schemas.comments import CommentCreate


async def create_comment(comment_data: CommentCreate, student_id):
    query = comments_table.insert().values(
        content=comment_data.content,
        student_id=student_id,
        assigment_answer_id=comment_data.assigment_answer_id,
        quiz_answer_id=comment_data.quiz_answer_id
    )
    return await database.execute(query)
