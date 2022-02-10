import databases

from settings import SQLALCHEMY_DATABASE_URL

database = databases.Database(SQLALCHEMY_DATABASE_URL)
