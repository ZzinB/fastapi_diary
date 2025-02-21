from fastapi_users import FastAPIUsers, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.password import PasswordHelper
from app.models import User
from app.core.db import get_user_db

class UserManager(UUIDDMixin, BaseUserManager[User, str]):
    reset_password_token_secret = "SECRET_TOKEN_SECRET"
    verification_token_secret = "SECRET_TOKEN_SECRET"

async def get_user_manager(user_db: SQLAlchemyUserDatabase):
    yield UserManager(user_db)