from abc import abstractmethod
from abc import ABCMeta
from typing import Optional

from result import Result

from lib.challenge.user.domain.user import User
from lib.challenge.user.domain.users import Users
from lib.challenge.user.domain.id import Id


class Repository(metaclass=ABCMeta):
    """Abstract user repository contract"""
    @abstractmethod
    def find(self, id: Id) -> Result[Optional[User], str]:
        """
        Finds a user with given user id in this repository.
        If any error found, upwards it.

        @param id: user id value object
        @return: Resulting User (None if not found) or error string
        """
        pass

    @abstractmethod
    def find_all(self) -> Result[Users, str]:
        """
        Finds all users in this repository.
        If any error found, upwards it.

        @return: Resulting Users or error string
        """
        pass

    @abstractmethod
    def save(self, user: User):
        """
        Save a user in this repository.

        @param user: user that wants to save
        @return: Nothing
        """
        pass

    @abstractmethod
    def verify_email(self, id: Id):
        """
        Verify email of user with given id

        @param id: user id value object
        @return: Nothing
        """
        pass

    @abstractmethod
    def verify_phone(self, id: Id):
        """
        Verify phone of user with given id

        @param id: user id value object
        @return: Nothing
        """
        pass
