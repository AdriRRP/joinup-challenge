from __future__ import annotations

from result import Result, Ok, Err


class Surname:
    """User name value object"""

    def __init__(self, surname: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        Arguments:
        surname -- string value of the surname
        """
        self._surname = surname

    @staticmethod
    def new(surname: str) -> Result[Surname, str]:
        """
        Factory method to create a new Surname object.

        Synthetic restriction of 150 chars is used to show the power of value objects, but is not needed.

        If the surname received by parameter is valid, it returns an Ok() result containing the Surname object.
        Otherwise, it returns an Err() object with the error message.

        @param surname: string value of the surname
        @return: Resulting Surname object
        """

        if len(surname) <= 150:
            return Ok(Surname(surname))
        else:
            return Err(f"Invalid surname length in `{surname}`: Surnames can't be longer than 150 chars")

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two surnames are equal if their values
        are the same text string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Surname):
            return self.value() == other.value()
        return False

    def value(self) -> str:
        """
        Value object primitive accessor.

        @return: the string value of this surname.
        """
        return self._surname
