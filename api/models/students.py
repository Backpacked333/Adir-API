import sqlalchemy

metadata = sqlalchemy.MetaData()

students_table = sqlalchemy.Table(
    "students",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("user.id")),
    sqlalchemy.Column("login", sqlalchemy.String(50)),
    sqlalchemy.Column("password", sqlalchemy.String(50)),
    sqlalchemy.Column("domain", sqlalchemy.String(150)),
    sqlalchemy.Column("bearer_token", sqlalchemy.String(300)),
    sqlalchemy.Column("local_id", sqlalchemy.String(10)),
)
