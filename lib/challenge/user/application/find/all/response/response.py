from __future__ import annotations

from typing import Optional

from lib.shared.domain.bus.query.response import Response as AbstractResponse


class Response(AbstractResponse):
    """Response for find all users service"""

    def __init__(self, data: dict):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param data: dictionary with response needed data
        """

        user_keys = ['id', 'name', 'surname', 'email', 'phone', 'hobbies', 'email_verified', 'phone_verified']
        if 'users' in data and \
                len(data['users']) > 0 and \
                all(all(key in user for key in user_keys) for user in data['users']):
            self._users = data['users']
            self._is_empty = False
            self._is_err = False
        elif 'err_msg' in data:
            self._is_empty = False
            self._is_err = True
            self._err_msg = data['err_msg']
        else:
            self._is_empty = True
            self._is_err = False

    @staticmethod
    def new(data: dict) -> Response:
        """
        Factory method to create a new Response for find all users.

        @param data: dictionary with response needed data
        @return: instance of this Response
        """

        response = Response(data)
        return response

    def is_empty(self) -> bool:
        """
        Checks if current response has no data

        @return: True if empty, False otherwise
        """
        return self._is_empty

    def is_error(self) -> bool:
        """
        Checks if current response has error

        @return: True if has error, False otherwise
        """
        return self._is_err

    def get_error_message(self) -> Optional[str]:
        """
        If this response is an error, returns error message

        @return: error message if has error, None otherwise
        """
        if self.is_error():
            return self._err_msg
        else:
            return None

    def get_users(self) -> Optional[dict]:
        """
        If this response is an error, returns error message

        @return: error message if has error, None otherwise
        """
        if not self.is_error() and not self.is_empty():
            return self._users
        else:
            return None

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two responses are equal if their values
        are the same primitive values.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Response):
            return ((hasattr(self, '_users') and hasattr(other, '_users') and self._users == other._users) or
                    (not hasattr(self, '_users') and not hasattr(other, '_users'))) and \
                self._is_empty == other._is_empty and \
                self._is_err == other._is_err
        return False
