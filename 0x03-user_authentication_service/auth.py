#!/usr/bin/env python3
""" Hash password """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes """
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
