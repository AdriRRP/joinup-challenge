from __future__ import annotations

from result import Result, Ok, Err


class Name:
    """User name value object"""

    def __init__(self, name: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param name: string value of the name
        """

        self._name = name

    @staticmethod
    def new(name: str) -> Result[Name, str]:
        """
        Factory method to create a new Name object.

        Synthetic restriction of 50 chars is used to show the power of value objects, but is not needed.

        If the name received by parameter is valid, it returns an Ok() result containing the Name object.
        Otherwise, it returns an Err() object with the error message.

        @param name: string value of the name
        @return: Resulting Name object
        """

        if len(name) <= 50:
            return Ok(Name(name))
        else:
            return Err(f"Invalid name length in `{name}`: Names can't be longer than 50 chars")

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two names are equal if their values
        are the same text string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Name):
            return self.value() == other.value()
        return False

    def value(self) -> str:
        """
        Value object primitive accessor.

        @return: the string value of this name.
        """

        return self._name
