from __future__ import annotations

from result import Result, Ok, Err

from lib.shared.domain.value_object.uuid import Uuid


class Id:
    """User id value object"""

    def __init__(self, uuid: Uuid):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param uuid: string value the uuid
        """

        self._uuid = uuid

    @staticmethod
    def new(id: str) -> Result[Id, str]:
        """
        Factory method to create a new Id object.

        If the email received by parameter is valid, it returns an Ok() result containing the Email object.
        Otherwise, it returns an Err() object with the error message.

        @param id: string value of the id
        @return: Resulting Id object
        """

        uuid = Uuid.new(id)

        if uuid.is_ok():
            return Ok(Id(uuid.ok_value))
        else:
            err_msg = uuid.err_value
            return Err(f"Invalid Id `{id}`: {err_msg}")

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two ids are equal if their values
        are the same text string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Id):
            return self.value() == other.value()
        return False

    def value(self) -> str:
        """
        Value object primitive accessor.

        @return: the string value of this id.
        """

        return self._uuid.value()
