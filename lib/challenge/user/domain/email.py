from __future__ import annotations

import re

from result import Result, Ok, Err


class Email:
    """User email value object"""

    def __init__(self, email: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param email: string value of the email
        """
        self._email = email

    @staticmethod
    def new(email: str) -> Result[Email, str]:
        """
        Factory method to create a new Email object.

        If the email received by parameter is valid, it returns an Ok() result containing the Email object.
        Otherwise, it returns an Err() object with the error message.

        @param email: string value of the email
        @return: Resulting Email object
        """

        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            return Ok(Email(email))
        else:
            return Err(f"Invalid email format in `{email}`")

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two emails are equal if their values
        are the same text string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Email):
            return self.value() == other.value()
        return False

    def value(self) -> str:
        """
        Value object primitive accessor.

        @return: the string value of this email.
        """

        return self._email
