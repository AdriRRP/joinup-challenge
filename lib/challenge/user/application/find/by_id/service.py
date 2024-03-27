from __future__ import annotations
from typing import Optional

from result import Result

from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.repository import Repository
from lib.challenge.user.domain.user.user import User


class UserFinder:
    def __init__(self, repository: Repository):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param repository: implementation of user repository
        """

        self._repository = repository

    @staticmethod
    def new(repository: Repository) -> UserFinder:
        """
        Factory method to create a new UserFinder.

        @param repository: implementation of user repository
        @return: instance of UserFinder
        """

        service = UserFinder(repository)
        return service

    def find(self, id: Id) -> Result[Optional[User], str]:
        """
        Find user by id in self repository

        @param id:  Id object of user to find
        @return:    Result of call repository find function
        """
        return self._repository.find(id)
