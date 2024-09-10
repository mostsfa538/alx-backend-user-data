#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save the user to the database and return the User object"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Returns the first row found in the users table filtered by kwargs"""
        model_columns = {c.name for c in inspect(User).columns}

        for k in kwargs.keys():
            if k not in model_columns:
                raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound()

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ update the user’s attributes """
        try:
            user = self.find_user_by(id=user_id)
            valid_columns = {c.name for c in inspect(User).columns}
            for k, v in kwargs.items():
                if k not in valid_columns:
                    raise InvalidRequestError(f"Invalid column name: {k}")
                setattr(user, k, v)

            self._session.commit()
        except NoResultFound:
            raise ValueError()
        except InvalidRequestError:
            raise ValueError()
