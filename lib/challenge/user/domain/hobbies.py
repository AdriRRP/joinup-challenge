from __future__ import annotations
from result import Result


class Hobbies:
    """User hobbies value object"""

    def __init__(self, hobbies: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param hobbies: string with user hobbies separated by new line
        """

        self._hobbies = [hobby.strip() for hobby in hobbies.split('\n') if len(hobby.strip()) > 0]
        self._hobbies.sort()

    @staticmethod
    def new(hobbies: str = "") -> Hobbies:
        """
        Factory method to create a new Hobbies object.

        @param hobbies: string with user hobbies separated by new line
        @return: Resulting Hobbies object
        """

        return Hobbies(hobbies)

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two hobbies are equal if their values
        are the same list of string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Hobbies):
            return self.value() == other.value()
        return False

    def value(self) -> list[str]:
        """
        Value object primitive accessor.

        @return: the list of string value of these hobbies.
        """

        return self._hobbies
