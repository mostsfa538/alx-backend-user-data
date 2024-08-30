#!/usr/bin/env python3
""" Encrypting """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Encrypting passwords """
    bytes = password.encode('utf-8')
    hash = bcrypt.hashpw(bytes, bcrypt.gensalt())

    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check valid password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
