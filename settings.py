import os

import databases
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DEBUG", True)

DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "LMS-scraping.2021")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "lms")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

API_VERSION = "1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CORS_ORIGINS = [
    "http://localhost:8000",
]





# engine = sqlalchemy.create_engine(
#     SQLALCHEMY_DATABASE_URL, # connect_args={"check_same_thread": False}
# )
# metadata = sqlalchemy.MetaData()
# metadata.create_all(engine)