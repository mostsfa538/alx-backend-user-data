#!/usr/bin/env python3
""" Basic auth """
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ class BasicAuth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.split()[-1]

    def decode_base64_authorization_header(self,
                                           base64_authorization: str) -> str:
        """ returns the decoded value of a Base64 string """
        if base64_authorization is None:
            return None
        if not isinstance(base64_authorization, str):
            return None
        try:
            val = base64.b64decode(base64_authorization)
            return val.decode('UTF-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        data = decoded_base64_authorization_header.split(':')
        email = data[0]
        password = ':'.join(data[1:])
        return (email, password)
