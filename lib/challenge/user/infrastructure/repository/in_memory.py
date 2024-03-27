from __future__ import annotations
from typing import Optional

from result import Result, Ok, Err

from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.repository import Repository
from lib.challenge.user.domain.user.user import User
from lib.challenge.user.domain.user.users import Users


class InMemory(Repository):
    """Implementation for in memory user repository"""

    def __init__(self, users: list[User] = None):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param users: list of users preloaded in the repository (empty by default)
        """

        self._users: list[User] = users

    @staticmethod
    def new(users: list[User] = None) -> InMemory:
        """
        Factory method to create a new user Repository object.

        @param users: list of users preloaded in the repository (empty by default)
        @return: instance for a new InMemory repository object
        """

        repository = InMemory(users)
        return repository

    def find(self, id: Id) -> Result[Optional[User], str]:
        user_found = [user for user in self._users if user.id() == id.value()]
        if user_found:
            if len(user_found) == 1:
                return Ok(user_found[0])
            else:
                return Err(f"Found more than one user with id `{id.value()}`")
        else:
            return Ok(None)

    def find_all(self) -> Result[Users, str]:
        users = Users.new(self._users.copy())
        return Ok(users)

    def save(self, user: User):
        self._users.append(user)
