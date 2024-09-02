#!/usr/bin/env python3
""" auth module """
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False - path and excluded_paths will be used later """
        if path is None or excluded_paths is None:
            return True
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*' and path.startswith(
                    excluded_path[:-1]):
                return False
            elif path == excluded_path or path + '/' == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object """
        if request is None or 'Authorization' not in request.heders:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object """
        return None
