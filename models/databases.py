from os import environ

import databases

from app.settings import SQLALCHEMY_DATABASE_URL

database = databases.Database(SQLALCHEMY_DATABASE_URL)
