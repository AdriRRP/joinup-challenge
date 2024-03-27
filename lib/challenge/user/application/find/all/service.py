from __future__ import annotations

from result import Result

from lib.challenge.user.domain.user.repository import Repository
from lib.challenge.user.domain.user.users import Users


class UsersFinder:
    def __init__(self, repository: Repository):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param repository: implementation of user repository
        """

        self._repository = repository

    @staticmethod
    def new(repository: Repository) -> UsersFinder:
        """
        Factory method to create a new UsersFinder.

        @param repository: implementation of user repository
        @return: instance of UserFinder
        """

        service = UsersFinder(repository)
        return service

    def find(self) -> Result[Users, str]:
        """
        Find all users in self repository

        @return: Result of call repository find function
        """
        return self._repository.find_all()
