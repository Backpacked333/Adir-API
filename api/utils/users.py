import hashlib
import os
import random
import string
from datetime import datetime, timedelta
from uuid import UUID
from google.oauth2 import id_token
from google.auth.transport import requests

from fastapi import HTTPException
from sqlalchemy import and_, update

from api.models.databases import database
from api.models.users import tokens_table, users_table
from api.schemas import users as student_schema
from api.schemas.users import UserBase

from api.utils.students import check_student

import settings
from api.schemas.students import StudentCreate
from api.utils.students import create_student


def get_random_string(length=12):
    """ Generate a random string used as salt """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Hashes a password with salt """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Checks that the password hash matches the hash from the database """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_email(email: str):
    """ Returns information about the user """
    query = users_table.select().where(users_table.c.email == email)
    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    """ Returns information about the owner of the specified token """
    query = tokens_table.join(users_table).select().where(
        and_(
            tokens_table.c.token == token,
            tokens_table.c.expires > datetime.now()
        )
    )
    user = await database.fetch_one(query)
    if user:
        update_query = update(users_table).values(last_login=datetime.utcnow()).where(users_table.c.id == user['user_id'])
        await database.execute(update_query)
        return UserBase(**dict(user))
    return None


async def create_user_token(user_id: int):
    """ Creates a token for the user with the specified user_id """
    token = await get_uuid4()
    expires = datetime.now() + timedelta(weeks=settings.TOKEN_LIFETIME_WEEKS)
    query = (
        tokens_table.insert().values(expires=expires, user_id=user_id, token=token)
                             .returning(tokens_table.c.token, tokens_table.c.expires)
    )
    return await database.fetch_one(query)


async def create_user(user: student_schema.UserCreate):
    """ Creates a new user in the database """
    student = StudentCreate(login=user.external_login, password=user.external_password)
    is_account_exist = await check_student(student)
    if not is_account_exist:
        raise HTTPException(status_code=400, detail="Canvas account doesn't exist")

    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        email=user.email, full_name=user.full_name, password=f"{salt}${hashed_password}",
        last_login=datetime.utcnow()
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    student_id = await create_student(student=student, user_id=user_id)

    return {**user.dict(), "user_id": user_id, "student_id": student_id, "token": token_dict}


async def create_user_email(user: student_schema.UserCreateEmail):
    """ Creates a new user in the database """
    student = StudentCreate(login=user.external_login, password=user.external_password)
    is_account_exist = await check_student(student)
    if not is_account_exist:
        raise HTTPException(status_code=400, detail="Canvas account doesn't exist")

    query = users_table.insert().values(
        email=user.email,
        last_login=datetime.utcnow()
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    student_id = await create_student(student=student, user_id=user_id)

    return {**user.dict(), "user_id": user_id, "student_id": student_id, "token": token_dict}

# async def get_token_data(token_id):
#     query = tokens_table.select().where(tokens_table.c.id == token_id)
#     return await database.fetch_one(query)


async def get_uuid4():
    """Generate a random UUID."""
    return UUID(bytes=os.urandom(16), version=4).hex


async def verify_google_token(token):

    # (Receive token by HTTPS POST)

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        id_info = id_token.verify_oauth2_token(token, requests.Request())
        # idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        email = id_info['email']
        return {"status": "ok", "email": email}
    except ValueError:
        return {"status": "error", "message": "Invalid token"}
