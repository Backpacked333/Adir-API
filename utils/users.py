import hashlib
import os
import random
import string
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import and_

from app.models.databases import database
from app.models.users import tokens_table, users_table
from app.schemas import users as student_schema
from app.schemas.users import UserID


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
        return UserID(**dict(user))
    return None


async def create_user_token(user_id: int):
    """ Creates a token for the user with the specified user_id """
    token = await get_uuid4()
    query = (
        tokens_table.insert().values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id, token=token)
                             .returning(tokens_table.c.token, tokens_table.c.expires)
    )
    return await database.fetch_one(query)


async def create_user(user: student_schema.UserCreate):
    """ Creates a new user in the database """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        email=user.email, full_name=user.full_name, password=f"{salt}${hashed_password}"
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}


# async def get_token_data(token_id):
#     query = tokens_table.select().where(tokens_table.c.id == token_id)
#     return await database.fetch_one(query)


async def get_uuid4():
    """Generate a random UUID."""
    return UUID(bytes=os.urandom(16), version=4).hex
