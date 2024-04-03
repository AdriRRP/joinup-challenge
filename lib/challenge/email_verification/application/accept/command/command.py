from __future__ import annotations
from lib.shared.domain.bus.command.command import Command as AbstractCommand


class Command(AbstractCommand):
    """Command implementation to accept a verification"""

    def __init__(self,
                 code: str,
                 ):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param code: verification code in string format
        """
        super().__init__()
        self._code = code

    @staticmethod
    def new(code: str) -> Command:
        """
        Factory method to create a new Command.

        @param code: verification code in string format
        @return: instance of this Command
        """

        command = Command(code)
        return command

    def code(self) -> str:
        """
        Command code primitive accessor.

        @return: the string value of command code.
        """
        return self._code

    @staticmethod
    def command_name() -> str:
        return "accept.email_verification.command"

    def to_primitive(self) -> dict:
        return {
            'code': self._code,
        }
