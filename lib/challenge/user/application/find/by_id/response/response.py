from __future__ import annotations

from typing import Optional

from lib.shared.domain.bus.query.response import Response as AbstractResponse


class Response(AbstractResponse):
    """Response for find user by id service"""

    def __init__(self, data: dict):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param data: dictionary with response needed data
        """

        user_keys = ['id', 'name', 'surname', 'email', 'phone', 'hobbies', 'email_verified', 'phone_verified']
        if all(key in data for key in user_keys):
            self._id = data['id']
            self._name = data['name']
            self._surname = data['surname']
            self._email = data['email']
            self._phone = data['phone']
            self._hobbies = data['hobbies']
            self._email_verified = data['email_verified']
            self._phone_verified = data['phone_verified']
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
        Factory method to create a new Response for find user by id.

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

    def get_user(self) -> Optional[dict]:
        """
        If this response is an error, returns error message

        @return: error message if has error, None otherwise
        """
        if not self.is_error() and not self.is_empty():
            return {
                'id': self._id,
                'name': self._name,
                'surname': self._surname,
                'email': self._email,
                'phone': self._phone,
                'hobbies': self._hobbies,
                'email_verified': self._email_verified,
                'phone_verified': self._phone_verified,
            }
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
            return ((hasattr(self, '_id') and hasattr(other, '_id') and self._id == other._id) or
                    (not hasattr(self, '_id') and not hasattr(other, '_id'))) and \
                ((hasattr(self, '_name') and hasattr(other, '_name') and self._name == other._name) or
                 (not hasattr(self, '_name') and not hasattr(other, '_name'))) and \
                ((hasattr(self, '_surname') and hasattr(other, '_surname') and self._surname == other._surname)
                 or (not hasattr(self, '_surname') and not hasattr(other, '_surname'))) and \
                ((hasattr(self, '_email') and hasattr(other, '_email') and self._email == other._email)
                 or (not hasattr(self, '_email') and not hasattr(other, '_email'))) and \
                ((hasattr(self, '_phone') and hasattr(other, '_phone') and self._phone == other._phone)
                 or (not hasattr(self, '_phone') and not hasattr(other, '_phone'))) and \
                ((hasattr(self, '_hobbies') and hasattr(other, '_hobbies') and self._hobbies == other._hobbies)
                 or (not hasattr(self, '_hobbies') and not hasattr(other, '_hobbies'))) and \
                ((hasattr(self, '_email_verified') and hasattr(other, '_email_verified') and
                  self._email_verified == other._email_verified)
                 or (not hasattr(self, '_email_verified') and not hasattr(other, '_email_verified'))) and \
                ((hasattr(self, '_phone_verified') and hasattr(other, '_phone_verified') and
                  self._phone_verified == other._phone_verified)
                 or (not hasattr(self, '_phone_verified') and not hasattr(other, '_phone_verified'))) and \
                self._is_empty == other._is_empty and \
                self._is_err == other._is_err
        return False
