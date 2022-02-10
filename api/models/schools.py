import sqlalchemy

metadata = sqlalchemy.MetaData()


school_table = sqlalchemy.Table(
    "schools",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String()),
    sqlalchemy.Column("login_form_url", sqlalchemy.String()),
    sqlalchemy.Column("logo_url", sqlalchemy.String()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
)


"""
create table schools (
    id SERIAL,
    name varchar,
    login_form_url varchar,
    logo_url varchar,
    created_at timestamp
);

GRANT ALL ON  schools TO  lms;
GRANT USAGE, SELECT ON SEQUENCE schools_id_seq TO lms;
"""
