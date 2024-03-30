from __future__ import annotations

import re

from result import Result, Ok, Err


class Phone:
    """User phone value object"""

    def __init__(self, phone: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param phone: string value of the phone number
        """

        self._phone = phone

    @staticmethod
    def new(phone: str) -> Result[Phone, str]:
        """
        Factory method to create a new Phone object.

        If the phone received by parameter is valid, it returns an Ok() result containing the Phone object.
        Otherwise, it returns an Err() object with the error message.

        @param phone: string value of the phone number
        @return: Resulting Phone object
        """

        regex = re.compile(r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')
        if re.fullmatch(regex, phone):
            return Ok(Phone(phone))
        else:
            return Err(f"Invalid phone format in `{phone}`")

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two phone are equal if their values
        are the same text string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Phone):
            return self.value() == other.value()
        return False

    def value(self) -> str:
        """
        Value object primitive accessor.

        @return: the string value of this phone.
        """

        return self._phone
