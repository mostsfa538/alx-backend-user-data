#!/usr/bin/env python3
""" Hash password """
import bcrypt
from db import DB
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes """
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ return a string representation of a new UUID """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user if not exists"""
        try:
            self._db.find_user_by(email=email)
        except Exception:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ check the password with bcrypt.checkpw """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('UTF-8'),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ find the user corresponding to the email,
        generate a new UUID and store it in the database as the user’s
        session_id, then return the session ID """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Find user by session ID """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ Destroy session """
        try:
            user = self._db.find_user_by(id=user_id)
        except Exception:
            return None
        self._db.update_user(user.id, session_id=None)
