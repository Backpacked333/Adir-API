import os
import sys


from dotenv import load_dotenv

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(APP_DIR))

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

TOKEN_LIFETIME_WEEKS = 4

QUESTION_PAGINATION_SIZE = 10
