import sqlalchemy

metadata = sqlalchemy.MetaData()

students_table = sqlalchemy.Table(
    "students",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("user.id")),
    sqlalchemy.Column("url", sqlalchemy.String(150)),
    sqlalchemy.Column("external_id", sqlalchemy.String(300)),
    sqlalchemy.Column("external_login", sqlalchemy.String(50)),
    sqlalchemy.Column("external_password", sqlalchemy.String(50)),
    sqlalchemy.Column("external_token", sqlalchemy.String()),
)
