import sqlalchemy

metadata = sqlalchemy.MetaData()

assignments_table = sqlalchemy.Table(
    "assignments",
    metadata,
    sqlalchemy.Column("ind_db", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_id", sqlalchemy.ForeignKey("student.id")),
    sqlalchemy.Column("id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("description", sqlalchemy.String(1000)),
    sqlalchemy.Column("due_at", sqlalchemy.DateTime(50)),
    sqlalchemy.Column("points_possible", sqlalchemy.String(50)),
    sqlalchemy.Column("grading_type", sqlalchemy.String(50)),
    sqlalchemy.Column("allowed_attempts", sqlalchemy.String(50)),
    sqlalchemy.Column("course_id", sqlalchemy.ForeignKey("course.id")),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("submission_types", sqlalchemy.String(50)),
    sqlalchemy.Column("has_submitted_submissions", sqlalchemy.String(50)),
    sqlalchemy.Column("due_date_required", sqlalchemy.DateTime(50)),
    sqlalchemy.Column("workflow_state", sqlalchemy.String(50)),
    sqlalchemy.Column("html_url", sqlalchemy.String(150)),
    sqlalchemy.Column("quiz_id", sqlalchemy.String(50)),
    sqlalchemy.Column("locked", sqlalchemy.String(5)),
)


quizzes_table = sqlalchemy.Table(
    "quizzes",
    metadata,
    sqlalchemy.Column("ind_db", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_id", sqlalchemy.ForeignKey("student.id")),
    sqlalchemy.Column("id", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("description", sqlalchemy.String(1000)),
    sqlalchemy.Column("due_at", sqlalchemy.DateTime(50)),
    sqlalchemy.Column("points_possible", sqlalchemy.String(50)),
    sqlalchemy.Column("grading_type", sqlalchemy.String(50)),
    sqlalchemy.Column("allowed_attempts", sqlalchemy.String(50)),
    sqlalchemy.Column("course_id", sqlalchemy.ForeignKey("course.id")),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("submission_types", sqlalchemy.String(50)),
    sqlalchemy.Column("has_submitted_submissions", sqlalchemy.String(50)),
    sqlalchemy.Column("due_date_required", sqlalchemy.DateTime(50)),
    sqlalchemy.Column("workflow_state", sqlalchemy.String(50)),
    sqlalchemy.Column("html_url", sqlalchemy.String(150)),
    sqlalchemy.Column("quiz_id", sqlalchemy.String(50)),
    sqlalchemy.Column("locked", sqlalchemy.String(5)),
)

courses_table = sqlalchemy.Table(
    "courses",
    metadata,
    sqlalchemy.Column("id_db", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_id", sqlalchemy.ForeignKey("student.id")),
    sqlalchemy.Column("id", sqlalchemy.String(50), index=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("start_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("end_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("course_code", sqlalchemy.String(50), index=True),
    sqlalchemy.Column("workflow_state", sqlalchemy.String(50)),
    sqlalchemy.Column("enrolled_as", sqlalchemy.String(50))
)


questions_table = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("assignment_id", sqlalchemy.Integer),
    sqlalchemy.Column("id", sqlalchemy.String(12), index=True),
    sqlalchemy.Column("student_id", sqlalchemy.ForeignKey("student.id")),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("points", sqlalchemy.Integer),
    sqlalchemy.Column("type", sqlalchemy.String(25)),
    sqlalchemy.Column("text", sqlalchemy.Text()),
    sqlalchemy.Column("answer_0", sqlalchemy.String(50)),
    sqlalchemy.Column("answer_1", sqlalchemy.String(50)),
    sqlalchemy.Column("answer_2", sqlalchemy.String(50)),
    sqlalchemy.Column("answer_3", sqlalchemy.String(50)),
)


grades_table = sqlalchemy.Table(
    "grades",
    metadata,
    sqlalchemy.Column("id_db", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_id", sqlalchemy.ForeignKey("student.id")),
    sqlalchemy.Column("course_id", sqlalchemy.String(50)),
    sqlalchemy.Column("assignment_id", sqlalchemy.String(50)),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("link", sqlalchemy.String(150)),
    sqlalchemy.Column("status", sqlalchemy.String(50)),
    sqlalchemy.Column("score", sqlalchemy.String(5)),
    sqlalchemy.Column("grade", sqlalchemy.String(5)),
    sqlalchemy.Column("out_of", sqlalchemy.String(5)),
    sqlalchemy.Column("due", sqlalchemy.String(50)),
)
