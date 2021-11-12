import sqlalchemy

metadata = sqlalchemy.MetaData()

assignments_table = sqlalchemy.Table(
    "assignments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_id", sqlalchemy.ForeignKey("student.id")),
    sqlalchemy.Column("assigment_ident", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("description", sqlalchemy.String(1000)),
    sqlalchemy.Column("due_at", sqlalchemy.DateTime(50)),
    sqlalchemy.Column("points_possible", sqlalchemy.String(50)),
    sqlalchemy.Column("grading_type", sqlalchemy.String()),
    sqlalchemy.Column("allowed_attempts", sqlalchemy.String()),
    sqlalchemy.Column("course_id", sqlalchemy.ForeignKey("course.id")),
    sqlalchemy.Column("name", sqlalchemy.String()),
    sqlalchemy.Column("submission_types", sqlalchemy.String()),
    sqlalchemy.Column("has_submitted_submissions", sqlalchemy.String()),
    sqlalchemy.Column("due_date_required", sqlalchemy.DateTime()),
    sqlalchemy.Column("workflow_state", sqlalchemy.String()),
    sqlalchemy.Column("quiz_ident", sqlalchemy.String()),
)


courses_table = sqlalchemy.Table(
    "courses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_id", sqlalchemy.ForeignKey("student.id")),
    sqlalchemy.Column("course_ident", sqlalchemy.String(50), index=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("start_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("end_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("course_code", sqlalchemy.String(50), index=True),

    sqlalchemy.Column("workflow_state", sqlalchemy.String(50)),
    sqlalchemy.Column("enrolled_as", sqlalchemy.String(50))
)
