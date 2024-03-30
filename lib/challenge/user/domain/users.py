from __future__ import annotations
from lib.challenge.user.domain.user import User


class Users:
    def __init__(self, users: list[User]):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        Initializes self index to 0 (first element).

        @param users: list of users that this object contains
        """
        self._users: list[User] = users
        self._index = 0

    @staticmethod
    def new(users: list[User]) -> Users:
        """
        Factory method to create a new User object.

        @param users: list of users that this object contains
        @return: Resulting Users object
        """

        users_obj = Users(users)
        return users_obj

    def __iter__(self):
        """
        Makes Users object iterator.

        @return: self instance
        """

        return self

    def __next__(self) -> User:
        """
        This method is needed to make Users iterable.

        @return: next user in this users object
        """
        if self._index < len(self._users):
            user = self._users[self._index]
            self._index += 1
            return user
        raise StopIteration

    def __len__(self):
        """
        Total amount of users wrapped by this object.

        @return: length of self user list
        """
        return len(self._users)

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two users objects are equal if their
        containing users are the same.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Users):
            return set(self) == set(other)
        return False

    def reset_index(self):
        self._index = 0

