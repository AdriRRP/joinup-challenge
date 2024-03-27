from __future__ import annotations

from uuid import UUID

from result import Result, Ok, Err


class Uuid:
    """Generic UUID value object"""

    version = 4

    def __init__(self, uuid: UUID):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param uuid: string value the uuid
        """

        self._uuid = uuid

    @staticmethod
    def new(uuid: str) -> Result[Uuid, str]:
        """
        If the email received by parameter is valid, it returns an Ok() result containing the Uuid object.
        Otherwise, it returns an Err() object with the error message.

        @param uuid: string value of the uuid
        @return: instance of Uuid value object
        """

        try:
            uuid_obj = UUID(uuid, version=Uuid.version)
        except ValueError as e:
            return Err(f"Invalid Uuid `{uuid}`: {str(e)}")

        return Ok(Uuid(uuid_obj))

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two uuids are equal if their values
        are the same text string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Uuid):
            return self.value() == other.value()
        return False

    def value(self) -> str:
        """
        Value object primitive accessor.

        @return: the string value of this uuid.
        """

        return str(self._uuid.urn)[9:]
